from aws_cdk import (
    core,
    aws_lambda,
    aws_apigateway
)
import json

class SkamokawaStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        pystache_layer = aws_lambda.LayerVersion(self, 'pystache_layer',
            code = aws_lambda.AssetCode('layers/pystache_layer'),
            compatible_runtimes = [aws_lambda.Runtime.PYTHON_3_7])

        # Dynamically generate HTML for images
        socialize_func = aws_lambda.Function(self, "socialize_func",
            code = aws_lambda.AssetCode('functions/socialize_func'),
            handler = "lambda.handler",
            layers = [pystache_layer],
            runtime = aws_lambda.Runtime.PYTHON_3_7)
            
        # Uses API Gateway as the endpoint
        socialize_api = aws_apigateway.LambdaRestApi(self, 'socialize_api',
            handler = socialize_func,
            proxy = False)

        # Only GETs are supported
        socialize_resource = socialize_api.root.add_resource('socialize')
        socialize_resource.add_method('GET',
            aws_apigateway.LambdaIntegration(socialize_func, proxy = True))