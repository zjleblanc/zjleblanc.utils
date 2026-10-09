# Changelog

All notable changes to this collection will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

### Added

- `download_aap_installer_rpm_deps` playbook, downloading only the base OS RPM dependencies (e.g. `podman`, `ansible-core`, `crun`) required by the [Ansible Automation Platform containerized installer](https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.7/install-assembly_aap_containerized_disconnected_installation) via `dnf download --resolve`, and installing them on a disconnected host via `dnf localinstall`.
- `community.general` collection dependency, required by the new playbook.

## [1.3.9] and earlier

Releases prior to this file being introduced were tracked only via [GitHub tags](https://github.com/zjleblanc/zjleblanc.utils/tags) and commit history.
