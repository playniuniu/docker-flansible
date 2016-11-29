#!/usr/bin/env python
import argparse
import csv
import json
from collections import defaultdict


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

    def dynamic_inventory(self):
        '''
        CSV format is:

        -----------------------
        ip, user, passwd, group
        -----------------------

        Inventory format is:

        -----------------------
        'group1': { hosts: [ip1, ip2, ip3 ] },
        'group2': { hosts: [ip4, ip5, ip6 ] },
        '_meta': {
            "hostvars": {
                'ip1': {
                    ansible_user = xxx
                    ansible_ssh_pass = xxx
                },
                'ip2': {
                    ansible_user = xxx
                    ansible_ssh_pass = xxx
                }
            }
        }
        -----------------------
        '''

        with open('/etc/ansible/hosts.csv', 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            csv_hostvar = {}
            csv_group = defaultdict(list)

            for row in reader:
                # csv_hosts.append(row['ip'])
                ip = row['ip']
                group = row['group']

                csv_hostvar[ip] = {
                    'ansible_user': row['user'],
                    'ansible_ssh_pass': row['passwd']
                }

                csv_group[group].append(row['ip'])

            res = defaultdict(dict)

            for key in csv_group:
                res[key]['hosts'] = csv_group[key]

            res['_meta'] = {'hostvars': csv_hostvar}

            return res

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
