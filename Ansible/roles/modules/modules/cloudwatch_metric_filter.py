#!/usr/bin/python
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['stableinterface'],
                    'supported_by': 'curated'}


DOCUMENTATION = """
module: cloudwatch_metric_filter
short_description: "Create/update AWS Cloudwatch Metric Filters"
description:
 - Can create or update AWS Metric Filters.
version_added: "2.4"
author: "Martinus Nel (@gmail)"
requirements:
    - boto3
    - python >= 2.6
options:
    log_group_name:
      description:
        - The name of the log group.
      required: true
    state:
      description:
        - Whether the rule is present or absent
      choices: ["present", "absent"]
      default: present
      required: true
    filter_name:
      description:
        - A name for the metric filter.
      required: true
    filter_pattern:
      description:
        - A filter pattern for extracting metric data out of ingested log events.
      required: true
    metric_transformations:
      description:
        - A collection of information that defines how metric data gets emitted.
              metricName (string) -- [REQUIRED]
                  The name of the CloudWatch metric.
              metricNamespace (string) -- [REQUIRED]
                  The namespace of the CloudWatch metric.
              metricValue (string) -- [REQUIRED]
                  The value to publish to the CloudWatch metric when a filter pattern matches a log event.
              defaultValue (float) --
                  (Optional) The value to emit when a filter pattern does not match a log event. This value can be null.
      required: true

extends_documentation_fragment:
    - aws
"""

EXAMPLES = '''
  - name: create metric filter
    put_metric_filter:
      region: ap-southeast-2
      log_group_name: "/var/log/audit"
      filter_name: "var_log_audit_error"
      filter_pattern: "error"
      metric_transformations: {'metric_name':'error', 'metric_namespace':'MyMetrics', 'metric_value':'1'}

'''

try:
    import boto3
    HAS_BOTO3 = True
except ImportError:
    HAS_BOTO3 = False
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.ec2 import boto3_conn, ec2_argument_spec, get_aws_connection_info
from boto.exception import BotoServerError, NoAuthHandlerFound

def create_metric_filter(connection, module):

    log_group_name = module.params.get('log_group_name')
    filter_name = module.params.get('filter_name')
    filter_pattern = module.params.get('filter_pattern')
    metric_transformations = module.params.get('metric_transformations')

    try:
        connection.put_metric_filter(
            logGroupName=log_group_name,
            filterName=filter_name,
            filterPattern=filter_pattern,
            metricTransformations=metric_transformations
        )
        module.exit_json(msg="Create Metric Filter operation complete.",changed=True)
    except BotoServerError as e:
        module.fail_json(msg=str(e))

def delete_metric_filter(connection, module):
    log_group_name = module.params.get('log_group_name')
    filter_name = module.params.get('filter_name')

    filters = connection.describe_metric_filters(
                  logGroupName=log_group_name,
                  filterNamePrefix=filter_name
              )
    if filters:
        try:
            connection.delete_metric_filter(
                logGroupName=log_group_name,
                filterName=filter_name
            )
            module.exit_json(changed=True)
        except BotoServerError as e:
            module.fail_json(msg=str(e))
    else:
        module.exit_json(changed=False)


def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(
        dict(
            log_group_name=dict(required=True, type='str'),
            filter_name=dict(required=True, type='str'),
            filter_pattern=dict(required=True, type='str'),
            metric_transformations=dict(required=True, type='list'),
            state=dict(default='present', choices=['present', 'absent']),
            )
    )

    module = AnsibleModule(argument_spec=argument_spec)

    if not HAS_BOTO3:
        module.fail_json(msg='boto3 required for this module')

    state = module.params.get('state')

    region, ec2_url, aws_connect_kwargs = get_aws_connection_info(module, boto3=True)
    if region:
        connection = boto3_conn(module, conn_type='client', resource='logs', region=region, endpoint=ec2_url, **aws_connect_kwargs)
    else:
        module.fail_json(msg="region must be specified")

    if state == 'present':
        create_metric_filter(connection, module)
    elif state == 'absent':
        delete_metric_filter(connection, module)

if __name__ == '__main__':
    main()
