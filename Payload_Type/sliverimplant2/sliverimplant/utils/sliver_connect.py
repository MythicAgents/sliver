import asyncio
from typing import Dict, Union
from sliver import SliverClientConfig, SliverClient, InteractiveBeacon, InteractiveSession, client_pb2

from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *
from mythic_container.PayloadBuilder import *


# global 'cache'
sliver_server_clients: Dict[str, SliverClient] = {}
sliver_implant_clients: Dict[str, Union[InteractiveSession, InteractiveBeacon]] = {}


async def connect_and_store_sliver_client(configfile_id, configfile):
    # This function could run multiple times during service startup or sync, so add check to not re-create client
    if (configfile_id in sliver_server_clients.keys()):
        return sliver_server_clients[f"{configfile_id}"]

    config = SliverClientConfig.parse_config(configfile)
    client = SliverClient(config)
    await client.connect()
    
    sliver_server_clients[f"{configfile_id}"] = client

    async def read_server_events():
        async for data in client.events():
            await handle_sliver_event(data)
    asyncio.create_task(read_server_events())

    return client


async def connect_and_store_sliver_interact(configfile_id, implant_id):
    client = sliver_server_clients[f"{configfile_id}"]

    # These simplify later functionality, but appear to trigger a 'user connected' event that shows in sliver
    # Alternatively, could just .interact when running the function if that becomes annoying
    beacon_interact = await client.interact_beacon(implant_id)
    session_interact = await client.interact_session(implant_id)
    implant_interact = beacon_interact or session_interact

    if (implant_interact == None):
        # TODO: possibly another good spot to mark as 'disconnected'
        return None

    sliver_implant_clients[f"{implant_id}"] = implant_interact
    return implant_interact


async def handle_sliver_event(event: client_pb2.Event):
    # Implant service handles disconnects so that it can update the cached interacts
    # Server service wouldn't have access to those variables
    if (event.EventType == 'session-disconnected'):
        print('session disconnected event')

        callbacks = await SendMythicRPCCallbackSearch(MythicRPCCallbackSearchMessage(
            AgentCallbackID=1,
            SearchCallbackExtraInfo=event.Session.ID
        ))

        await SendMythicRPCCallbackUpdate(MythicRPCCallbackUpdateMessage(
            CallbackID=callbacks.Results[0].ID,
            Description='disconnected!',
            IntegrityLevel=-1,
        ))

        sliver_implant_clients[f"{event.Session.ID}"] = None

    else:
        print(f"implant unhandled event: {event.EventType}")
