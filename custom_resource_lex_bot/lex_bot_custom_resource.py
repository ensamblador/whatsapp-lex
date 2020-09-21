from aws_cdk import (
    core, 
    aws_iam as iam,
    aws_lambda as _lambda
)

from aws_cdk.core import CustomResource

import aws_cdk.aws_logs as logs

import aws_cdk.custom_resources as cr

import uuid
import json


class LexBotResource(core.Construct):
    def __init__( self, scope: core.Construct, id: str, f_lambda, bot_locale) -> None:
        super().__init__(scope, id)

        
        on_event = _lambda.Function(self, "ON-EVENT", runtime=_lambda.Runtime.PYTHON_3_6,
                        handler="lex-bot-provider.on_event", timeout=core.Duration.seconds(60),
                        memory_size=256, code=_lambda.Code.asset("./custom_resource_lex_bot/lambda"),
                        description='PROCESA EVENTOS CUSTOM RESOURCE',
                        environment={'LAMBDA_ARN_FULLFILL': f_lambda.function_arn, 'BOT_LOCALE': bot_locale} )


        is_complete = _lambda.Function(self, "IS-COMPLETE", runtime=_lambda.Runtime.PYTHON_3_6,
                        handler="lex-bot-provider.is_complete", timeout=core.Duration.seconds(60),
                        memory_size=256, code=_lambda.Code.asset("./custom_resource_lex_bot/lambda"),
                        description='IS COMPLETE HANDLER')

        on_event.add_to_role_policy(iam.PolicyStatement(actions=["lex:*"],resources=['*']))
        is_complete.add_to_role_policy(iam.PolicyStatement(actions=["lex:*"],resources=['*']))

        my_provider = cr.Provider(self, "ON_EVENT_CUSTOM_RESOURCE_PROVIDER",
                            on_event_handler=on_event,
                            is_complete_handler=is_complete, # optional async "waiter"
                            log_retention=logs.RetentionDays.ONE_DAY)

        CustomResource(self, "lexbotcustom", service_token=my_provider.service_token)
    