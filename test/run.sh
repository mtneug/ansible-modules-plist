#!/bin/sh
set -e

ansible-playbook test.yml -i hosts -M ../

set +e
defaults read /tmp/ansible.modules.plist.test.plist | /usr/bin/diff - ./ansible.modules.plist.test.content
status=$?
set -e

echo

if [ $status -eq 0 ]; then
  echo "PASSED"
else
  echo "FAILED"
fi

exit $status
