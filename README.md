# ansible-openssl-pki

An extendable ansible role to create a local Root CA and then, add Subordinate CAs as much as you want!

Additionally, the role provides necessary basic commands to create, easily, TLS objects like certificates and CRLs.

To understand every detail of the configuration, while using this role, we strongly recommand reading **Evan Restic**'s awesome [Openssl CookBook](https://www.feistyduck.com/library/openssl-cookbook/online/)!

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

2. Create a subordinate CA used to generate certificates for **servers**, **clients** and **[kernel module signing](https://drivers.suse.com/doc/Usage/Secure_Boot_Certificate.html)** (for secure boot)!

Creating Root CA, Sub CA
========================

Root CA
-------

Self-sign the Root CA using the script [root-ca-req.sh](https://github.com/MagonBC/ansible-openssl-pki/blob/main/roles/openssl-ca/templates/root-ca-tools/root-ca-req.sh.j2)

```shell
master:~/root-ca-lab.local/tools # ./root-ca-req.sh 
Generating a RSA private key
.........................................++++
...............................................................................++++
writing new private key to 'private/root-ca.key'
Enter PEM pass phrase:
...
master:~/root-ca-lab.local/tools # ls ../certs/
B12E84F65EB39C91245919744FF57FED.pem  root-ca.crt
```

Subordinate CA
--------------

Create a CA sign request, send the csr request to the Root CA then sign it:

```shell
master:~/root-ca-lab.local/sub-ca/tools # ./sub-ca-req.sh 
Generating a RSA private key
................................++++
........................................................................................................++++
writing new private key to 'private/sub-ca.key'
Enter PEM pass phrase:
Verifying - Enter PEM pass phrase:
-----

master:~/root-ca-lab.local # cp sub-ca/csr/sub-ca.csr csr/

master:~/root-ca-lab.local/tools # ./sub-ca-sign.sh sub-ca pub_sub_ca_ext
Using configuration from root-ca.conf
...
```

Request a webserver cert
------------------------

```shell
master:~/root-ca-lab.local/sub-ca/tools # ./server-req.sh webserver 
Generating a RSA private key
..++++
...............................................................................................................................................................................................................................................................................................................................++++
writing new private key to 'private/webserver.key'
Enter PEM pass phrase:
Verifying - Enter PEM pass phrase:
-----
Using configuration from sub-ca.conf
Enter pass phrase for /root/root-ca-lab.local/sub-ca/private/sub-ca.key:
Check that the request matches the signature
Signature ok
Certificate Details:
Certificate:
    Data:
        Version: 3 (0x2)
        Serial Number:
            70:c2:d1:6b:a5:49:b4:06:22:f6:90:07:fd:46:ed:16
        Issuer:
            countryName               = TN
            organizationName          = ARCH Linux
            commonName                = Sub CA
        Validity
            Not Before: Jan 12 16:04:07 2025 GMT
            Not After : Jan 12 16:04:07 2026 GMT
        Subject:
            countryName               = TN
            organizationName          = ARCH Linux
            organizationalUnitName    = Web Servers
            commonName                = webserver
        Subject Public Key Info:
...
```

Secure Boot
-----------

After generating the _kern_mod_sign.crt_ and [configure secure Boot](https://drivers.suse.com/doc/Usage/Secure_Boot_Certificate.html), You have to (if it's not done automatically) sign all Virtualbox drivers, 
in order to load them without errors:

```shell
export KBUILD_SIGN_PIN=changeit
/lib/modules/$(uname -r)/build/scripts/sign-file sha256 /root/root-ca-lab.local/sub-ca/private/kern_mod_sign.key /root/root-ca-lab.local/sub-ca/certs/kern_mod_sign.crt vboxdrv.ko 
/lib/modules/$(uname -r)/build/scripts/sign-file sha256 /root/root-ca-lab.local/sub-ca/private/kern_mod_sign.key /root/root-ca-lab.local/sub-ca/certs/kern_mod_sign.crt vboxnetadp.ko 
/lib/modules/$(uname -r)/build/scripts/sign-file sha256 /root/root-ca-lab.local/sub-ca/private/kern_mod_sign.key /root/root-ca-lab.local/sub-ca/certs/kern_mod_sign.crt vboxnetflt.ko 
/lib/modules/$(uname -r)/build/scripts/sign-file sha256 /root/root-ca-lab.local/sub-ca/private/kern_mod_sign.key /root/root-ca-lab.local/sub-ca/certs/kern_mod_sign.crt vboxsf.ko 
/lib/modules/$(uname -r)/build/scripts/sign-file sha256 /root/root-ca-lab.local/sub-ca/private/kern_mod_sign.key /root/root-ca-lab.local/sub-ca/certs/kern_mod_sign.crt vboxguest.ko
```

Nice!