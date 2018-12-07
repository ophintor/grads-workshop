AWS ENI
=========

Create AWS Elastic Network Interfaces (ENI)

Requirements
------------

boto will be required for this role

Role Variables
--------------

A dictionary (aws_network_enis) should be presented to this role, with the following keys:

  description
  private_ip
  security_groups
  subnet_id

security_groups should be a list of security groups.

Dependencies
------------

There are no dependencies for this role

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: localhost
      vars:
        aws_network_enis:
          description: This is a description of this network interface. This can be ommitted.
          private_ip: 192.168.4.6
          security_groups:
            - sg-12345678
            - sg-34567890
          subnet_id: subnet-12345678
      roles:
         - { role: aws_eni }

License
-------

GPL

Author Information
------------------

Iain M Conochie <iain.conochie@bjss.com>
