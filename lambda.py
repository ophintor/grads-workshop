import json
import boto3

def lambda_handler(event, context):
   
   message = json.loads(event["Message"])
   key = message["Records"][0]["s3"]["object"]["key"]
   
   s3 = boto3.resource('s3')
   copy_source = {
       'Bucket': 'alastair-bucket-source',
       'Key': key
   }
   s3.meta.client.copy(copy_source, 'alastair-bucket-destination', 'key')
   
   
   
   
   
   
