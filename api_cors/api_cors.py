from aws_cdk import (core, aws_lambda as _lambda, aws_apigateway as _apigw)


class api_cors_lambda(core.Construct):
    def __init__(self, scope: core.Construct, id: str, base_lambda, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        base_api = _apigw.RestApi(self,'ApiGatewayWithCors',rest_api_name='api')
        resource = base_api.root.add_resource('twilio')

        resource_lambda_integration = _apigw.LambdaIntegration(
            base_lambda,
            proxy=True,
            integration_responses=[{
                'statusCode': '200',
                'responseParameters': {
                    'method.response.header.Access-Control-Allow-Origin': "'*'"
                }
            }])

        resource.add_method(
            'POST',
            resource_lambda_integration,
            method_responses=[{
                'statusCode': '200',
                'responseParameters': {
                    'method.response.header.Access-Control-Allow-Origin': True,
                }
            }])

        self.add_cors_options(resource)

    def add_cors_options(self, apigw_resource):
        apigw_resource.add_method(
            'OPTIONS',
            _apigw.MockIntegration(integration_responses=[{
                'statusCode': '200',
                'responseParameters': {
                    'method.response.header.Access-Control-Allow-Headers':
                    "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'",
                    'method.response.header.Access-Control-Allow-Origin':
                    "'*'",
                    'method.response.header.Access-Control-Allow-Methods':
                    "'GET,OPTIONS'"
                }
            }],
                                   passthrough_behavior=_apigw.
                                   PassthroughBehavior.WHEN_NO_MATCH,
                                   request_templates={
                                       "application/json":
                                       "{\"statusCode\":200}"
                                   }),
            method_responses=[{
                'statusCode': '200',
                'responseParameters': {
                    'method.response.header.Access-Control-Allow-Headers':
                    True,
                    'method.response.header.Access-Control-Allow-Methods':
                    True,
                    'method.response.header.Access-Control-Allow-Origin': True,
                }
            }],
        )
