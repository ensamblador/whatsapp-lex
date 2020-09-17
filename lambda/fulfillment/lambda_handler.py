import logging
import json
import os
import random
import boto3
import datetime


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

ddb = boto3.resource('dynamodb')
table = ddb.Table(os.environ["APPOINTMENTS_TABLE"])

def close(session_attributes, fulfillment_state, message):
    response = {
        "sessionAttributes": session_attributes,
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": fulfillment_state,
            "message": message,
        },
    }

    return response


def dispatch(appointment, session_attributes):
    resultado = "Su hora de {} con {} ha sido confirmada para {} a las {}\n\nDireccion: Andres Bello 1192 {}, Providencia".format(
        appointment["C_Tipo"],
        appointment["C_Esp"],
        appointment["C_Fecha"],
        appointment["C_Hora"],
        appointment["C_Ubi"]
    )

    return close (
        session_attributes,
        "Fulfilled",
        {"contentType": "PlainText", "content": resultado},
    )


def make_appointment(appointmen_info):
    doctores = ["Doctor Brown", "Doctora Rodríguez", "Doctora Fuentes", "Doctor Geller"]
    oficinas = ["Piso 5", "Piso 3", "Piso 9", "Piso 2"]
    appointmen_info["C_Esp"] = random.choice(doctores)
    appointmen_info["C_Ubi"] = random.choice(oficinas)
    return appointmen_info


def save_appointment(event):

    request_time = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")

    request_attributes = event["requestAttributes"]

    user_id = event["userId"].split(":")
    target_id = request_attributes["x-amz-lex:twilio-target-phone-number"].split(":")

    target_phone = target_id[1]
    target_channel = target_id[0]

    user_channel = user_id[0]
    user_phone = user_id[1]

    bot = event["bot"]

    appointment_type = event["currentIntent"]["slots"]["AppointmentType"]
    appointment_date = event["currentIntent"]["slots"]["Date"]
    appointment_time = event["currentIntent"]["slots"]["Time"]
    intent_name = event["currentIntent"]["name"]
    sentiment = event["sentimentResponse"]["sentimentLabel"]

    appointment_info = {
        "request_time": request_time,
        #"user_channel": user_channel,
        "user_phone": user_phone,
        #"target_channel": target_channel,
        #"target_phone": target_phone,
        #"bot": bot,
        #"intent_name": intent_name,
        "C_Tipo": appointment_type,
        "C_Fecha": appointment_date,
        "C_Hora": appointment_time,
        #"sentiment": sentiment,
    }

    appointment_info = make_appointment(appointment_info)
    save_item_ddb(appointment_info)
    return appointment_info


def save_item_ddb(item):
    response = table.put_item(Item=item)
    return response


def main(event, context):
    logger.info("## ENVIRONMENT VARIABLES\r" + json.dumps(dict(**os.environ)))
    logger.info(event)
    appointment_info = save_appointment(event)
    return dispatch(appointment_info, event['sessionAttributes'])
