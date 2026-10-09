# zjleblanc.utils

Ansible collection for utility operations

[Galaxy](https://galaxy.ansible.com/ui/repo/published/zjleblanc/utils/) | [Changelog](CHANGELOG.md)

## Contents

### Playbooks

| Name | Description |
| -------- | ------- |
| [download_aap_installer_rpm_deps](playbooks/download_aap_installer_rpm_deps.yml) | Download/install the base OS RPM dependencies required by the AAP containerized installer on a disconnected host |

See [playbooks/README.md](playbooks/README.md) for variables and usage.

### Roles

| Name | Description |
| -------- | ------- |
| [letsencrypt](roles/letsencrypt) | Generate Let's Encrypt certificates via http-01/dns-01 challenge; optionally configure an nginx site |

### Lookup Plugins

| Name | Description |
| -------- | ------- |
| [org_host_metrics](plugins/lookup/org_host_metrics.py) | Generate host metrics by organization from the controller database |

### Filter Plugins

| Name | Description |
| -------- | ------- |
| [lsof_parse](plugins/filter/lsof_parse.py) | Parse raw `lsof` output into structured records |
| [top_parse](plugins/filter/top_parse.py) | Parse raw `top` output into structured metadata and task data |

### Callback Plugins

| Name | Description |
| -------- | ------- |
| [host_failed_at](plugins/callback/host_failed_at.py) | Records failed tasks with reason/timestamp and emails a failure report |
| [host_failed_at_base](plugins/callback/host_failed_at_base.py) | Records the task name each host failed on |

### Event-Driven Ansible Event Sources

| Name | Description |
| -------- | ------- |
| [custom_webhook](extensions/eda/plugins/event_source/custom_webhook.py) | Receives events via a webhook, with optional TLS/mTLS and HMAC signature verification |
