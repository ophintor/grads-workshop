"""
Description: This lookup takes an AWS region and a list of one or more
security Group Names and returns a list of matching security Group IDs.
Example Usage:
{{ lookup('aws_sg_ids_from_names', ('eu-west-1', 'vpc-id', ['nginx_group', 'mysql_group'])) }}
"""
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os
import codecs

from ansible.errors import *
from ansible.plugins.lookup import LookupBase

try:
    import boto
    import boto.ec2
    import boto.vpc
except ImportError:
    raise AnsibleError("aws_sg_ids_from_names lookup cannot be run without boto installed")

class LookupModule(LookupBase):

    def run(self, terms, variables=None, **kwargs):
        sg_list = []
        region = terms[0][0]
        vpc_name = terms[0][1]
        group_names = terms[0][2]
        if isinstance(group_names, basestring):
            group_names = [group_names]

        # Lookup VPC ID
        vpc_conn = boto.vpc.connect_to_region(region)
        filters = {
            'tag:Name': vpc_name,
            'state': 'available'
        }
        vpc = None
        vpc = vpc_conn.get_all_vpcs(filters=filters)
        if vpc and vpc[0]:
            vpc_id = [vpc[0].id.encode('utf-8')]
        else:
            pass
            #raise AnsibleError('VPC (' + vpc_name + ') not found')

        if vpc:
            conn = boto.ec2.connect_to_region(region)
            #TODO: Use OR filter rather than making multiple calls
            for group_name in group_names:
                filters = {'group_name': group_name, 'vpc_id': vpc_id }
                try:
                    sg = conn.get_all_security_groups(filters=filters)
                    if sg and sg[0]:
                        sg_list.append(sg[0].id)
                except Exception:
                    pass



        return sg_list
