from typing import Dict, Union
from sliver import SliverClientConfig, SliverClient, InteractiveBeacon, InteractiveSession


# global 'cache'
sliver_server_clients: Dict[str, SliverClient] = {}
sliver_implant_clients: Dict[str, Union[InteractiveSession, InteractiveBeacon]] = {}


async def connect_and_store_sliver_client(configfile_id, configfile):
    # This function could run multiple times during service startup, so add check to not re-create client
    if (configfile_id in sliver_server_clients.keys()):
        return sliver_server_clients[f"{configfile_id}"]

    config = SliverClientConfig.parse_config(configfile)
    client = SliverClient(config)
    await client.connect()
    
    sliver_server_clients[f"{configfile_id}"] = client

    return client


async def connect_and_store_sliver_interact(configfile_id, implant_id):
    client = sliver_server_clients[f"{configfile_id}"]

    beacon_interact = await client.interact_beacon(implant_id)
    session_interact = await client.interact_session(implant_id)
    implant_interact = beacon_interact or session_interact

    sliver_implant_clients[f"{implant_id}"] = implant_interact
