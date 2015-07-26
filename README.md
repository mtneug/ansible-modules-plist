# Ansible Module for plists
This is an [Ansible](http://www.ansible.com/) module for creating and manipulating [plists](https://developer.apple.com/library/mac/documentation/Darwin/Reference/ManPages/man5/plist.5.html).

## Install
To install this module copy the `library` folder to the location of your playlist or role. The script makes use of [biplist](https://github.com/wooster/biplist) so make sure to install it on the targeted system.

```yaml
- name: Install pip
  easy_install: name=pip
  sudo: yes

- name: Install python module dependencies
  pip: name=biplist
  sudo: yes
```

## Usage
The module takes three arguments:
- `dest` (Required): Either the absolute path of the plist, or a domain/filename which will be searched for in `~/Library/Preferences/<domain>.plist`
- `key` (Optional): The key of write the value to. If not given it is written to the root node.
- `value` (Required): The value to write. It may be a `string`, `int`, `float`, `boolean`, `array` or `dictionary`. Nested dictionaries are allowed and are inclusive, i.e. nested keys that are only present in the current plist file will not be deleted.

This module supports [check mode](http://docs.ansible.com/ansible/playbooks_checkmode.html).

## Example

```yaml
- name: example 1
  plist_file:
    dest: /tmp/example.plist
    key: myString
    value: myValue

- name: Change Dock settings
  plist_file:
    dest: com.apple.dock
    value:
      # One of left, bottom, right
      orientation: left

      # Mission Control animation speed
      expose-animation-duration: 0.1
```

## Limitations
- The `date` and `data` types are not supported.

## Tests
A simple test can be run with:

```sh
$ cd test
$ ./run.sh
```

## License
This module is released under the [MIT License](https://github.com/mtneug/ansible-modules-plist/blob/master/LICENSE.md).
