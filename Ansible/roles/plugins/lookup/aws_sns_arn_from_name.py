"""
Description: This lookup takes an AWS region and a sns
topic name and returns a matching ARN.
Example Usage:
{{ lookup('aws_sns_arn_from_name', ('eu-west-1', 'sns-name')) }}
"""
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.errors import *
from ansible.plugins.lookup import LookupBase

try:
    import boto
    import boto.sns
except ImportError:
    raise AnsibleError("aws_sns_arn_from_name lookup cannot be run without boto installed")


class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        region = terms[0][0]
        sns_name = terms[0][1]
        conn = boto.sns.connect_to_region(region)
        snss = conn.get_all_topics()
        for sns in snss['ListTopicsResponse']['ListTopicsResult']['Topics']:
            if sns_name in sns['TopicArn']:
                return([sns['TopicArn'].encode('utf-8')])
        return None
