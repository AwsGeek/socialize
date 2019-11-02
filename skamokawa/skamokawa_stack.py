from aws_cdk import (
    core,
    aws_lambda,
    aws_dynamodb,
    aws_apigateway
)
import os, json

class SkamokawaStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        notes_config = {
            'title': 'Jerry Hargrove',
            'tagline': 'Cloud Diagrams & Notes',
            'twitter': 'awsgeek',
            'google_analytics': 'UA-106486526-1'}

        notes_table = aws_dynamodb.Table(self, 'notes_table',
          partition_key = { 'name': 'id', 'type': aws_dynamodb.AttributeType.STRING },
          billing_mode = aws_dynamodb.BillingMode.PAY_PER_REQUEST)

        boto_layer = aws_lambda.LayerVersion(self, 'boto_layer',
            code = aws_lambda.AssetCode('layers/boto_layer'),
            compatible_runtimes = [aws_lambda.Runtime.PYTHON_3_7])

        pystache_layer = aws_lambda.LayerVersion(self, 'pystache_layer',
            code = aws_lambda.AssetCode('layers/pystache_layer'),
            compatible_runtimes = [aws_lambda.Runtime.PYTHON_3_7])

        # Dynamically generate HTML for images
        notes_func = aws_lambda.Function(self, "notes_func",
            code = aws_lambda.AssetCode('functions/notes_func'),
            handler = "lambda.handler",
            layers = [boto_layer, pystache_layer],
            runtime = aws_lambda.Runtime.PYTHON_3_7,
            environment = {
                'NOTES_TABLE': notes_table.table_name})

        notes_table.grant_read_data(notes_func)

        # Uses API Gateway as the endpoint
        notes_api = aws_apigateway.LambdaRestApi(self, 'notes_api',
            handler = notes_func,
            proxy = False)

        # Only GETs are supported
        notes_resource = notes_api.root.add_resource('notes')
        id_resource = notes_resource.add_resource('{id}')
        id_resource.add_method('GET',
            aws_apigateway.LambdaIntegration(notes_func, proxy = False,
                request_templates =  { 'application/json': json.dumps({"id": "$input.params('id')"}) },
                passthrough_behavior = aws_apigateway.PassthroughBehavior.WHEN_NO_TEMPLATES,
                integration_responses = [aws_apigateway.IntegrationResponse(
                    status_code = "200",
                    response_templates = {'application/json': '$input.path("$")'}
                )]
            )
            ,
            method_responses = [aws_apigateway.MethodResponse(
                status_code = '200',
                response_models = {
                    'text/html': aws_apigateway.Model.EMPTY_MODEL
                })
            ]
        )