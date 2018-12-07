from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

from ansible.errors import *
from ansible.plugins.lookup import LookupBase

try:
    import boto3
    import botocore
except ImportError:
    raise AnsibleError("aws_tg_arn_from_name requires boto3 to be installed")


class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        if isinstance(terms, basestring):
            terms = [terms]
        region = terms[0][0]
        tg_name = []
        tg_name.append(terms[0][1])
        session = boto3.session.Session(region_name=region)
        try:
            elbv2_client = session.client('elbv2')
        except botocore.exception.NoRegionError:
            raise AnsibleError("AWS region not provided")

        result = elbv2_client.describe_target_groups(Names=tg_name)
        the_tg = result.get('TargetGroups')

        return [the_tg[0].get('TargetGroupArn').encode('utf-8')]
