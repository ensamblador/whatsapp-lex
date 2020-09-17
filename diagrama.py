#%%

#https://diagrams.mingrammer.com/docs/guides/diagram

from diagrams import Diagram,Cluster, Edge
from diagrams.aws.ml import Lex
from diagrams.generic.device import Mobile

from diagrams.aws.analytics import KinesisDataFirehose as KFH
from diagrams.aws.analytics import ElasticsearchService as ESS
from diagrams.elastic.elasticsearch import Kibana
from diagrams.aws.general import Users
from diagrams.aws.storage import S3
from diagrams.aws.security import Cognito
from diagrams.aws.analytics import Athena
from diagrams.aws.analytics import GlueCrawlers
from diagrams.aws.analytics import GlueDataCatalog
from diagrams.aws.compute import Lambda 
from diagrams.aws.mobile import APIGatewayEndpoint,APIGateway
from diagrams.onprem.client import Client
from diagrams.aws.database import DynamodbTable,DDB
from diagrams.aws.engagement import SES
from diagrams.aws.integration import SQS

graph_attr = {
    "esep": "+20",
    "fontsize": "45"
}
node_attr = {
       "esep": "+20",
    "fontsize": "10" 
}


with Diagram("Whatsapp-Lex-Appointments", show=True, direction='LR',
            graph_attr=graph_attr, node_attr =node_attr):

    _ddb = DDB('DynamoDB Agendas Solcitadas')
    _lambda = Lambda('Lambda Agendar')
    _lambda << Edge() >> _ddb 

    _device = Mobile('Whatsapp')

    _lex =  Lex('Bot de Agendamiento')
    _device << Edge() >> _lex
    _lex >> Edge(label='Intent') >> _lambda



