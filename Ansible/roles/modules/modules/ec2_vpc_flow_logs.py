#!/usr/bin/python

DOCUMENTATION = '''
---
module: ec2_vpc_flow_logs
short_description: Manage VPC flow logs
description:
    - Manage flow logs on VPCs, Subnets or Network Interfaces
version_added: 2.3
author: Dave Kirk <david.kirk@bjss.com>
requirements: [ botocore, boto3 ]
notes:
    - You can only create 2 VPC flow logs per resource ID. This is an AWS
      limit rather than a limitation of the module but currently the module
      does not check the number of flow logs on the provided resource ID so
      will error if you break this limit
options:
    resource_id:
        description:
            - The resource to add the flow logs to
        required: true
        default: null
    resource_type:
        description:
            - The resource type you're adding the flow logs to
        required: true
        default: null
        choices: [ 'VPC', 'Subnet', 'NetworkInterface' ]
    traffic_type:
        description:
            - The traffic type to log
        required: true
        default: null
        choices: [ 'ALL', 'ACCEPT', 'REJECT' ]
    log_group_name:
        description:
            - The CloudWatch Log Group logs will be sent to
        required: true
        default: null
    iam_role_arn:
        description:
            - The ARN of the IAM role with permissions to post logs to the
              CloudWatch Log Group
        required: true
        default: null
    state:
        description:
            - Create or Remove the flow logs
        required: false
        default: present
        choices: [ 'present', 'absent' ]
'''

EXAMPLES = '''
    # add flow logs to vpc
    ec2_vpc_flow_logs:
        resource_id: vpc-12ac836d
        state: present
        resource_type: VPC
        traffic_type: REJECT
        log_group_name: MY-CLOUDWATCH-LOG-GROUP
        iam_role_arn: arn:aws:iam::<account_id>:role/<role_name>
        region: eu-west-2

    # remove flow logs from a subnet
    ec2_vpc_flow_logs:
        resource_id: subnet-12ac836d
        state: absent
        resource_type: Subnet
        traffic_type: REJECT
        log_group_name: MY-CLOUDWATCH-LOG-GROUP
        iam_role_arn: arn:aws:iam::<account_id>:role/<role_name>
'''

try:
    from botocore.exceptions import ClientError
    HAS_BOTOCORE = True
except ImportError:
    HAS_BOTOCORE = False

try:
    import boto3
    HAS_BOTO3 = True
except ImportError:
    HAS_BOTO3 = False

import json
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.ec2 import (boto3_conn, camel_dict_to_snake_dict,
        ec2_argument_spec, get_aws_connection_info)

class Ec2VpcFlowLogsManager:
    def __init__(self, module):
        self.module = module
        try:
            region, ec2_url, aws_connect_kwargs = \
                    get_aws_connection_info(module, boto3=True)
            if not region:
                module.fail_json(msg="Region not provided.")
            self.ec2 = boto3_conn(module,
                                  conn_type='client',
                                  resource='ec2',
                                  region=region,
                                  endpoint=ec2_url,
                                  **aws_connect_kwargs)
        except ClientError as e:
            module.fail_json(msg=e.message)

    def describe_vpc_flow_logs(self,
                               resource_id,
                               traffic_type,
                               log_group_name):
        response = self.ec2.describe_flow_logs(
            Filters=[
                {
                    'Name': 'resource-id',
                    'Values': [
                        resource_id
                    ]
                },
                {
                    'Name': 'traffic-type',
                    'Values': [
                        traffic_type
                    ]
                },
                {
                    'Name': 'log-group-name',
                    'Values': [
                        log_group_name
                    ]
                }
            ]
        )

        return response

    def ensure_vpc_flow_logs_present(self, resource_id, resource_type,
                                     traffic_type, log_group_name, iam_role_arn):
        response = self.ec2.create_flow_logs(
            ResourceIds=[resource_id],
            ResourceType=resource_type,
            TrafficType=traffic_type,
            LogGroupName=log_group_name,
            DeliverLogsPermissionArn=iam_role_arn
        )

        return response

    def ensure_vpc_flow_logs_absent(self, flow_log_id):
        response = self.ec2.delete_flow_logs(FlowLogIds=[flow_log_id])

        return response


def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(
        dict(
            resource_id=dict(required=True, type='str'),
            resource_type=dict(required=True, choices=['VPC', 'Subnet', 'NetworkInterface']),
            traffic_type=dict(required=True, choices=['ACCEPT', 'REJECT', 'ALL']),
            log_group_name=dict(required=True, type='str'),
            iam_role_arn=dict(required=True, type='str'),
            state=dict(default='present', choices=['present', 'absent']),
        )
    )
    module = AnsibleModule(argument_spec=argument_spec,
                           supports_check_mode=True)

    if not HAS_BOTOCORE:
        module.fail_json(msg="botocore is required.")

    if not HAS_BOTO3:
        module.fail_json(msg="boto3 is required.")

    manager = Ec2VpcFlowLogsManager(module)

    existing = manager.describe_vpc_flow_logs(
        resource_id = module.params['resource_id'],
        traffic_type = module.params['traffic_type'],
        log_group_name = module.params['log_group_name']
    )
    results = dict(changed=False)

    if module.params['state'] == 'present':
        if existing['FlowLogs']:
           results['flow_logs'] = existing['FlowLogs']
        else:
            if not module.check_mode:
                create = manager.ensure_vpc_flow_logs_present(
                    module.params['resource_id'],
                    module.params['resource_type'],
                    module.params['traffic_type'],
                    module.params['log_group_name'],
                    module.params['iam_role_arn'],
                )

                if create['FlowLogIds']:
                    flow_log_id = create['FlowLogIds'][0]
                    existing = manager.describe_vpc_flow_logs(
                        resource_id = module.params['resource_id'],
                        traffic_type = module.params['traffic_type'],
                        log_group_name = module.params['log_group_name']
                    )
                    if existing['FlowLogs']:
                        results['flow_logs'] = existing['FlowLogs']

                results['changed'] = True
    elif module.params['state'] == 'absent':
        if existing['FlowLogs']:
            if not module.check_mode:
                results['flow_logs'] = manager.ensure_vpc_flow_logs_absent(
                                         existing['FlowLogs'][0]['FlowLogId'])
                results['changed'] = True

    pretty_results = camel_dict_to_snake_dict(results)
    module.exit_json(**pretty_results)

if __name__ == '__main__':
    main()
