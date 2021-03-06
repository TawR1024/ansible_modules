#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2018, Mikhail Yohman (@FragmentedPacket) <mikhail.yohman@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

ANSIBLE_METADATA = {
    "metadata_version": "1.1",
    "status": ["preview"],
    "supported_by": "community",
}

DOCUMENTATION = r"""
---
module: netbox_rack
short_description: Create, update or delete racks within Netbox
description:
  - Creates, updates or removes racks from Netbox
notes:
  - Tags should be defined as a YAML list
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Mikhail Yohman (@FragmentedPacket)
requirements:
  - pynetbox
version_added: '0.1.0'
options:
  netbox_url:
    description:
      - URL of the Netbox instance resolvable by Ansible control host
    required: true
  netbox_token:
    description:
      - The token created within Netbox to authorize API access
    required: true
  data:
    description:
      - Defines the rack configuration
    suboptions:
      name:
        description:
          - The name of the rack
        required: true
      facility_id:
        description:
          - The unique rack ID assigned by the facility
      site:
        description:
          - Required if I(state=present) and the rack does not exist yet
      rack_group:
        description:
          - The rack group the rack will be associated to
      tenant:
        description:
          - The tenant that the device will be assigned to
      status:
        description:
          - The status of the rack
        choices:
          - Active
          - Planned
          - Reserved
          - Available
          - Deprecated
      rack_role:
        description:
          - The rack role the rack will be associated to
      serial:
        description:
          - Serial number of the rack
      asset_tag:
        description:
          - Asset tag that is associated to the rack
      type:
        description:
          - The type of rack
        choices:
          - 2-post frame
          - 4-post frame
          - 4-post cabinet
          - Wall-mounted frame
          - Wall-mounted cabinet
      width:
        description:
          - The rail-to-rail width
        choices:
          - 19
          - 23
      u_height:
        description:
          - The height of the rack in rack units
      desc_units:
        description:
          - Rack units will be numbered top-to-bottom
        type: bool
      outer_width:
        description:
          - The outer width of the rack
      outer_depth:
        description:
          - The outer depth of the rack
      outer_unit:
        description:
          - Whether the rack unit is in Millimeters or Inches and is I(required) if outer_width/outer_depth is specified
        choices:
          - Millimeters
          - Inches
      comments:
        description:
          - Comments that may include additional information in regards to the rack
      tags:
        description:
          - Any tags that the rack may need to be associated with
      custom_fields:
        description:
          - must exist in Netbox
    required: true
  state:
    description:
      - Use C(present) or C(absent) for adding or removing.
    choices: [ absent, present ]
    default: present
  validate_certs:
    description:
      - If C(no), SSL certificates will not be validated. This should only be used on personally controlled sites using self-signed certificates.
    default: 'yes'
    type: bool
"""

EXAMPLES = r"""
- name: "Test Netbox modules"
  connection: local
  hosts: localhost
  gather_facts: False

  tasks:
    - name: Create rack within Netbox with only required information
      netbox_rack:
        netbox_url: http://netbox.local
        netbox_token: thisIsMyToken
        data:
          name: Test rack
          site: Test Site
        state: present

    - name: Delete rack within netbox
      netbox_rack:
        netbox_url: http://netbox.local
        netbox_token: thisIsMyToken
        data:
          name: Test Rack 
        state: absent
"""

RETURN = r"""
rack:
  description: Serialized object as created or already existent within Netbox
  returned: success (when I(state=present))
  type: dict
msg:
  description: Message indicating failure or info about what has been achieved
  returned: always
  type: str
"""

from ansible_collections.netbox_community.ansible_modules.plugins.module_utils.netbox_utils import (
    NetboxAnsibleModule,
    NETBOX_ARG_SPEC,
)
from ansible_collections.netbox_community.ansible_modules.plugins.module_utils.netbox_dcim import (
    NetboxDcimModule,
    NB_RACKS,
)


def main():
    """
    Main entry point for module execution
    """
    argument_spec = NETBOX_ARG_SPEC
    argument_spec.update(
        dict(
            data=dict(
                type="dict",
                required=True,
                options=dict(
                    name=dict(required=True, type="str"),
                    facility_id=dict(required=False, type="str"),
                    site=dict(required=False, type="raw"),
                    rack_group=dict(required=False, type="raw"),
                    tenant=dict(required=False, type="raw"),
                    # Will uncomment other status dict once slugs are the only option (Netbox 2.8)
                    status=dict(required=False, type="raw"),
                    # status=dict(
                    #    required=False,
                    #    type="str",
                    #    choices=[
                    #        "Active",
                    #        "Planned",
                    #        "Reserved",
                    #        "Available",
                    #        "Deprecated",
                    #    ],
                    # ),
                    rack_role=dict(required=False, type="raw"),
                    serial=dict(required=False, type="str"),
                    asset_tag=dict(required=False, type="str"),
                    type=dict(
                        required=False,
                        type="str",
                        choices=[
                            "2-post frame",
                            "4-post frame",
                            "4-post cabinet",
                            "Wall-mounted frame",
                            "Wall-mounted cabinet",
                        ],
                    ),
                    width=dict(required=False, type="str", choices=["19", "23",],),
                    u_height=dict(required=False, type="int"),
                    desc_units=dict(required=False, type="bool"),
                    outer_width=dict(required=False, type="int"),
                    outer_depth=dict(required=False, type="int"),
                    outer_unit=dict(
                        required=False, type="str", choices=["Millimeters", "Inches",],
                    ),
                    comments=dict(required=False, type="str"),
                    tags=dict(required=False, type=list),
                    custom_fields=dict(required=False, type=dict),
                ),
            ),
        )
    )

    required_if = [("state", "present", ["name"]), ("state", "absent", ["name"])]

    module = NetboxAnsibleModule(
        argument_spec=argument_spec, supports_check_mode=True, required_if=required_if
    )

    netbox_rack = NetboxDcimModule(module, NB_RACKS)
    netbox_rack.run()


if __name__ == "__main__":
    main()
