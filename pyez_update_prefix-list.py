#!/usr/bin/env python

from netaddr import *
from jinja2 import Template
from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from jnpr.junos.exception import *
from jnpr.junos.op.routes import RouteTable
import yaml

# prepare the Jinja2-template
pl_template = Template('''
policy-options {
    replace:
    prefix-list {{ prefixlist.name }} {
        {%- for prefix in prefixlist.prefixes %}
            {{ prefix }};
        {%- endfor %}
    }
}
''')

def main():
    hosts = [ 'XX.YY.ZZ.EE' ]
    user = 'autobot'
    
    for host in hosts:
        # https://www.juniper.net/techpubs/en_US/junos-pyez1.0/topics/topic-map/junos-pyez-authenticating-users-with-ssh-keys.html
        dev = Device(host=host, user='autobot', ssh_private_key_file='/home/bot/.ssh/id_rsa.pub') # password=password)
        # Open the connection & config
        try:
            print "Opening connnection to:", host
            dev.open()
        except Exception as err:
            print "Cannot connect to device:", err
            return

        dev.timeout = 300

        yaml_plkanet = '''
---
prefixlist:
    name: pl-kanet
    prefixes:'''

        # Getting information through Table/View
        tblrt = RouteTable(dev)

        tblrt.get(table='RI-PPPoE-INET.inet.0', community_name='community-city')
        ip_list = []
        for route_item in tblrt.keys():
            ip_list.append(IPNetwork(route_item))

        # summarize groups of IP subnets and addresses,
        # merging them together where possible to create the smallest possible list of CIDR subnets
        ip_list = cidr_merge(ip_list)

        for route_item in ip_list:
            yaml_plkanet += "\n    - " + str(route_item)

        pl_config = yaml.load(yaml_plkanet)

        dev.bind(cu=Config)
        # Lock the configuration, load changes, commit
        print "Locking the configuration on:", host
        try:
            dev.cu.lock()
        except LockError:
            print "Error: Unable to lock configuration on:", host
            dev.close()
            return
        print "Loading configuration changes on:", host
        try:
            dev.cu.load('''delete policy-options prefix-list pl-kanet''', format='set')
            dev.cu.load(template=pl_template, template_vars=pl_config, format='text')
        except ValueError as err:
            print err.message
        except Exception as err:
            if err.rsp.find('.//ok') is None:
                rpc_msg = err.rsp.findtext('.//error-message')
                print "Unable to load config changes: ", rpc_msg
            print "Unlocking the configuration on:", host
            try:
                dev.cu.unlock()
            except UnlockError:
                print "Error: Unable to unlock configuration on:", host
            dev.close()
            return
        if dev.cu.diff() is None:
            print "configuration is up-to-date"
        else:
            print "configuration differences:", dev.cu.pdiff()
            print "Committing the configuration on:", host
            try:
                dev.cu.commit()
            except CommitError:
                print "Error: Unable to commit configuration on:", host
                print "Unlocking the configuration on:", host
                try:
                    dev.cu.unlock()
                except UnlockError:
                    print "Error: Unable to unlock configuration on:", host
                    dev.close()
                    return
        print "Unlocking the configuration on:", host
        try:
            dev.cu.unlock()
        except UnlockError:
            print "Error: Unable to unlock configuration on:", host
        print "Closing connection to:", host
        dev.close()


if __name__ == "__main__":
    main()



