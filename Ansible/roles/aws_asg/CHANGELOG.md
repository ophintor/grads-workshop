# CHANGELOG

## 1.1.0 - Added High Data launch config and allow manual specification of heartbeat in ASG

## 1.0.2 - Allow addition of second static defined interface to instances within an ASG

### Manual Steps Introduced

N/A

### Tasks & Bug Fixes

  * BETA-7971 - Deploy forward proxy for DNS in Internal Connectivity VPC

 The update to this role is to allow the user-data script to attach a pre-defined interface
to an instance within an ASG upon bootup. This pre-defined interface will have a static IP
address assigned, so a DNS record external to route53 can be defined to use the service
on this IP; in this case a squid proxy server.
