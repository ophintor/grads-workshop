"""
Description: This lookup takes an AWS region and a dhcp options
name and returns a matching dhcp options ID.
Example Usage:
{{ lookup('aws_dhcp_options_id_from_name', ('eu-west-1', 'dhcp-opts1')) }}
"""
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.errors import *
from ansible.plugins.lookup import LookupBase

try:
    import boto
    import boto.vpc
except ImportError:
    raise AnsibleError("aws_dhcp_options_id_from_name lookup cannot be run without boto installed")


class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        region = terms[0][0]
        dhcp_options_name = terms[0][1]
        vpc_conn = boto.vpc.connect_to_region(region)
        filters = {'tag:Name': dhcp_options_name}
        dhcp_opts = vpc_conn.get_all_dhcp_options(filters=filters)
        if dhcp_opts and dhcp_opts[0]:
            return [dhcp_opts[0].id.encode('utf-8')]
        return None
