#%%
import boto3
client = boto3.client('lex-runtime')
# %%
response = client.post_text(
    botName='ScheduleAppointment_esUS_A',
    botAlias='$LATEST',
    userId='123495',
    inputText='Hola'
)
# %%
response['message']
# %%
response = client.post_content(
    botName='ScheduleAppointment_esUS_A',
    botAlias='$LATEST',
    userId='123495',
    accept='text/plain; charset=utf-8',
    contentType='audio/x-l16; sample-rate=16000; channel-count=1',
    inputStream="https://api.twilio.com/2010-04-01/Accounts/AC59ca71b8460163a870250ec8d4c1c7fc/Messages/MM0d53027ca469f9a2d46bbf45e37e32f1/Media/MEbf7c97c8309e2cf8ac0e992e093a5f40"
)
# %%
response
# %%
