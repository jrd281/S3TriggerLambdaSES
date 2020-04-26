import json
import urllib.parse
import boto3
import os
import datetime
import dateutil.tz

s3 = boto3.client('s3')
ses = boto3.client('ses')

# 'US/Eastern'
# https://stackoverflow.com/questions/34906589/import-pytz-into-aws-lambda-function
environ_timezone = dateutil.tz.gettz(os.environ['TIMEZONE'])

# These are environment parameters that have to be set on the lambda
# itself
email_from = os.environ['EMAIL_FROM']
email_to = os.environ['EMAIL_TO']

current_datetime = datetime.datetime.now(tz=environ_timezone)
current_datetime_fmt = current_datetime.strftime("%Y-%m-%d %H:%M")


# https://github.com/thigley986/Lambda-AWS-SES-Send-Email/blob/master/SendEmail.py
def lambda_handler(event, context):
    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    split_object_name = key.rsplit('/', 1)
    object_name = split_object_name and split_object_name[-1]

    if (object_name is None) or (str(object_name).strip() == ""):
        email_subject = 'App S3 Email - ' + current_datetime_fmt
    else:
        email_subject = 'App S3 Email - ' + object_name

    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        # open the file object and read it into the variable filedata.
        file_data = response['Body'].read()

        # file data will be a binary stream.  We have to decode it
        contents = file_data.decode('utf-8')
        # The below line is for debugging
        # print(contents)
        email_body = contents
        email_response = ses.send_email(
            Source=email_from,
            Destination={
                'ToAddresses': [
                    email_to,
                ]
            },
            Message={
                'Subject': {
                    'Data': email_subject
                },
                'Body': {
                    'Text': {
                        'Data': contents
                    }
                }
            }
        )

        return email_response
    except Exception as e:
        print(e)
        print(
            'Error getting object {} from bucket {}. Make sure they exist '
            'and your bucket is in the same region as '
            'this function.'.format(
                key, bucket))
        raise e
