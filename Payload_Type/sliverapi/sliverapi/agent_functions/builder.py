import pathlib
from mythic_container.PayloadBuilder import *
from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *
from ..SliverRequests import SliverAPI

from sliver import SliverClientConfig, SliverClient

import asyncio


async def setupApiThreads():
    # print('setup api threads')

    sliverapi_payloads = await SendMythicRPCPayloadSearch(MythicRPCPayloadSearchMessage(
        CallbackID=1,
        PayloadTypes=['sliverapi']
    ))

    for sliverapi_payload in sliverapi_payloads.Payloads:
        # print('got payload to setup')
        client = await SliverAPI.create_sliver_client_with_config(sliverapi_payload.UUID, sliverapi_payload.BuildParameters[0].Value)

        # TODO: could further improve here by looking for sessions that now exist (that were created while the Mythic service was offline)
        # Create those payloads and callbacks
        # Would fit the usecase of connecting mythic to an already existing sliver operation with lots of callbacks

        # sessions = await client.sessions()
        # for session in sessions:
        #     # if payload uuid doesn't exist, create it and then create the callback?
        #     sliverimplant_payloads = await SendMythicRPCPayloadSearch(MythicRPCPayloadSearchMessage(
        #         CallbackID=1,
        #         PayloadUUID=session.ID
        #     ))
        #     if (len(sliverimplant_payloads.Payloads) == 0):
                # create the payload and callback associated and thread?

# TODO: better name for this
initial_thread_to_handle_api_events = None

class SliverApi(PayloadType):
    # TODO: understand why this fires off twice
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # This class is instantiated during start_and_run_forever, as well as when payloads are generated
        # In this case, I only want this to run setupApiThreads when the service first starts up
        global initial_thread_to_handle_api_events
        if (initial_thread_to_handle_api_events == None):
            initial_thread_to_handle_api_events = asyncio.create_task(setupApiThreads())

    name = "sliverapi"
    author = "Spencer Adolph"
    note = """This payload connects to sliver to run meta commands."""
    supported_os = [SupportedOS("sliver")]
    file_extension = ""
    wrapper = False
    wrapped_payloads = []
    supports_dynamic_loading = False
    c2_profiles = []
    mythic_encrypts = False
    translation_container = None
    agent_type = "service"
    agent_path = pathlib.Path(".") / "sliverapi"
    agent_icon_path = agent_path / "agent_functions" / "sliver.svg"
    agent_code_path = agent_path / "agent_code"
    build_steps = []
    build_parameters = [
        BuildParameter(
            name="CONFIGFILE",
            description="Sliver Operator Config (select file)",
            parameter_type=BuildParameterType.File,
        )
    ]

    async def build(self) -> BuildResponse:
        # this function gets called to create an instance of your payload
        resp = BuildResponse(status=BuildStatus.Success)
        ip = "127.0.0.1"
        create_callback = await SendMythicRPCCallbackCreate(MythicRPCCallbackCreateMessage(
            PayloadUUID=self.uuid,
            C2ProfileName="",
            User="SliverAPI",
            Host="SliverAPI",
            Ip=ip,
            IntegrityLevel=3,
            ExtraInfo=self.uuid,
        ))

        # TODO: fail building if callback already exists for this sliver config?

        # doing this will cache the connection and start to read events
        await SliverAPI.create_sliver_client_with_config(self.uuid, self.build_parameters[0].value)

        if not create_callback.Success:
            logger.info(create_callback.Error)
        else:
            logger.info(create_callback.CallbackUUID)
        return resp
