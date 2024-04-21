from ..SliverRequests import SliverAPI

from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *
from mythic_container.PayloadBuilder import *


class VersionArguments(TaskArguments):
    def __init__(self, command_line, **kwargs):
        super().__init__(command_line, **kwargs)
        self.args = []

    async def parse_arguments(self):
        pass


class Version(CommandBase):
    cmd = "version"
    needs_admin = False
    help_cmd = "version"
    description = "Display version information"
    version = 1
    author = "Spencer Adolph"
    argument_class = VersionArguments
    attackmapping = []

    async def create_go_tasking(self, taskData: MythicCommandBase.PTTaskMessageAllData) -> MythicCommandBase.PTTaskCreateTaskingMessageResponse:      
        # Display version information

        # Usage:
        # ======
        #   version [flags]

        # Flags:
        # ======
        #        -h, --help           display help
        #        -t, --timeout int    command timeout in seconds (default: 60)

        response = await version(taskData)

        await SendMythicRPCResponseCreate(MythicRPCResponseCreateMessage(
            TaskID=taskData.Task.ID,
            Response=response.encode("UTF8"),
        ))

        taskResponse = MythicCommandBase.PTTaskCreateTaskingMessageResponse(
            TaskID=taskData.Task.ID,
            Success=True,
            Completed=True,
        )

        return taskResponse

    async def process_response(self, task: PTTaskMessageAllData, response: any) -> PTTaskProcessResponseMessageResponse:
        resp = PTTaskProcessResponseMessageResponse(TaskID=task.Task.ID, Success=True)
        return resp
    

async def version(taskData: PTTaskMessageAllData):
    client = await SliverAPI.create_sliver_client(taskData)
    version_results = await client.version()

    # TODO: match sliver formatting

    # [*] Client v1.5.42 - 85b0e870d05ec47184958dbcb871ddee2eb9e3df - linux/amd64
    #     Compiled at 2024-02-28 13:46:53 -0600 CST
    #     Compiled with go version go1.20.7 linux/amd64


    # [*] Server v1.5.42 - 85b0e870d05ec47184958dbcb871ddee2eb9e3df - linux/amd64
    #     Compiled at 2024-02-28 13:46:53 -0600 CST

    return f"{version_results}"
