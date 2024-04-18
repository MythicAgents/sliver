from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import SendMythicRPCFileGetContent, MythicRPCFileGetContentMessage
from sliver import SliverClientConfig, SliverClient, client_pb2
from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *
from mythic_container.PayloadBuilder import *


async def create_sliver_client(taskData: PTTaskMessageAllData):
    filecontent = await SendMythicRPCFileGetContent(MythicRPCFileGetContentMessage(
        # TODO: could possibly mirror this in the implant create_client, and get rid of extraInfo? (payload vs callback....)
        AgentFileId=taskData.BuildParameters[0].Value
    ))

    config = SliverClientConfig.parse_config(filecontent.Content)
    client = SliverClient(config)
    
    # TODO: cache this (global dict?) - can verify in this function if need to re-create
    await client.connect()

    return client
