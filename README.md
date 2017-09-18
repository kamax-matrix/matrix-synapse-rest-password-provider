# HTTP JSON REST Authenticator module for synapse
This synapse authentication module (password provider) allows you to query identity data in existing webapps, like:
- Forums (phpBB, Discourse, etc.)
- Custom Identity stores (Keycloak, ...)
- CRMs (Wordpress, ...)
- self-hosted clouds (Nextcloud, ownCloud, ...)

It is mainly used with [mxisd](https://github.com/kamax-io/mxisd), the Federated Matrix Identity Server, to delegate all matters of 
Identity (directory, authentication, search) to it and offer a fully integrated solution.

## Install
Copy in whichever directory python2.x can pick it up as a module.  

If you installed synapse using the Matrix debian repos:
```
git clone https://github.com/maxidor/matrix-synapse-rest-auth.git
cd matrix-synapse-rest-auth
sudo cp rest_auth_provider.py /usr/lib/python2.6/dist-packages/
sudo cp rest_auth_provider.py /usr/lib/python2.7/dist-packages/
```

## Configure
Add or amend the `password_providers` entry like so:
```
password_providers:
  - module: "rest_auth_provider.RestAuthProvider"
    config:
      endpoint: "http://change.me.example.com:12345"
```

Replace the `endpoint` value with the appropriate value.

## Use
1. Install, configure, restart synapse
2. Try to login with a valid username and password for the endpoint configured

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
  "authentication": {
    "success": <boolean>
    "mxid": "@matrix.id.of.the.user:example.com"
    "display_name": "String of the display name to set, optional"
  }
}
```

## Support
For community support, use the Matrix room [#matrix-synapse-rest-auth:kamax.io](https://matrix.to/#/#matrix-synapse-rest-auth:kamax.io)
