from pprint import pprint
from uuid import uuid4
from index_by.key import index_by_key

from gs_api_client import SyncGridscaleApiClient, GridscaleApiClient, models
from gs_api_client import Configuration

import secrets

api_key = secrets.api_key_gridscale
api_user = secrets.api_user_gridscale

def get_client():
    # run `pip3 install index_by` before executing this file

    api_config = Configuration()
    # api_config.debug = True
    api_config.host = 'https://api.gridscale.io'

    api_config.api_key['X-Auth-Token'] = api_key
    api_config.api_key['X-Auth-UserId'] = api_user
    api_config.debug = False

    grid_client = SyncGridscaleApiClient(configuration=api_config, http_info=False)

    return grid_client

def get_client_async():
    # run `pip3 install index_by` before executing this file

    api_config = Configuration()
    # api_config.debug = True
    api_config.host = 'https://api.gridscale.io'

    
    api_config.api_key['X-Auth-Token'] = api_key
    api_config.api_key['X-Auth-UserId'] = api_user
    api_config.debug = False

    grid_client = GridscaleApiClient(configuration=api_config, http_info=False)

    return grid_client
