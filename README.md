# HTTP JSON REST Authenticator module for synapse
Allows you to use any backend implementing a specific HTTP JSON REST endpoint to authenticate a user in Matrix.  
This allows to externalize authentication in synapse without having to write a module in python but rely on possibly existing workflows.

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
```
password_providers:
  - module: "rest_auth_provider.RestAuthProvider"
    config:
      endpoint: "http://change.me.example.com:12345"
```

## Use
1. Install, configure, restart synapse
2. Try to login with a valid username and password for the endpoint configured

## Extend
The following endpoint path is called with HTTP POST request: `/_matrix-internal/identity/v1/check_credentials` with the following JSON body:
```
{
  "user": {
    "id": "@matrix.id.of.the.user:example.com",
    "password": "passwordOfTheUser"
  }
}
```

The following JSON answer is expected:
```
{
  "authentication": {
    "success": <boolean>
    "mxid": "@matrix.id.of.the.user:example.com"
    "display_name": <String of the display name to set, optional>
  }
}
```

## Support
For community support, use the Matrix room [#matrix-synapse-rest-auth:kamax.io](https://matrix.to/#/#matrix-synapse-rest-auth:kamax.io)
