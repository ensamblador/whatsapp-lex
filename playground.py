#%%
import json
# %%
LEX_BOT_FILE = './lex-bot-definition/bot-definition.json'
bot_definition = json.load(open(LEX_BOT_FILE))

# %%
bot_definition['resource']['intents'][0]['fulfillmentActivity']['codeHook']['uri']
# %%

bot_definition

# %%
import uuid

# %%
uuid.uuid4()
# %%
str(uuid.uuid4()).split('-')[-1]
# %%
res=bot_definition['resource']['intents']
# %%
for intent in bot_definition['resource']['intents']:
    intent['name'] = intent['name']+'sufijo'
# %%
res
# %%
res = bot_definition['resource']
# %%
res['intents'][0]['slots']
# %%
res['slotTypes']
# %%
import boto3
# %%
client = boto3.client('lex-models')

# %%
res = client.response = client.delete_bot(
    name='ScheduleAppointment_esUS'
)

# %%
res
# %%
response = client.get_bot_aliases(
    botName='ScheduleAppointment_esUS'
)
# %%
response

# %%
response = client.get_bot_channel_associations(
    botName='ScheduleAppointment_esUS',
    botAlias='agendar'
)
# %%
response['botChannelAssociations']
# %%
