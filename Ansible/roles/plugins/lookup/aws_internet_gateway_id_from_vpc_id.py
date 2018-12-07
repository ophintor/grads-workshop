"""
Description: This lookup takes an AWS region and a vpc id
and returns a matching internet gateway.
Example Usage:
{{ lookup('aws_internet_gateway_id_from_vpc_id', ('eu-west-1', 'vpc-503cefg')) }}
"""
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.errors import *
from ansible.plugins.lookup import LookupBase

try:
    import boto
    import boto.vpc
except ImportError:
    raise AnsibleError("aws_internet_gateway_id_from_vpc_id lookup cannot be run without boto installed")


class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        region = terms[0][0]
        vpc_id = terms[0][1]
        vpc_conn = boto.vpc.connect_to_region(region)
        filters = {'attachment.vpc-id': vpc_id}
        internet_gateway = vpc_conn.get_all_internet_gateways(filters=filters)
        if internet_gateway and internet_gateway[0]:
            return [internet_gateway[0].id.encode('utf-8')]
        return None
