from aws_cdk import (
    aws_lambda as _lambda,
    aws_iam as iam,
    aws_s3 as s3,
    aws_dynamodb as ddb,
    core
)

from cdk_dynamo_table_viewer import TableViewer

class WhatsappLexStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # The code that defines your stack goes here
        fullfillment_lambda = _lambda.Function(self, "FULLFILMENT", runtime=_lambda.Runtime.PYTHON_3_6,
                                          handler="lambda_handler.main", timeout=core.Duration.seconds(20),
                                          memory_size=256, code=_lambda.Code.asset("./lambda/fulfillment"),
                                          description='Procesa la completación del Intent')

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