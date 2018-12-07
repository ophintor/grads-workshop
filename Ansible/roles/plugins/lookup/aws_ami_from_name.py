"""
Description: This lookup takes several variables and returns the latest AMI.
Variables required: Region, Owner, Name
Name can be a partial match, as everything to the right of the variable will be matched against a wildcard.
Example Usage:
{{ lookup('aws_ami_from_name', ('region', 'ami_owner', 'name')) }}
{{ lookup('aws_ami_from_name', ('eu-west-2', '123456789', 'low-centos')) }}
"""
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.errors import *
from ansible.plugins.lookup import LookupBase
from ansible.module_utils._text import to_text

try:
    from __main__ import display
except ImportError:
    from ansible.utils.display import Display
    display = Display()

try:
    import boto
    import boto.ec2
except ImportError:
    raise AnsibleError("aws_ami_from_name lookup cannot be run without boto installed")

class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        region = terms[0][0]
        ami_owner = terms[0][1]
        ami_name = terms[0][2]
        conn = boto.ec2.connect_to_region(region)
        
        ami_filters = { 
            'name': '*' + str(ami_name) + '*', 
            'owner-id': ami_owner,
            }

        images = conn.get_all_images(filters=ami_filters) 
        images.sort(key=lambda r: r.creationDate, reverse=True)

        if images:
            # used for debugging if you have a query about what AMIs are being returned
            #print("AMI Lookup found the following AMIs, selecting the first item:")
            #for i in images:
            #    print(i.id + " - " + i.creationDate + " - " + i.name)
            return [images[0].id.encode('utf-8')]
        return None
