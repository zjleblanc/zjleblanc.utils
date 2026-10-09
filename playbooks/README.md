zjleblanc.utils playbooks
=========

download_aap_installer_rpm_deps
------------------------------

Downloads only the host-level RPM dependencies required by the [Ansible Automation Platform containerized installer](https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.7/install-assembly_aap_containerized_disconnected_installation) (e.g. `podman`, `ansible-core`, `crun`) and transfers them to a disconnected host for local installation. Because the AAP bundled setup tarball already ships every container image and collection needed for the install, the disconnected host only needs a small set of base OS packages -- there is no need to mirror the entire BaseOS/AppStream repositories with `reposync`.

On the connected host, the playbook uses `dnf download --resolve` to fetch the requested packages along with their full dependency tree, archives the result, and fetches it to the control node. On the disconnected host, the archive is extracted and installed with `dnf localinstall`.

Requires `community.general` (for `archive`).

**Inventory groups**

| Group | Description |
| -------- | ------- |
| `rhel_connected` | RHEL host with an active internet connection used to run `dnf download` |
| `rhel_disconnected` | Air-gapped RHEL host(s) that will install the downloaded RPMs via `dnf localinstall` |

**Variables**

| Variable | Type | Value or Expression | Description |
| -------- | ------- | ------------------- | --------- |
| aap_rpm_dirname | default | aap-rpm-deps | Directory/archive base name used on both hosts |
| aap_rpm_download_path | default | `{{ ansible_user_dir }}/{{ aap_rpm_dirname }}` | Where `dnf download` saves RPMs on the connected host |
| aap_rpm_fetch_dir | default | `{{ playbook_dir }}/fetched_archives` | Local directory on the control node used to stage the fetched archive |
| aap_rpm_dest_path | default | `/opt/{{ aap_rpm_dirname }}` | Where the RPM archive is extracted on the disconnected host |
| aap_installer_packages | default | see below | List of packages (and their dependency tree) to download/install |

`aap_installer_packages` defaults to the base OS packages required by the AAP containerized installer's `ansible.containerized_installer` common role, plus `ansible-core` to run the installer itself:

```yaml
aap_installer_packages:
  - ansible-core
  - podman
  - crun
  - slirp4netns
  - fuse-overlayfs
  - polkit
  - gzip
  - rsync
  - container-selinux
  - python3-firewall
```

**Example Playbook**

```yaml
- name: Download and install AAP installer RPM dependencies
  ansible.builtin.import_playbook: zjleblanc.utils.download_aap_installer_rpm_deps
```

```ini
[rhel_connected]
connected-rhel.example.com

[rhel_disconnected]
disconnected-rhel.example.com
```

```sh
ansible-playbook -i inventory.ini zjleblanc.utils.download_aap_installer_rpm_deps
```

License
-------

MIT

Author Information
-------
**Zachary LeBlanc**

Red Hat
