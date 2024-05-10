org_host_metrics
=========

Generate host metrics based on an organization in Ansible Automation Platform

Minimum Ansible Version: 2.9

Galaxy Tags: \[ controller hosts inventory metrics \]


Role Variables
--------------

| Variable | Type | Value or Expression | Description |
| -------- | ------- | ------------------- | --------- |
| org_host_metrics_org_names | optional | [Default] | Name of the organization(s) to target |
| org_host_metrics_report | var | {} |  |

Example Playbook
----------------

```yaml
- name: Retrieve host metrics by organization
  hosts: localhost

  roles:
    - role: zjleblanc.utils.org_host_metrics
      vars:
        # omit to process all organizations
        org_host_metrics_org_names:
          - Autodotes
          - Default

  tasks:
    - name: Write report to file
      ansible.builtin.copy:
        content: "{{ org_host_metrics_report | to_nice_json(indent=2) }}"
        dest: "{{ playbook_dir }}/org_host_metrics_report.json"
        mode: "0644"
```

Expected Output
----------------
```json
{
  "Autodotes": {
    "id": 3,
    "name": "Autodotes",
    "organization": {
      "hosts_automated": 2,
      "hosts_disabled": 0,
      "hosts_imported": 18,
      "hosts_with_failures": 0
    },
    "inventories": {
      "AD LDAP Demo Inventory": {
        "hosts_automated": 0,
        "hosts_disabled": 0,
        "hosts_imported": 5,
        "hosts_with_failures": 0
      },
      "Azure Inventory": {
        "hosts_automated": 0,
        "hosts_disabled": 0,
        "hosts_imported": 1,
        "hosts_with_failures": 0
      },
      "Proxmox Inventory": {
        "hosts_automated": 3,
        "hosts_disabled": 0,
        "hosts_imported": 5,
        "hosts_with_failures": 0
      },
      "Satellite Inventory": {
        "hosts_automated": 0,
        "hosts_disabled": 0,
        "hosts_imported": 3,
        "hosts_with_failures": 0
      },
      "Service Now Inventory": {
        "hosts_automated": 0,
        "hosts_disabled": 0,
        "hosts_imported": 5,
        "hosts_with_failures": 0
      }
    }
  },
  "Default": {
    "id": 1,
    "name": "Default",
    "organization": {
      "hosts_automated": 5,
      "hosts_disabled": 0,
      "hosts_imported": 27,
      "hosts_with_failures": 1
    },
    "inventories": {
      "Home Sandbox": {
        "hosts_automated": 4,
        "hosts_disabled": 0,
        "hosts_imported": 16,
        "hosts_with_failures": 1
      },
      "Cisco Sandbox": {
        "hosts_automated": 0,
        "hosts_disabled": 0,
        "hosts_imported": 10,
        "hosts_with_failures": 0
      },
      "Cloud Sandbox": {
        "hosts_automated": 1,
        "hosts_disabled": 0,
        "hosts_imported": 3,
        "hosts_with_failures": 0
      }
    }
  }
}
```

License
-------

GPL-2.0-or-later

Author Information
-------
**Zach LeBlanc <@zjleblanc>**

Red Hat
