import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')

def test_rootca_selfsign(host):
    cmd = host.run("cd /root/root-ca-lab.local/tools; ./root-ca-req.sh -nodes")

def test_rootca_private_key_permission(host):
    f = host.file('/root/root-ca-lab.local/private/root-ca.key')
    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'
    assert oct(f.mode) == '0o600'

# TODO: get ansible variables root_ca_default_home and root_default_name from role.