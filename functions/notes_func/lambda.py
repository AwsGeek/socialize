import os
import json
import boto3
import datetime
import pystache

ddb = boto3.resource('dynamodb')
table = ddb.Table(os.environ['NOTES_TABLE'])

def handler(event, context):

  html = ""
  try:
      response = table.get_item(
          Key={ 'id': event['id'] }
      )
  except Exception as e:
      print(e)
  else:
      note = response['Item']

      with open('note.mustache', 'r') as f:
        template = f.read()
        html =  pystache.render(template, note)

  return html