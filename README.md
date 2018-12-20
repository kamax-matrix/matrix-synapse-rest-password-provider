# HTTP JSON REST Authenticator module for synapse
This synapse authentication module (password provider) allows you to query identity data in existing webapps, like:
- Forums (phpBB, Discourse, etc.)
- Custom Identity stores (Keycloak, ...)
- CRMs (Wordpress, ...)
- self-hosted clouds (Nextcloud, ownCloud, ...)

It is mainly used with [mxisd](https://github.com/kamax-matrix/mxisd), the Federated Matrix Identity Server, to provide
missing features and offer a fully integrated solution (directory, authentication, search).

## Install
### From Synapse v0.34.0/py3
Copy in whichever directory python3.x can pick it up as a module.  

If you installed synapse using the Matrix debian repos:
```
sudo curl https://raw.githubusercontent.com/kamax-matrix/matrix-synapse-rest-auth/master/rest_auth_provider.py -o /opt/venvs/matrix-synapse/lib/python3.5/site-packages/
```

### Before Synapse v0.34.0/py3 or any py2-based release
Copy in whichever directory python2.x can pick it up as a module.  

If you installed synapse using the Matrix debian repos:
```
sudo curl https://raw.githubusercontent.com/kamax-matrix/matrix-synapse-rest-auth/master/rest_auth_provider.py -o /usr/lib/python2.7/dist-packages/
```

## Configure
Add or amend the `password_providers` entry like so:
```
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
```
[...]
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
```
[...]
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

## Integrate
To use this module with your backend, you will need to implement a single REST endpoint:

Path: `/_matrix-internal/identity/v1/check_credentials`  
Method: POST  
Body as JSON UTF-8:
```
{
  "user": {
    "id": "@matrix.id.of.the.user:example.com",
    "password": "passwordOfTheUser"
  }
}
```

The following JSON answer will be provided:
```
{
  "auth": {
    "success": <boolean>
    "mxid": "@matrix.id.of.the.user:example.com"
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

## Support
For community support, visit our Matrix room [#matrix-synapse-rest-auth:kamax.io](https://matrix.to/#/#matrix-synapse-rest-auth:kamax.io)
