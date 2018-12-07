"""
Description: This lookup takes an AWS region and a auto
scaling group name and returns a matching ID.
Example Usage:
{{ lookup('aws_asg_id_from_name', ('eu-west-1', 'asg-name')) }}
"""
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.errors import *
from ansible.plugins.lookup import LookupBase

try:
    import boto
    import boto.ec2.autoscale
except ImportError:
    raise AnsibleError("aws_asg_id_from_name lookup cannot be run without boto installed")


class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        region = terms[0][0]
        asg_name = terms[0][1]
        conn = boto.ec2.autoscale.connect_to_region(region)
        asgs = conn.get_all_groups(names=[asg_name])
        if asgs and asgs[0]:
            return [asgs[0]]
        return None
