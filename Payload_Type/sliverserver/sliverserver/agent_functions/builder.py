import pathlib
import json
import asyncio

from mythic_container.PayloadBuilder import *
from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *

from ..utils.sliver_connect import connect_and_store_sliver_client

service_started = False

class SliverServer(PayloadType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # This class is instantiated during start_and_run_forever, as well as when payloads are generated
        # When the service first starts up, it should re-create the sliver clients
        global service_started
        if (not service_started):
            service_started = True
            asyncio.create_task(recreate_sliver_clients())

    name = "sliverserver"
    author = "Spencer Adolph"
    note = "This service payload connects to a Sliver C2 Server to run commands."
    supported_os = [SupportedOS("SliverServer")]
    file_extension = ""
    wrapper = False
    wrapped_payloads = []
    supports_dynamic_loading = False
    c2_profiles = []
    mythic_encrypts = False
    translation_container = None
    agent_type = "service"
    agent_path = pathlib.Path(".") / "sliverserver"
    agent_icon_path = agent_path / "sliver.svg"
    agent_code_path = agent_path / "agent_code"
    build_steps = []
    build_parameters = [
        BuildParameter(
            # https://sliver.sh/docs?name=Multi-player+Mode
            name="configfile_id",
            description="Sliver Operator Config",
            parameter_type=BuildParameterType.File,
        )
    ]

    async def build(self) -> BuildResponse:
        # Get the config file
        filecontent = await SendMythicRPCFileGetContent(MythicRPCFileGetContentMessage(
            AgentFileId=self.get_parameter('configfile_id')
        ))
        # Get the IP from the config
        lhost = json.loads(filecontent.Content)["lhost"]

        # Create a callback so we can send tasks
        await SendMythicRPCCallbackCreate(MythicRPCCallbackCreateMessage(
            PayloadUUID=self.uuid,
            C2ProfileName="",
            IntegrityLevel=3,
            Ip=lhost,
            Host="SliverServer",
            User="SliverServer",
        ))

        # Once this is done, commands will have a connected client available to use
        await connect_and_store_sliver_client(self.uuid, filecontent.Content)

        resp = BuildResponse(status=BuildStatus.Success)
        return resp


async def recreate_sliver_clients():
    # This is a limitation of Mythic which RPC calls, which are generally restricted to a single 'operation'
    # In this case, the operation is determined by a callbackID
    # This is called out in the 'limitations' section of the README
    payload_search_results = await SendMythicRPCPayloadSearch(MythicRPCPayloadSearchMessage(
        CallbackID=1,
        PayloadTypes=['sliverserver']
    ))

    for sliverserver_payload in payload_search_results.Payloads:
        filecontent = await SendMythicRPCFileGetContent(MythicRPCFileGetContentMessage(
            AgentFileId=sliverserver_payload.BuildParameters[0].Value
        ))
        await connect_and_store_sliver_client(sliverserver_payload.UUID, filecontent.Content)
