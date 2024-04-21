from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import SendMythicRPCFileGetContent, MythicRPCFileGetContentMessage
from sliver import SliverClientConfig, SliverClient, client_pb2
from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *
from mythic_container.PayloadBuilder import *
import asyncio

# from mythic_container.MythicCommandBase import *
# from mythic_container.MythicRPC import *
# from mythic_container.PayloadBuilder import *

sliver_clients = {}

async def create_sliver_client(taskData: PTTaskMessageAllData):
    if (f"{taskData.Payload.UUID}" in sliver_clients.keys()):
        return sliver_clients[f"{taskData.Payload.UUID}"]
    
    filecontent = await SendMythicRPCFileGetContent(MythicRPCFileGetContentMessage(
        # TODO: could possibly mirror this in the implant create_client, and get rid of extraInfo? (payload vs callback....)
        AgentFileId=taskData.BuildParameters[0].Value
    ))

    config = SliverClientConfig.parse_config(filecontent.Content)
    client = SliverClient(config)
    
    await client.connect()

    sliver_clients[f"{taskData.Payload.UUID}"] = client

    # 'Sync' Events from the Server
    # TODO: refactor this into the builder.py
    # TODO: is this a weird python closure? (and does that matter?)
    async def read_server_events():
        async for data in client.events():
            await handleSliverEvent(data, taskData.BuildParameters[0].Value)
    asyncio.create_task(read_server_events())

    # TODO: sync callbacks and payloads here

    return client


# TODO: could refactor this more
async def create_sliver_client_with_config(payload_uuid, configFileId):

    filecontent = await SendMythicRPCFileGetContent(MythicRPCFileGetContentMessage(
        # TODO: could possibly mirror this in the implant create_client, and get rid of extraInfo? (payload vs callback....)
        AgentFileId=configFileId
    ))

    config = SliverClientConfig.parse_config(filecontent.Content)
    client = SliverClient(config)
    
    await client.connect()

    sliver_clients[f"{payload_uuid}"] = client

    # TODO: refactor this into the builder.py
    async def read_server_events():
        async for data in client.events():
            await handleSliverEvent(data, configFileId)
    asyncio.create_task(read_server_events())

    # TODO: sync callbacks and payloads here

    return client

# TODO: spin these off from python main.py, instead of waiting for a first 'sessions' command (or anything)
# might be able to 'for each sliverapi payload, cache the client and start a thread...'
async def handleSliverEvent(event: client_pb2.Event, configFileId):
    print(event.EventType)
    # if (data.EventType == 'session-connected'):
    #             print('session-connected')
    #             # look for uuid in payload types
    #             # if payload type doesn't exist, create it, then make callback
    #             # if payload type does exist, look for callback, create it if not found? (but should be there if payload is there?)
    #             # print(taskData.Callback.ID)
    #             # print(data.Session)
    #         print(data.EventType)

    if (event.EventType == 'session-connected'):
        # print(event.Session)

        # create payload
        sliver_os_table = {
            'linux': 'Linux'
        }

        # TODO: only include 'shell' for interactive sessions, not beacons

        new_payload = MythicRPCPayloadCreateFromScratchMessage(
            # TODO: this may need some mythic improvements
            TaskID=1,

            PayloadConfiguration=MythicRPCPayloadConfiguration(
                payload_type="sliverimplant",
                uuid=event.Session.ID,
                selected_os=sliver_os_table[event.Session.OS],                 
                description=f"(no download) using sliver interactive implant for {event.Session.ID}",
                build_parameters=[],
                c2_profiles=[],
                # TODO: figure out if possible to not specify these manually
                commands=['ifconfig', 'download', 'upload', 'ls', 'ps', 'ping', 'whoami', 'screenshot', 'netstat', 'getgid', 'getuid', 'getpid', 'cat', 'cd', 'pwd', 'info', 'execute', 'mkdir', 'shell', 'terminate', 'rm']
            ),
        )
        scratchBuild = await SendMythicRPCPayloadCreateFromScratch(new_payload)

        # create callback
        extra_info = json.dumps({
            # TODO: if buildparams changes, then this won't work anymore (could make it more resilient)
            "slivercfg_fileid": configFileId,
            "type": 'session'
        })
        response = await SendMythicRPCCallbackCreate(MythicRPCCallbackCreateMessage(
            PayloadUUID=event.Session.ID,

            C2ProfileName="",
            IntegrityLevel=3,
            Host=event.Session.Hostname,
            User=event.Session.Username,
            Ip=event.Session.RemoteAddress.split(':')[0],
            ExtraInfo=extra_info,
            PID=event.Session.PID
        ))

    if (event.EventType == 'session-disconnected'):
        print(event)
        # close the callback?

        # which callback to close?

        callbacks = await SendMythicRPCCallbackSearch(MythicRPCCallbackSearchMessage(
            AgentCallbackID=1,
            SearchCallbackPID=event.Session.PID
        ))

        await SendMythicRPCCallbackUpdate(MythicRPCCallbackUpdateMessage(
            CallbackID=callbacks.Results[0].ID,
            TaskID=1,
            PID=event.Session.PID,
            
            Description='disconnected!'
        ))



