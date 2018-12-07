"""
Description: This lookup takes an AWS region and returns a list of
available availability zones for that region.
Example Usage:
{{ lookup('aws_available_azs_by_region', 'eu-west-1') }}
"""
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os
import codecs

from ansible.errors import *
from ansible.plugins.lookup import LookupBase
import inspect

try:
    import boto
    import boto.ec2
except ImportError:
    raise AnsibleError("aws_available_azs_by_region lookup cannot be run without boto installed")

class LookupModule(LookupBase):

    def run(self, terms, variables=None, **kwargs):
        az_list = []
        region = terms[0]
        conn = boto.ec2.connect_to_region(region)
        filters = {
            'region-name': region,
            'state': 'available'
        }
        zones = conn.get_all_zones(filters=filters)
        for zone in zones:
            az_list.append(zone.name)

        return az_list
