import json
import os
import subprocess
import uuid
import stat
import shutil
import boto3
import datetime
from twilio.twiml.messaging_response import Body, Message, Redirect, MessagingResponse
import urllib
from botocore.vendored import requests

import boto3
client = boto3.client('lex-runtime')


lambda_tmp_dir = '/tmp' # Lambda fuction can use this directory.
local_source_audio = "{0}/downloaded".format(lambda_tmp_dir)
output_file = "{0}/output.wav".format(lambda_tmp_dir)
botAlias ='$LATEST'

def is_lambda_runtime():
    return True if "LAMBDA_TASK_ROOT" in os.environ else False

if is_lambda_runtime():
    # ffmpeg is stored with this script.
    # When executing ffmpeg, execute permission is requierd.
    # But Lambda source directory do not have permission to change it.
    # So move ffmpeg binary to `/tmp` and add permission.
    ffmpeg_bin = "{0}/ffmpeg.linux64".format(lambda_tmp_dir)
    shutil.copyfile('/opt/ffmpeg.linux64', ffmpeg_bin)
    os.environ['IMAGEIO_FFMPEG_EXE'] = ffmpeg_bin
    os.chmod(ffmpeg_bin, os.stat(ffmpeg_bin).st_mode | stat.S_IEXEC)
    

def main(event, context):

    log_banner('Log de Ejecución')

    body = urllib.parse.parse_qs(event["body"])

    print('body: {}'.format(json.dumps(body)))

    response = MessagingResponse()
    message = Message()
    
    try:
        session = client.get_session(
            botName='ScheduleAppointment_esUS_A',
            botAlias=botAlias,
            userId=body['From'][0].replace(':','').replace('+','')
        )
        
    except Exception:
        session = client.put_session(
            botName='ScheduleAppointment_esUS_A',
            botAlias=botAlias,
            userId=body['From'][0].replace(':','').replace('+','')
        )
    
    print (session)
    
    if "Body" in body:
        lex_response = client.post_text(
            botName='ScheduleAppointment_esUS_A',
            botAlias=botAlias,
            userId=body['From'][0].replace(':','').replace('+',''),
            inputText=body['Body'][0]
        )
        print (lex_response)
        message.body(lex_response['message'])
    
    if "MediaUrl0" in body:
        download_audio(body['MediaUrl0'][0])
        transcode_audio()
        print ("start request")
    
        with open(output_file, 'rb') as file:
            binary_file = file.read()

    
        response_content = client.post_content(
            botName='ScheduleAppointment_esUS_A',
            botAlias=botAlias,
            userId=body['From'][0].replace(':','').replace('+',''),
            accept='text/plain; charset=utf-8',
            #accept='audio/mpeg',
            contentType='audio/l16; rate=16000; channels=1',
            inputStream=binary_file
        )  
        print (response_content)
        message.body(response_content['message'])


                

    
    response.append(message)

    return {
        'statusCode': 200,
        "headers": {
            "Content-Type": "text/html",
        },
        'body': str(response)
    }



def log_banner(text):
    banner_width = len(text)+8
    print (banner_width*'*')
    print ('*** {} ***'.format(text))
    print (banner_width*'*')
    
def download_audio(audio_url):
    resp = requests.get(audio_url)
    download_to = local_source_audio
    if resp.status_code==200:
        with open(download_to, "wb") as fh:
            fh.write(resp.content)
    output = subprocess.check_output(["file", local_source_audio ])
    print( str(output, "utf-8") )
    

def transcode_audio():
    print('start transcode_audio()')
    resp = subprocess.check_output([ffmpeg_bin, '-i', local_source_audio, '-vn', '-acodec', 'pcm_s16le', '-ar', '16000', '-y', output_file ])
    print( str(resp, "utf-8") )    
    print( str(subprocess.check_output(["file", output_file ]), "utf-8")  )