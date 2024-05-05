import asyncio
from typing import Dict
from sliver import SliverClientConfig, SliverClient, client_pb2

from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *
from mythic_container.PayloadBuilder import *
from mythic_container.MythicRPC import MythicRPCPayloadCreateFromScratchMessage, SendMythicRPCPayloadCreateFromScratch, MythicCommandBase, SendMythicRPCResponseCreate, MythicRPCResponseCreateMessage
from mythic_container.MythicGoRPC.send_mythic_rpc_payload_create_from_scratch import MythicRPCPayloadConfiguration

# global 'cache'
sliver_server_clients: Dict[str, SliverClient] = {}

sliver_os_table_lookup = {
    'linux': 'Linux',
    'windows': 'Windows',
    'darwin': 'macOS'
}


async def connect_and_store_sliver_client(payload_uuid, config_file, config_file_id):
    config = SliverClientConfig.parse_config(config_file)
    client = SliverClient(config)
    await client.connect()

    sliver_server_clients[f"{payload_uuid}"] = client

    async def read_server_events():
        async for data in client.events():
            await handle_sliver_event(data, config_file_id, payload_uuid)
    asyncio.create_task(read_server_events())

    return client


async def handle_sliver_event(event: client_pb2.Event, config_file_id: str, sliverserver_payload_id: str):
    if (event.EventType == 'session-connected'):
        print('session connected event')

        # create payload
        await SendMythicRPCPayloadCreateFromScratch(MythicRPCPayloadCreateFromScratchMessage(
                TaskID=1,
                PayloadConfiguration=MythicRPCPayloadConfiguration(
                    PayloadType="sliverimplant",
                    UUID=event.Session.ID,
                    SelectedOS=sliver_os_table_lookup[f"{event.Session.OS}"],
                    Description=f"sliver interactive implant {event.Session.ID} (event)",
                    BuildParameters=[
                        MythicRPCPayloadConfigurationBuildParameter(
                            name='configfile_id',
                            value=config_file_id
                        )
                    ],
                    C2Profiles=[],
                    Commands=[]
                ),
            ))

        # create callback
        await SendMythicRPCCallbackCreate(MythicRPCCallbackCreateMessage(
            PayloadUUID=event.Session.ID,
            C2ProfileName="",
            IntegrityLevel=3,
            Host=event.Session.Hostname,
            User=event.Session.Username,
            Ip=event.Session.RemoteAddress.split(':')[0],
            ExtraInfo=event.Session.ID,
            PID=event.Session.PID
        ))

    elif (event.EventType == 'beacon-registered'):
        print('beacon register event')

        # unlike session-connected events, beacon-registered Data is not as friendly to work with
        beacon_id = event.Data[2:38].decode("utf-8")
        client = sliver_server_clients[f"{sliverserver_payload_id}"]
        beacon_info = await client.beacon_by_id(beacon_id=beacon_id)

        # create payload
        await SendMythicRPCPayloadCreateFromScratch(MythicRPCPayloadCreateFromScratchMessage(
            TaskID=1,
            PayloadConfiguration=MythicRPCPayloadConfiguration(
                PayloadType="sliverimplant",
                UUID=beacon_info.ID,
                SelectedOS=sliver_os_table_lookup[f"{beacon_info.OS}"],
                Description=f"sliver beaconing implant {beacon_info.ID} (event)",
                BuildParameters=[
                    MythicRPCPayloadConfigurationBuildParameter(
                        name='configfile_id',
                        value=config_file_id
                    )
                ],
                C2Profiles=[],
                Commands=[]
            ),
        ))

        # create callback
        await SendMythicRPCCallbackCreate(MythicRPCCallbackCreateMessage(
            PayloadUUID=beacon_info.ID,
            C2ProfileName="",
            IntegrityLevel=3,
            Host=beacon_info.Hostname,
            User=beacon_info.Username,
            Ip=beacon_info.RemoteAddress.split(':')[0],
            ExtraInfo=beacon_info.ID,
            PID=beacon_info.PID
        ))

    # elif (event.EventType == 'beacon-taskresult'):
    #     # TODO: update the 'last checkin' value in Mythic for this specific beacon
    #     print('beacon task result event')

    else:
        print(f"server unhandled event: {event.EventType}")

