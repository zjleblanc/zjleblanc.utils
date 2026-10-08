zjleblanc.utils playbooks
=========

configure_local_repo_reposync
------------------------------

Automates [Configure a local repository using reposync](https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.7/install-assembly_aap_containerized_disconnected_installation#configure-local-repo-reposync) from the Ansible Automation Platform disconnected installation guide. The playbook syncs the BaseOS and AppStream repositories on an internet-connected RHEL host, transfers the resulting archive to the control node, and extracts/configures it as a local Yum repository on the disconnected host(s).

Requires `community.general` (for `rhsm_repository` and `archive`).

**Inventory groups**

| Group | Description |
| -------- | ------- |
| `reposync_connected` | RHEL host with an active internet connection used to run `reposync` |
| `reposync_disconnected` | Air-gapped RHEL host(s) that will consume the resulting local repository |

**Required Variables**

| Name | Example | Description |
| -------- | ------- | ------------------- |
| rhel_version | `9` | RHEL major version whose BaseOS/AppStream repositories should be synced |

**Variables**

| Variable | Type | Value or Expression | Description |
| -------- | ------- | ------------------- | --------- |
| reposync_repo_dirname | default | rhel-repos | Directory/archive base name used on both hosts |
| reposync_download_path | default | `{{ ansible_user_dir }}/{{ reposync_repo_dirname }}` | Where `reposync` downloads repo content on the connected host |
| reposync_fetch_dir | default | `{{ playbook_dir }}/fetched_archives` | Local directory on the control node used to stage the fetched archive |
| reposync_dest_path | default | `/opt/{{ reposync_repo_dirname }}` | Where the local repository is extracted on the disconnected host |
| reposync_repo_file | default | /etc/yum.repos.d/rhel-local.repo | Yum repo file created on the disconnected host |

**Example Playbook**

```yaml
- name: Configure a disconnected local repository via reposync
  ansible.builtin.import_playbook: zjleblanc.utils.configure_local_repo_reposync
```

```ini
[reposync_connected]
connected-rhel.example.com

[reposync_disconnected]
disconnected-rhel.example.com
```

```sh
ansible-playbook -i inventory.ini zjleblanc.utils.configure_local_repo_reposync -e rhel_version=9
```

License
-------

MIT

Author Information
-------
**Zachary LeBlanc**

Red Hat
