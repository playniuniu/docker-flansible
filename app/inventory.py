#!/usr/bin/env python
import argparse
import csv
import json


class DynamicInventory(object):

    def __init__(self):
        self.inventory = {}
        self.read_cli_args()

        # Called with `--list`.
        if self.args.list:
            self.inventory = self.dynamic_inventory()
        # Called with `--host [hostname]`.
        elif self.args.host:
            # Not implemented, since we return _meta info `--list`.
            self.inventory = self.empty_inventory()
        # If no groups or vars are present, return empty inventory.
        else:
            self.inventory = self.empty_inventory()

        print(json.dumps(self.inventory))

    # Example inventory for testing.
    def dynamic_inventory(self):

        with open('/etc/ansible/hosts.csv', 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            csv_hosts = []
            csv_hostvar = {}

            for row in reader:
                csv_hosts.append(row['ip'])
                csv_hostvar[row['ip']] = {
                    'ansible_user': row['user'],
                    'ansible_ssh_pass': row['passwd']
                }

            return {
                'group': {
                    'hosts': csv_hosts,
                },
                '_meta': {
                    'hostvars': csv_hostvar
                }
            }

    # Empty inventory for testing.
    def empty_inventory(self):
        return {'_meta': {'hostvars': {}}}

    # Read the command line args passed to the script.
    def read_cli_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--list', action='store_true')
        parser.add_argument('--host', action='store')
        self.args = parser.parse_args()


if __name__ == '__main__':
    DynamicInventory()
