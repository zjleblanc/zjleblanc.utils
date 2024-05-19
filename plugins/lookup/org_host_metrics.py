# (c) 2020 Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
name: org_host_metrics
author: Zachary LeBlanc
short_description: Generate host metrics by organization
requirements:
  - None
description:
  - Returns host metrics from the AAP database per organization
  - Useful to generate reports when integration with Automation Analytics is not enabled
options:
  names:
    description:
        - If a list is provided, then host metrics will only be gathered for specified Organizations
        - If not provided, then all Organizations will be analyzed
    required: False
    type: list
extends_documentation_fragment: zjleblanc.utils.auth_plugin
"""

EXAMPLES = """
- name: Gather host metrics
  ansible.builtin.set_fact:
    host_metrics: "{{ lookup('zjleblanc.utils.org_host_metrics') }}"

- name: Publish a host metrics report
  ansible.builtin.copy:
    content: "{{ lookup('zjleblanc.utils.org_host_metrics') | to_nice_json(indent=2) }}"
    dest: "{{ report_dest }}"
    mode: "{{ report_mode }}"

- name: Publish a host metrics report for the Default organization only
  ansible.builtin.copy:
    content: "{{ lookup('zjleblanc.utils.org_host_metrics', names=['Default']) | to_nice_json(indent=2) }}"
    dest: "{{ report_dest }}"
    mode: "{{ report_mode }}"
"""

RETURN = """
  _list:
    description:
      - A list of Organization specific host metrics, sub-divided by Inventory
    type: list
    contains:
      id:
        description: The Organization id
        type: int
      name:
        description: The Organization name
        type: str
      organization:
        description: The Organization level host metrics
        type: dict
        contains:
          hosts_imported:
            description: The total hosts imported in this Inventory
            type: int
          hosts_automated:
            description: The total hosts automated in this Inventory, based on job execution records
            type: int
          hosts_disabled:
            description: The total hosts disabled in this Inventory
            type: int
          hosts_with_failures:
            description: The total hosts with failures in this Inventory, based on job execution records
            type: int
      inventories:
        description: The Inventory level host metrics keyed off of the Inventory id
        type: list
        elements: dict
        sample:
          - id: 1
            name: Demo Inventory
            hosts_automated: 2
            hosts_disabled: 0
            hosts_imported: 18
            hosts_with_failures: 0
"""

from ansible.plugins.lookup import LookupBase
from ansible.errors import AnsibleError
from ansible.module_utils._text import to_native
from ansible.utils.display import Display
from ..module_utils.controller_api import ControllerAPIModule


class LookupModule(LookupBase):
  display = Display()
  module = None

  def handle_error(self, **kwargs):
    raise AnsibleError(to_native(kwargs.get('msg')))

  def warn_callback(self, warning):
    self.display.warning(warning)

  def run(self, terms, variables=None, **kwargs):
    self.set_options(direct=kwargs)

    # Defer processing of params to logic shared with the modules
    module_params = {}
    for plugin_param, module_param in ControllerAPIModule.short_params.items():
      opt_val = self.get_option(plugin_param)
      if opt_val is not None:
        module_params[module_param] = opt_val

    # Create our module
    self.module = ControllerAPIModule(
      argument_spec={}, 
      direct_params=module_params, 
      error_callback=self.handle_error, 
      warn_callback=self.warn_callback
    )

    organizations = self.__get_all('organizations')

    org_names = self.get_option('names', None)
    if org_names:
      organizations = filter(lambda o: o['name'] in org_names, organizations)

    results = []
    for org in organizations:
      results.append(self.__get_org_metrics(org))
    
    return results
  
  def __get_org_metrics(self, org: dict) -> dict:
    inventories = self.__get_all('inventories', {'organization': org['id']})
    hosts = []
    for inv in inventories:
      inv_hosts = self.__get_all('hosts', {'inventory': inv['id']})
      hosts.extend(inv_hosts)
          
    return self.__do_analysis(hosts, org)
  
  def __get_all(self, endpoint: str, query_params=None) -> list:
    response = self.module.get_endpoint(endpoint, data=query_params)

    if 'status_code' not in response:
      raise AnsibleError("Unclear response from API: {0}".format(response))

    if response['status_code'] != 200:
      raise AnsibleError("Failed to query the API: {0}".format(response['json'].get('detail', response['json'])))

    response_data = response['json']
    if 'results' in response_data:
      next_page = response_data['next']
      while next_page is not None:
        next_response = self.module.get_endpoint(next_page)
        response_data['results'] += next_response['json']['results']
        next_page = next_response['json']['next']
      response_data['next'] = None
    
    return response_data['results']

  def __do_analysis(self, hosts: list, org: dict) -> dict:
    report = { 
      "name": org["name"],
      "id": org["id"],
      "organization": self.__setup_metrics(),
      "inventories": {}
    }

    hostnames = set()
    for host in hosts:
      inventory_id = int(host["summary_fields"]["inventory"]["id"])
      inventory_name = host["summary_fields"]["inventory"]["name"]
      inventory_metrics = report["inventories"].get(inventory_id, self.__setup_metrics())
      inventory_metrics["name"] = inventory_name
      report["inventories"][inventory_id] = self.__add_host_metrics(inventory_metrics, host)

      host_name = host["name"]
      if host_name not in hostnames:
        report["organization"] = self.__add_host_metrics(report["organization"], host)
        hostnames.add(host_name)
    
    report["inventories"] = self.__dict2items(report["inventories"])
    return report
  
  @staticmethod
  def __setup_metrics() -> dict:
    return {
      "hosts_imported": 0,
      "hosts_automated": 0,
      "hosts_with_failures": 0,
      "hosts_disabled": 0
    }
  
  @staticmethod
  def __add_host_metrics(metrics: dict, host: dict) -> dict:
      automated = host["last_job"] != None
      failures = host["has_active_failures"]
      disabled = not host["enabled"]

      metrics["hosts_imported"] += 1
      if automated:
        metrics["hosts_automated"] += 1
      if failures:
        metrics["hosts_with_failures"] += 1
      if disabled:
        metrics["hosts_disabled"] += 1

      return metrics
  
  @staticmethod
  def __dict2items(_in: dict, key="id") -> list:
      items = []
      for k in _in.keys():
        item = _in[k]
        item.update({key: k})
        items.append(item)
      return items