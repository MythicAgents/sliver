from ..SliverRequests import SliverAPI

from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *
from mythic_container.PayloadBuilder import *


class CanariesArguments(TaskArguments):
    def __init__(self, command_line, **kwargs):
        super().__init__(command_line, **kwargs)
        self.args = []

    async def parse_arguments(self):
        pass


class Canaries(CommandBase):
    cmd = "canaries"
    needs_admin = False
    help_cmd = "canaries"
    description = "List previously generated canaries"
    version = 1
    author = "Spencer Adolph"
    argument_class = CanariesArguments
    attackmapping = []

    async def create_go_tasking(self, taskData: MythicCommandBase.PTTaskMessageAllData) -> MythicCommandBase.PTTaskCreateTaskingMessageResponse:
        # List previously generated canaries

        # Usage:
        # ======
        #   canaries [flags]

        # Flags:
        # ======
        # TODO:  -b, --burned         show only triggered/burned canaries
        # TODO:  -h, --help           display help
        # TODO:  -t, --timeout int    command timeout in seconds (default: 60)

        response = await canaries(taskData)

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


async def canaries(taskData: PTTaskMessageAllData):
    client = await SliverAPI.create_sliver_client(taskData)

    canaries_list = await client.canaries()

    # TODO: match sliver formatting

    return f"{canaries_list}"
