from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

from ansible.errors import *
from ansible.plugins.lookup import LookupBase

try:
    import boto3
    import botocore
except ImportError:
    raise AnsibleError("aws_lambda_arn_from_name requires boto3 to be installed")


class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        if isinstance(terms, basestring):
            terms = [terms]
        lambda_name = ''
        region = terms[0][0]
        lambda_name = terms[0][1]
        session = boto3.session.Session(region_name=region)
        try:
            lambda_client = session.client('lambda')
        except botocore.exception.NoRegionError:
            raise AnsibleError("AWS region not provided")

        result = lambda_client.get_function(FunctionName=lambda_name)
        the_lambda = result.get('Configuration')

        return [the_lambda.get('FunctionArn').encode('utf-8')]
