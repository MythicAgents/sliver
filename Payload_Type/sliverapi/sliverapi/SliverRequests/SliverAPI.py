from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import SendMythicRPCFileGetContent, MythicRPCFileGetContentMessage
from sliver import SliverClientConfig, SliverClient, client_pb2
from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *
from mythic_container.PayloadBuilder import *
import asyncio

sliver_clients = {}

async def create_sliver_client(taskData: PTTaskMessageAllData):
    # builder.py should have cached it by calling create_sliver_client_with_config
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

    # # TODO: refactor this into the builder.py
    async def read_server_events():
        async for data in client.events():
            await handleSliverEvent(data, configFileId)
    asyncio.create_task(read_server_events())

    # TODO: sync callbacks and payloads here

    return client

async def handleSliverEvent(event: client_pb2.Event, configFileId):
    print(event.EventType)

    if (event.EventType == 'session-connected'):
        # print(event.Session)

        # create payload
        sliver_os_table = {
            'linux': 'Linux',
            'windows': 'Windows'
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
        # TODO: often hard-coding ID=1 cause not sure how else to get results back...
        # This thread isn't running on behalf of a specific callback
        # Could potentially pass down the CallbackID of the instantiated sliverapi callback
        # All the way from the parent function that called this?
        # it works for now tho........
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
