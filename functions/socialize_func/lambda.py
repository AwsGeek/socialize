import pystache
from urllib.parse import unquote, unquote_plus

def handler(event, context):
  print(event)
  
  params = event['queryStringParameters']
  info = { 
    'image' : unquote(params['image']) 
  }
  if 'title' in params:
    info['title'] = unquote_plus(unquote(params['title']))
    
  if 'description' in params:
    info['description'] = unquote_plus(unquote(params['description']))

  if 'url' in params:
    info['url'] = unquote_plus(unquote(params['url']))
  
  with open('note.mustache', 'r') as f:
    template = f.read()
    html =  pystache.render(template, info)

  return {
        "body": html,
        "statusCode": 200,
        "headers": {"content-type": "text/html"}
    }