# conan-ldap-plugin

LDAP authentication plugin for conan package manager


## Install

- Clone the repository
- Copy to (or create link) `~/.conan_server/plugins/authenticator/ldap_authenticator.py`
- Create `~/.conan_server/plugins/authenticator/ldap.conf`


## ldap.conf

```ini
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
```