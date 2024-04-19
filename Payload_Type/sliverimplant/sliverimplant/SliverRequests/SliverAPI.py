from mythic_container.MythicCommandBase import PTTaskMessageAllData
from mythic_container.MythicRPC import SendMythicRPCFileGetContent, MythicRPCFileGetContentMessage
from sliver import SliverClientConfig, SliverClient, client_pb2, sliver_pb2
from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *
from mythic_container.PayloadBuilder import *
import json

from mythic_container.LoggingBase import *
from mythic_container.MythicGoRPC import *

from sliver import InteractiveBeacon

# TODO: make this better, if using identify all fields that will be used / handle emptying when exiting
sliver_clients = {}

async def create_sliver_interact(taskData: PTTaskMessageAllData):
    # check to see if its cached
    if (f"{taskData.Callback.ID}" in sliver_clients.keys()):
        return sliver_clients[f"{taskData.Callback.ID}"]['interact'], isinstance(sliver_clients[f"{taskData.Callback.ID}"]['interact'], InteractiveBeacon)

    extraInfoObj = json.loads(taskData.Callback.ExtraInfo)
    configfile = extraInfoObj['slivercfg_fileid']

    # otherwise get it
    filecontent = await SendMythicRPCFileGetContent(MythicRPCFileGetContentMessage(
        AgentFileId=configfile
    ))

    config = SliverClientConfig.parse_config(filecontent.Content)
    client = SliverClient(config)
    await client.connect()

    callback_extra_info = json.loads(taskData.Callback.ExtraInfo)
    isBeacon = callback_extra_info['type'] == 'beacon'
    if (isBeacon):
        interact = await client.interact_beacon(taskData.Payload.UUID)
    else:
        interact = await client.interact_session(taskData.Payload.UUID)

    # cache it for later
    # TODO: memory leak if this never gets removed? (why useful to implement 'exit' command)
    sliver_clients[f"{taskData.Callback.ID}"] = {
        'interact': interact,
    }

    return interact, isBeacon

