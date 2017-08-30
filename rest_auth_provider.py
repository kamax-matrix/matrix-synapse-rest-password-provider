# -*- coding: utf-8 -*-
#
# REST endpoint Authentication module for Matrix synapse
# Copyright (C) 2017 Maxime Dor
#
# https://max.kamax.io/
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import logging
from twisted.internet import defer
import requests
import json

__version__ = "0.0.1"
logger = logging.getLogger(__name__)

class RestAuthProvider(object):
    __version__ = "0.0.1"

    def __init__(self, config, account_handler):
        self.account_handler = account_handler

        if not config.endpoint:
            raise RuntimeError('Missing endpoint config')

        self.endpoint = config.endpoint

    @defer.inlineCallbacks
    def check_password(self, user_id, password):
        logger.info("Got password check for " + user_id)
        data = {'user':{'id':user_id, 'password':password}}
        r = requests.post(self.endpoint + '/_matrix-internal/identity/v1/check_credentials', json = data)
        r.raise_for_status()
        r = r.json()
        if not r["authentication"]:
            reason = "Invalid JSON data returned from REST endpoint"
            logger.warning(reason)
            raise RuntimeError(reason)

        auth = r["authentication"]
        if not auth["success"]:
            logger.info("User not authenticated")
            defer.returnValue(False)

        logger.info("User authenticated: %s", auth["mxid"])

        if not (yield self.account_handler.check_user_exists(user_id)):
            logger.info("User %s does not exist yet, creating...", user_id)
            localpart = user_id.split(":", 1)[0][1:]
            user_id, access_token = (yield self.account_handler.register(localpart=localpart))
            logger.info("Registration based on REST data was successful for %s", user_id)

            if auth["display_name"]:
                store = self.account_handler.hs.get_handlers().profile_handler.store
                yield store.set_profile_displayname(localpart, auth["display_name"])
                logger.info("Name '%s' was set based on profile data", auth["display_name"]);

        defer.returnValue(True)

    @staticmethod
    def parse_config(config):
        # verify config sanity
        _require_keys(config, ["endpoint"])

        class _RestConfig(object):
            pass

        rest_config = _RestConfig()
        rest_config.endpoint = config["endpoint"]
        return rest_config

def _require_keys(config, required):
    missing = [key for key in required if key not in config]
    if missing:
        raise Exception(
            "REST Auth enabled but missing required config values: {}".format(
                ", ".join(missing)
            )
        )

