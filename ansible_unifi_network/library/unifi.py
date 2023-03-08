#!/usr/bin/python

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = r"""
---
module: my_test
short_description: This is my test module
# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "1.0.0"
description: This is my longer description explaining my test module.
options:
    name:
        description: This is the message to send to the test module.
        required: true
        type: str
    new:
        description:
            - Control to demo if the result of this module is changed or not.
            - Parameter description can be a list as well.
        required: false
        type: bool
# Specify this value according to your collection
# in format of namespace.collection.doc_fragment_name
extends_documentation_fragment:
    - my_namespace.my_collection.my_doc_fragment_name
author:
    - Your Name (@yourGitHubHandle)
"""

EXAMPLES = r"""
# Pass in a message
- name: Test with a message
  my_namespace.my_collection.my_test:
    name: hello world
# pass in a message and have changed true
- name: Test with a message and changed output
  my_namespace.my_collection.my_test:
    name: hello world
    new: true
# fail the module
- name: Test failure of the module
  my_namespace.my_collection.my_test:
    name: fail me
"""

RETURN = r"""
# These are examples of possible return values, and in general should use other names for return values.
original_message:
    description: The original name param that was passed in.
    type: str
    returned: always
    sample: 'hello world'
message:
    description: The output message that the test module generates.
    type: str
    returned: always
    sample: 'goodbye'
"""


def group_present(module_param):
    # seed the result dict in the object
    result = dict(result="")

    result["result"] = module_param["name"]

    return True, result


def group_absent(module_param):
    # seed the result dict in the object
    result = dict(result="")

    result["result"] = module_param["state"]

    return True, result


def main():
    # define parameters for the module
    module_args = dict(
        name=dict(type="str", required=True),
        state=dict(type="str", default="present", choices=["present", "absent"]),
    )
    choice_map = {"present": group_present, "absent": group_absent}

    # AnsibleModule object for abstraction of Ansible
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    # if check mode, return the current state
    if module.check_mode:
        module.exit_json(changed=False)

    # When exception occurs
    if module.params["name"] == "fail":
        module.fail_json(msg="You requested this to fail")

    # Run function based on passed state
    has_changed, result = choice_map.get(module.params["state"])(module.params)

    # Return message as output
    module.exit_json(changed=has_changed, meta=result)


if __name__ == "__main__":
    main()
