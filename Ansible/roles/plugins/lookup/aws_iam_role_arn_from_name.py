"""
Description: This lookup takes an AWS region and an IAM
Role name and returns the Role ARN.
Example Usage:
{{ lookup('aws_iam_role_arn_from_name', ('eu-west-1', 'role-name')) }}
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
    import boto.iam
except ImportError:
    raise AnsibleError("aws_iam_role_arn_from_name lookup cannot be run without boto installed")


class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        region = terms[0][0]
        role_name = terms[0][1]
        conn = boto.iam.connect_to_region(region)
        role = conn.get_role(role_name=role_name).get_role_response.get_role_result.role.arn
        if role:
            return [role.encode('utf-8')]
        return None
