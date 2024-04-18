from ..SliverRequests import SliverAPI

from mythic_container.MythicCommandBase import *
from mythic_container.PayloadBuilder import *
from mythic_container.MythicRPC import MythicRPCPayloadCreateFromScratchMessage, MythicCommandBase, SendMythicRPCPayloadCreateFromScratch, SendMythicRPCResponseCreate, MythicRPCResponseCreateMessage

from mythic_container.MythicGoRPC.send_mythic_rpc_payload_create_from_scratch import MythicRPCPayloadConfiguration

class GenerateArguments(TaskArguments):
    def __init__(self, command_line, **kwargs):
        super().__init__(command_line, **kwargs)
        self.args = [
            CommandParameter(
                name="os",
                cli_name="os",
                display_name="os",
                description="operating system",
                default_value='windows',
                type=ParameterType.ChooseOne,
                choices=["linux", "windows"]
            ),
            CommandParameter(
                name="mtls",
                cli_name="mtls",
                display_name="mtls",
                description="mtls ip:port to use",
                type=ParameterType.String,
            ),
        ]

    async def parse_arguments(self):
        self.load_args_from_json_string(self.command_line)


class Generate(CommandBase):
    cmd = "generate"
    needs_admin = False
    help_cmd = "generate"
    description = "Generate a new sliver binary"
    version = 1
    author = "Spencer Adolph"
    argument_class = GenerateArguments
    attackmapping = []

    async def create_go_tasking(self, taskData: MythicCommandBase.PTTaskMessageAllData) -> MythicCommandBase.PTTaskCreateTaskingMessageResponse:
        # TODO: paste all the config options here

        os = taskData.args.get_arg('os')
        mtls = taskData.args.get_arg('mtls')

        sliverconfig_file_uuid = taskData.BuildParameters[0].Value

        sliver_os_table = {
            'linux': 'Linux'
        }

        # TODO: include 'shell' for sessions, but not for beaconers

        createMessage = MythicRPCPayloadCreateFromScratchMessage(
            TaskID=taskData.Task.ID,
            PayloadConfiguration=MythicRPCPayloadConfiguration(
                PayloadType="sliverimplant",
                SelectedOS=sliver_os_table[os],                 
                Description="generated payload: sliver implant",
                BuildParameters=[
                    MythicRPCPayloadConfigurationBuildParameter(
                        name='sliverconfig_file_uuid',
                        value=sliverconfig_file_uuid
                    ),
                    MythicRPCPayloadConfigurationBuildParameter(
                        name='os',
                        value=os
                    ),
                    MythicRPCPayloadConfigurationBuildParameter(
                        name='mtls',
                        value=mtls
                    ),
                ],
                C2Profiles=[],
                Commands=['ifconfig', 'download', 'upload', 'ls', 'ps', 'ping', 'whoami', 'screenshot', 'netstat', 'getgid', 'getuid', 'getpid', 'cat', 'cd', 'pwd', 'info', 'execute', 'mkdir', 'shell', 'terminate', 'rm']
            ),
        )
        await SendMythicRPCPayloadCreateFromScratch(createMessage)
        
        await SendMythicRPCResponseCreate(MythicRPCResponseCreateMessage(
            TaskID=taskData.Task.ID,
            Response="generated implant".encode("UTF8"),
        ))

        taskResponse = MythicCommandBase.PTTaskCreateTaskingMessageResponse(
            TaskID=taskData.Task.ID,
            Success=True,
            Completed=True
        )
        return taskResponse

    async def process_response(self, task: PTTaskMessageAllData, response: any) -> PTTaskProcessResponseMessageResponse:
        resp = PTTaskProcessResponseMessageResponse(TaskID=task.Task.ID, Success=True)
        return resp
