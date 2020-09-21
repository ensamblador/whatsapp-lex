import boto3
import json
import os
from zipfile import ZipFile 


def on_event(event, context):
  print(event)
  request_type = event['RequestType']
  if request_type == 'Create': return on_create(event)
  if request_type == 'Update': return on_update(event)
  if request_type == 'Delete': return on_delete(event)
  raise Exception("Invalid request type: %s" % request_type)

def on_create(event):
  props = event["ResourceProperties"]
  client = boto3.client('lex-models')

  bot_definition = json.load(open('bot-definition.json'))
  bot_definition["resource"]["intents"][0]["fulfillmentActivity"]["codeHook"]["uri"] = os.environ.get('LAMBDA_ARN_FULLFILL')
  bot_definition["resource"]["locale"] = os.environ.get('BOT_LOCALE')

  with ZipFile('/tmp/bot-definition.zip','w') as zip: 
      with open('/tmp/bot-definition.json','w') as file:
          json.dump(bot_definition, file)
      zip.write('/tmp/bot-definition.json')

  with open('/tmp/bot-definition.zip', 'rb') as f:
    bytes_read = f.read()

  response = client.start_import(
    payload = bytes_read,
    resourceType='BOT',
    mergeStrategy='OVERWRITE_LATEST',
  )
  print (response)

  print("create new resource with props %s" % props)

  # add your create code here...
  physical_id = response['importId']

  return { 'PhysicalResourceId': physical_id }

def on_update(event):
  physical_id = event["PhysicalResourceId"]
  props = event["ResourceProperties"]
  on_create(event)
  print("update resource %s with props %s" % (physical_id, props))
  # ...

def on_delete(event):
  physical_id = event["PhysicalResourceId"]
  print("delete resource %s" % physical_id)
  bot_definition = json.load(open('bot-definition.json'))
  bot_name = bot_definition["resource"]["name"]
  intents = bot_definition["resource"]['intents']
  slot_types = bot_definition["resource"]['slotTypes']
  
  client = boto3.client('lex-models')
  
  delete_bot = client.delete_bot(name=bot_name)
  print(delete_bot)
  #for intent in intents:
  #    print(client.delete_intent(name=intent['name']))
      
  #for slot_type in slot_types:
  #    print(client.delete_slot_type(name=slot_type['name']))
  
  # ...


def is_complete(event, context):
  physical_id = event["PhysicalResourceId"]
  request_type = event["RequestType"]
  print(physical_id,request_type)
  
  if request_type.lower() == 'create':
    return is_complete_create(event)

  if request_type.lower() == 'update':
    return is_complete_create(event)

  if request_type.lower() == 'delete':
    return { 'IsComplete': True }
      
  return { 'IsComplete': False }


def is_complete_create (event):
  physical_id = event["PhysicalResourceId"]
  client = boto3.client('lex-models')

  response = client.get_import(importId=physical_id)
  status = response["importStatus"]
  is_complete = False
  if (status=="FAILED"):
    raise Exception(response["failureReason"]) 

  if (status=="IN_PROGRESS"):
    return { 'IsComplete': False }

  if (status=="COMPLETE"):
    bot_definition = json.load(open('bot-definition.json'))
    bot_name = bot_definition["resource"]["name"]
    bot = client.get_bot(name=bot_name, versionOrAlias='$LATEST')
    del bot['ResponseMetadata']
    del bot['createdDate']
    del bot['lastUpdatedDate']
    del bot['status']
    del bot['version']
    put_bot_response = client.put_bot(**bot)
    if put_bot_response['status'] == 'FAILED':
      raise Exception(put_bot_response["failureReason"])

    is_complete = True

  return { 'IsComplete':  is_complete}