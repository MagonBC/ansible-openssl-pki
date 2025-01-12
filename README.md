# ansible-openssl-pki

An extendable ansible role to create a local Root CA and then, add Subordinate CAs as much as you want!

Additionally, the role provide necessary basic commands to manipulate easily certificates and CRLs.

To understand all details of configuration while using this role, I recommand to read **Evan Restic** is awesome and free [Openssl CookBook](https://www.feistyduck.com/library/openssl-cookbook/online/)!

Use cases
=========
The [root-ca.conf](https://github.com/MagonBC/ansible-openssl-pki/blob/main/roles/openssl-ca/templates/root-ca.conf.j2) file containes necessary extentions to:
1. Manually generate the 3 Kubernetes CA, in order to properly init a controle-plane. 
```shell
/etc/kubernetes/pki/ca.crt
/etc/kubernetes/pki/ca.key
/etc/kubernetes/pki/etcd/ca.crt
/etc/kubernetes/pki/etcd/ca.key
/etc/kubernetes/pki/front-proxy-ca.crt
/etc/kubernetes/pki/front-proxy-ca.key
```
Reference -> [PKI certificates and requirements](https://kubernetes.io/docs/setup/best-practices/certificates/#:~:text=Kubernetes%20requires%20PKI%20certificates%20for,them%20on%20the%20API%20server.)

2. Create a subordinate CA used to generate certificates for **server**, **client** and **kernel module signing** (for secure boot)!

