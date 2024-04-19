from ..SliverRequests import SliverAPI

from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *
from mythic_container.PayloadBuilder import *


class BuildersArguments(TaskArguments):
    def __init__(self, command_line, **kwargs):
        super().__init__(command_line, **kwargs)
        self.args = []

    async def parse_arguments(self):
        pass


class Builders(CommandBase):
    cmd = "builders"
    needs_admin = False
    help_cmd = "builders"
    description = "Lists external builders currently registered with the server."
    version = 1
    author = "Spencer Adolph"
    argument_class = BuildersArguments
    attackmapping = []

    async def create_go_tasking(self, taskData: MythicCommandBase.PTTaskMessageAllData) -> MythicCommandBase.PTTaskCreateTaskingMessageResponse:
        # Command: builders
        # About: Lists external builders currently registered with the server.

        # External builders allow the Sliver server offload implant builds onto external machines.
        # For more information: https://github.com/BishopFox/sliver/wiki/External-Builders


        # Usage:
        # ======
        #   builders [flags]

        # Flags:
        # ======
        # TODO:  -h, --help           display help
        # TODO:  -t, --timeout int    command timeout in seconds (default: 60)


        response = await builders(taskData)

        await SendMythicRPCResponseCreate(MythicRPCResponseCreateMessage(
            TaskID=taskData.Task.ID,
            Response=response.encode("UTF8"),
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


async def builders(taskData: PTTaskMessageAllData):
    # client = await SliverAPI.create_sliver_client(taskData)
    # client._stub.bu

    # TODO: match sliver formatting

    return "This command not yet implemented, requires re-build of gRPC (or sliver 1.6)"
