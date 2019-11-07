import pystache
from urllib.parse import unquote_plus

def handler(event, context):
  print(event)
  
  params = event['queryStringParameters']
  info = { 
    'image' : unquote_plus(params.get('image','')),
    'title' : unquote_plus(params.get('title','')),
    'description' : unquote_plus(params.get('description','')),
    'url' : unquote_plus(params.get('url',''))
  }

  with open('note.mustache', 'r') as f:
    template = f.read()
    html =  pystache.render(template, info)

  return {
        "body": html,
        "statusCode": 200,
        "headers": {"content-type": "text/html"}
    }
