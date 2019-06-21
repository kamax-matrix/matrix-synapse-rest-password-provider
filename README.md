# Synapse REST Password provider
- [Overview](#overview)
- [Install](#install)
- [Configure](#configure)
- [Integrate](#integrate)
- [Support](#support)
---

**This project is no longer maintained.**

---

## Overview
This synapse's password provider allows you to validate a password for a given username and return a user profile using an existing backend, like:

- Forums (phpBB, Discourse, etc.)
- Custom Identity stores (Keycloak, ...)
- CRMs (Wordpress, ...)
- self-hosted clouds (Nextcloud, ownCloud, ...)

It is mainly used with [mxisd](https://github.com/kamax-matrix/mxisd), the Federated Matrix Identity Server, to provide
missing features and offer a fully integrated solution (directory, authentication, search).

**NOTE:** This module doesn't provide direct integration with any backend. If you do not use mxisd, you will need to write
your own backend, following the [Integration section](#integrate). This module simply translate an anthentication result
and profile information into actionables in synapse, and adapt your user profile with what is given.

## Install
### From Synapse v0.34.0/py3
Copy in whichever directory python3.x can pick it up as a module.  

If you installed synapse using the Matrix debian repos:
```
sudo curl https://raw.githubusercontent.com/kamax-matrix/matrix-synapse-rest-auth/master/rest_auth_provider.py -o /opt/venvs/matrix-synapse/lib/python3.5/site-packages/rest_auth_provider.py
```
If the command fail, double check that the python version still matches. If not, please let us know by opening an issue.

### Before Synapse v0.34.0/py3 or any py2-based release
Copy in whichever directory python2.x can pick it up as a module.  

If you installed synapse using the Matrix debian repos:
```
sudo curl https://raw.githubusercontent.com/kamax-matrix/matrix-synapse-rest-auth/master/rest_auth_provider.py -o /usr/lib/python2.7/dist-packages/rest_auth_provider.py
```
If the command fail, double check that the python version still matches. If not, please let us know by opening an issue.

## Configure
Add or amend the `password_providers` entry like so:
```yaml
password_providers:
  - module: "rest_auth_provider.RestAuthProvider"
    config:
      endpoint: "http://change.me.example.com:12345"
```
Set `endpoint` to the value documented with the endpoint provider.

## Use
1. Install, configure, restart synapse
2. Try to login with a valid username and password for the endpoint configured

## Next steps
### Lowercase username enforcement
**NOTE**: This is no longer relevant as synapse natively enforces lowercase.

To avoid creating users accounts with uppercase characters in their usernames and running into known
issues regarding case sensitivity in synapse, attempting to login with such username will fail.

It is highly recommended to keep this feature enable, but in case you would like to disable it:
```yaml
    config:
      policy:
        registration:
          username:
            enforceLowercase: false
```

### Profile auto-fill
By default, on first login, the display name is set to the one returned by the backend.  
If none is given, the display name is not set.  
Upon subsequent login, the display name is not changed.

If you would like to change the behaviour, you can use the following configuration items:
```yaml
    config:
      policy:
        registration:
          profile:
            name: true
        login:
          profile:
            name: false
```

3PIDs received from the backend are merged with the ones already linked to the account.
If you would like to change this behaviour, you can use the following configuration items:
```yaml
    config:
      policy:
        all:
          threepid:
            update: false
            replace: false
```
If update is set to `false`, the 3PIDs will not be changed at all. If replace is set to `true`, all 3PIDs not available in the backend anymore will be deleted from synapse.

## Integrate
To use this module with your back-end, you will need to implement a single REST endpoint:

Path: `/_matrix-internal/identity/v1/check_credentials`  
Method: POST  
Body as JSON UTF-8:
```json
{
  "user": {
    "id": "@matrix.id.of.the.user:example.com",
    "password": "passwordOfTheUser"
  }
}
```

If the credentials are accepted, the following JSON answer will be provided:
```json
{
  "auth": {
    "success": true,
    "mxid": "@matrix.id.of.the.user:example.com",
    "profile": {
      "display_name": "John Doe",
      "three_pids": [
        {
          "medium": "email",
          "address": "john.doe@example.org"
        },
        {
          "medium": "msisdn",
          "address": "123456789"
        }
      ]
    }
  }
}
```
`auth.profile` and any sub-key are optional.

---

If the credentials are refused, the following JSON answer will be provided:
```json
{
  "auth": {
    "success": false
  }
}
```
