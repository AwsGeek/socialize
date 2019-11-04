
# Skamokawa

A simple serverless back-end to dynamically generate social media friendly HTML wrappers for @awsgeek notes using AWS Lambda and Amazon API Gateway:

Referenced like this via API Gateway:
```
https://m8zzwx390d.execute-api.us-west-2.amazonaws.com/prod/socialize??image=https%3A%2F%2Fwww.awsgeek.com%2Fimages%2FAWS-Summit-2019-Bahrain-AWS-Compute-and-Storage-Fundamentals.jpg&title=AWS%20Compute%20and%20Storage%20Fundamentals
```
(replace with your API Gateway details and URL encoded parameters)

I use this on awsgeek.com as a Cloudfront custom origin that maps "/prod" to "notes/*". In "CDK speak":
```
api_config = aws_cloudfront.SourceConfiguration(
    behaviors = [aws_cloudfront.Behavior(path_pattern = 'notes/*')], 
    custom_origin_source = api_origin,
    origin_path = "/prod")
```

## To build (this is what I do in a Cloud 9 env):
```
npm install -g aws-cdk
git clone 
cd skamokawa
cd layers/boto_layer/python 
pip install -r requirements.txt -t .
cd ../../layers/pystache_layer/python 
pip install -r requirements.txt -t .
cd ../..
pip install -r requirements.txt
cdk deploy
```
