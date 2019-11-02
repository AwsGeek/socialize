
# Skamokawa

A simple serverless back-end to dynamically generate social media friendly HTML wrappers for @awsgeek notes that uses only AWS Lambda, Amazon API Gateway & Amazon DynamoDB

Example DynamoDB table entry:
```
{
  "author": "<a href=\"https://twitter.com/awsgeek\">@awsgeek</a> (Jerry Hargrove)",
  "event": "2019 AWS Summit (Bahrain)",
  "id": "AWS-Summit-2019-Bahrain-AWS-Compute-and-Storage-Fundamentals",
  "image": "https://www.awsgeek.com/images/AWS-Summit-2019-Bahrain-AWS-Compute-and-Storage-Fundamentals.jpg",
  "link": "https://www.awsgeek.com/notes/AWS-Summit-2019-Bahrain-AWS-Compute-and-Storage-Fundamentals",
  "session": "AWS Compute and Storage Fundamentals",
  "title": "2019 AWS Summit (Bahrain) - AWS Compute and Storage Fundamentals"
}
```

Referenced like this via API Gateway:
```
https://m8zzwx390d.execute-api.us-west-2.amazonaws.com/prod/notes/AWS-Summit-2019-Bahrain-AWS-Compute-and-Storage-Fundamentals
```
(replace with your API Gateway details)

I use this on awsgeek.com as a Cloudfront custom origin that maps "/prod" to "notes/*". In "CDK speak":
```
api_config = aws_cloudfront.SourceConfiguration(
    behaviors = [aws_cloudfront.Behavior(path_pattern = 'notes/*')], 
    custom_origin_source = api_origin,
    origin_path = "/prod")
```
