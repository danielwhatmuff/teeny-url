import json
import boto3
import os
import time
import sys
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError


redirect_bucket='teenyurl'


def handler(event, context):
    print "Received event: " + json.dumps(event, indent=2)
    if url in event.keys():
        url = event['url']
    else:
        print 'Couldnt find key "url"'
        sys.exit(1)
    if parse_url(url):
        generate_a_url_key(url)
    else:
        print 'URL malformed {}'.format(url)


def parse_url(url):
    val = URLValidator(verify_exists=False)
    try:
        val(url)
    except ValidationError, e:
        return False
    else:
        return True


def generate_a_url_key(url):
    epoch = int(time.time())
    response = client.put_object(
        Bucket=redirect_bucket,
        Key=epoch,
        ACL='public-read',
        Body='',
        ContentType='text/html',
        WebsiteRedirectLocation=url
    )
