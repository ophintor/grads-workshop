#!/bin/bash
set -eux

# Bring system up to date
yum update -y

# Configure Jenkins RPM repository and Jenkins
wget -O /etc/yum.repos.d/jenkins.repo https://pkg.jenkins.io/redhat/jenkins.repo
rpm --import https://pkg.jenkins.io/redhat/jenkins.io.key
yum install -y java-1.8.0-openjdk-devel jenkins git jq

# Add jenkins group to list of sudoers
echo -e '\n## Provision script additions\njenkins ALL=(ALL) NOPASSWD:ALL' | sudo EDITOR='tee -a' visudo

# Start services and reboot
service jenkins start
chkconfig jenkins on
