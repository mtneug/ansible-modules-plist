#!/usr/bin/python
#
# (c) 2015, Matthias Neugebauer

DOCUMENTATION = '''
---
module: plist_file
author: Matthias Neugebauer
short_description:  Manage settings in plist files
description:
     - Manage settings in plist files.
options:
  dest:
    description:
      - Domain or absolut path to the plist file; file will be created if required.
    required: true
    default: null
  key:
    description:
      - Key to manage.
    required: true
    default: null
  value:
    description:
     - Value which sould be set.
    required: true
    default: null
  type:
    description:
     - Type of the key.
    required: false
    default: string
    choices: [ string, data, int, float, bool, date, array, dict, dict-add ]
'''

EXAMPLES = '''
plist_file:
  dest: /tmp/ansible.modules.plist.test.plist
  key: testString
  value: myString
  type: string

plist_file:
  dest: ansible.modules.plist.test
  key: testInt
  value: 7
  type: int
'''

import subprocess

def do_plist(module, filename, key, value, type = 'string'):
    # read old value
    p = subprocess.Popen(['defaults', 'read', filename, key],
                         stdout=subprocess.PIPE)
    old_value = p.communicate()[0]

    # write new value
    if isinstance(value, list):
        value_list = [str(e) for e in value]
    elif isinstance(value, dict):
        value_list = list(reduce(lambda k, v: k + v, value.items()))
        value_list = [str(e) for e in value_list]
    else:
        value_list = [str(value)]

    p = subprocess.Popen(['defaults', 'write', filename, key, '-' + type] + value_list,
                         stdout=subprocess.PIPE)
    p.communicate()

    if p.returncode != 0:
        module.fail_json(msg="Can't change %s" % filename)
        return False

    # read new value
    p = subprocess.Popen(['defaults', 'read', filename, key],
                         stdout=subprocess.PIPE)
    new_value = p.communicate()[0]

    return old_value != new_value

def main():
    module = AnsibleModule(
        argument_spec = dict(
            dest  = dict(required=True),
            key   = dict(required=True),
            value = dict(required=True),
            type  = dict(default='string',
                         choices=['string', 'data', 'int', 'float', 'bool', 'date', 'array', 'dict', 'dict-add'])
        )
    )

    if not module.params['dest'].startswith('/'):
        module.params['dest'] = os.path.expanduser("~/Library/Preferences/%s.plist" % module.params['dest'])

    dest  = module.params['dest']
    key   = module.params['key']
    value = module.params['value']
    type  = module.params['type']

    changed = do_plist(module, dest, key, value, type)

    module.exit_json(dest=dest, changed=changed, msg="OK")

from ansible.module_utils.basic import *
main()
