import json

from aws_cdk import (
    aws_lambda as _lambda,
    aws_iam as iam,
    aws_s3 as s3,
    aws_dynamodb as ddb,
    core,
)

from aws_cdk.core import Lazy

from cdk_dynamo_table_viewer import TableViewer
from custom_resource_lex_bot.lex_bot_custom_resource import LexBotResource as lexbot

BOT_LANGUAGE = 'es-US' #'en-US'|'en-GB'|'de-DE'|'en-AU'

class WhatsappLexStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # The code that defines your stack goes here
        fullfillment_lambda = _lambda.Function(
            self,
            "FULLFILMENT",
            runtime=_lambda.Runtime.PYTHON_3_6,
            handler="lambda_handler.main",
            timeout=core.Duration.seconds(20),
            memory_size=256,
            code=_lambda.Code.asset("./lambda/fulfillment"),
            description="Procesa la completación del Intent",
        )

        fullfillment_lambda.add_permission('default',
        principal=iam.ServicePrincipal('lex.amazonaws.com'),action="lambda:invokeFunction",
        source_arn="arn:aws:lex:{}:{}:intent:*".format(self.region, self.account) )

        
        appointments_table = ddb.Table(
            self, "AGENDAMIENTOS",
            partition_key=ddb.Attribute(name="user_phone", type=ddb.AttributeType.STRING),
            sort_key=ddb.Attribute(name="request_time", type=ddb.AttributeType.STRING))

        appointments_table.grant_full_access(fullfillment_lambda)
        fullfillment_lambda.add_environment("APPOINTMENTS_TABLE", appointments_table.table_name)

        TableViewer(
            self, 'ViewHitCounter',
            title='Citas Realizadas vía Whatsapp',
            table=appointments_table
        ) 
        

        _lexbot = lexbot(self,"appointments-bot",f_lambda=fullfillment_lambda, bot_locale=BOT_LANGUAGE)

        #core.CfnOutput(self,"LambdaARN",description="ARN de la funcion lambda de fulfillment",value=fullfillment_lambda.function_arn)
