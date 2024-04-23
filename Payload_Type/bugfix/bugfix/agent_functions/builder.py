import pathlib
from mythic_container.PayloadBuilder import *
from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *


class Bugfix(PayloadType):
    name = "bugfix"
    author = "Spencer Adolph"
    note = """This payload is for a bugfix."""
    supported_os = [SupportedOS("bugfix")]
    file_extension = ""
    wrapper = False
    wrapped_payloads = []
    supports_dynamic_loading = False
    c2_profiles = []
    mythic_encrypts = False
    translation_container = None
    agent_type = "service"
    agent_path = pathlib.Path(".") / "bugfix"
    # agent_icon_path = agent_path / "agent_functions" / "sliver.svg"
    agent_code_path = agent_path / "agent_code"
    build_steps = []
    build_parameters = []

    async def build(self) -> BuildResponse:
        # this function gets called to create an instance of your payload
        resp = BuildResponse(status=BuildStatus.Success)
        ip = "127.0.0.1"
        create_callback = await SendMythicRPCCallbackCreate(MythicRPCCallbackCreateMessage(
            PayloadUUID=self.uuid,
            C2ProfileName="",
            User="bugfix",
            Host="bugfix",
            Ip=ip,
            IntegrityLevel=3,
            ExtraInfo=self.uuid,
        ))

        if not create_callback.Success:
            logger.info(create_callback.Error)
        else:
            logger.info(create_callback.CallbackUUID)
        return resp
