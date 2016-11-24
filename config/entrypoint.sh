#!/bin/sh
set -e

# prepare root ssh folder
if [ ! -d "/root/.ssh/" ]; then
    mkdir -p /root/.ssh/ && chmod 700 /root/.ssh/
fi

# prepare ansible ssh keys
if [ -f "/data/ssh/id_ansible_rsa" ]; then
    cp /data/ssh/id_ansible_rsa /root/.ssh/id_rsa \
    && chmod 600 /root/.ssh/id_rsa
fi

# prepare ansible
if [ -d "/data/ansible/" ]; then
    cp -r /data/ansible /etc/
fi

exec "$@"
