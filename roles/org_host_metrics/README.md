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
| org_host_metrics_report_dest | default | {{ playbook_dir }}/org_host_metrics_report.json | Destination location for report |
| org_host_metrics_report_mode | default | 0644 | Destination permissions for report |
| org_host_metrics_report | var | {} |  |

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

  ```yaml
    - hosts: servers
      tasks:
        - name: Execute org_host_metrics role
          ansible.builtin.include_role:
            name: org_host_metrics
          vars:
            # omit to process all organizations
            org_host_metrics_org_names:
              - Default
  ```

License
-------

GPL-2.0-or-later

Author Information
-------
**Zach LeBlanc <@zjleblanc>**

Red Hat
