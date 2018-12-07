aws-elb
=========

Create AWS Elastic Load Balancers

Requirements
------------

Boto is required to run this role. This role can only create load balancers with 1 listener

Role Variables
--------------

At a minimum, you should pass in a list names aws_elb detailed in the example playbook:

Dependencies
------------

There are no external dependencies in for this role

Example Playbook
----------------

    - hosts: localhost
      vars:
        my_aws_elb:
          - name: ELB-name
            subnets:
              - subnet-a
              - subnet-b
            instance_port: 8129
            scheme: internal
            sg_names:
              - sg-name-1
              - sg-name-2
            tags:
              Name: ELB-name
      roles: { - role: aws_elb, aws_elb: "{{ my_aws_elb }}" }

License
-------

BSD

Author Information
------------------

Iain M. Conochie <iain.conochie@bjss.com>
