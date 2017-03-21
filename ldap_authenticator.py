#!/usr/bin/evn python3
# coding: utf-8

"""LDAP authentication plugin for conan package manager

@author:   Dmitry Sokolov <mr.dmitry.sokolov@gmail.com>
@date:     2017-03-16
@version:  1.0


Install
----------------------------------------

- Clone the repository
- Copy to (or create link) ~/.conan_server/plugins/authenticator/ldap_authenticator.py
- Create ~/.conan_server/plugins/authenticator/ldap.conf


ldap.conf
----------------------------------------

[main]

#  LDAP protocol version
version = 3

#  Server name or IP
server = example.org

#  Distinguished Name (DN) pattern
#    {user} - a substitute for user name
dn = cn={user},dc=example,dc=org

#  Whether to use SSL (yes/no)
use_ssl = yes

[ssl]

#  Whether to validate certificate
#    CERT_NONE     - no certificates from the other side are required (or will
#                    be looked at if provided)
#    CERT_OPTIONAL - certificates are not required, but if provided will be
#                    validated, and if validation fails, the connection will
#                    also fail
#    CERT_REQUIRED - certificates are required, and will be validated, and
#                    if validation fails, the connection will also fail
validate = CERT_REQUIRED

"""

import configparser
import os
import ldap3
from ldap3.core.exceptions import LDAPExceptionError
import ssl


def get_class():
    return LDAPAuthenticator()


class LDAPAuthenticator(object):
    def __init__(self):
        conf_dir = os.path.dirname(os.path.abspath(__file__))
        conf = configparser.ConfigParser()
        conf.read(os.path.join(conf_dir, "ldap.conf"))

        conf_main = conf["main"]
        self.ldap_version = conf_main.getint("version", 3)
        self.ldap_server = conf_main.get("server", "example.org")
        self.ldap_dn = conf_main.get("dn", "cn={user},dc=example,dc=org")

        self.use_ssl = False
        self.ssl_validate = ssl.CERT_NONE
        if conf_main.getboolean("use_ssl", False):
            conf_ssl = conf["ssl"]
            self.ssl_validate = {"CERT_NONE": ssl.CERT_NONE,
                                 "CERT_OPTIONAL": ssl.CERT_OPTIONAL,
                                 "CERT_REQUIRED": ssl.CERT_REQUIRED
                                 }.get(conf_ssl.getboolean("validate", "CERT_NONE"))

    def valid_user(self, username, plain_password):
        try:
            tls_conf = ldap3.Tls(validate=self.ssl_validate) if self.use_ssl else None
            server = ldap3.Server(self.ldap_server, use_ssl=self.use_ssl, tls=tls_conf)
            uid = self.ldap_dn.format(user=username)
            ldap3.Connection(server, user=uid, password=plain_password, version=self.ldap_version,
                             auto_bind=True, read_only=True)
        except LDAPExceptionError:
            return False
        return True
