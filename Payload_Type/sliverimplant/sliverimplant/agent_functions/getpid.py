from ..SliverRequests import SliverAPI

from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *
from mythic_container.PayloadBuilder import *

class GetpidArguments(TaskArguments):
    def __init__(self, command_line, **kwargs):
        super().__init__(command_line, **kwargs)
        self.args = []

    async def parse_arguments(self):
        pass


class Getpid(CommandBase):
    cmd = "getpid"
    needs_admin = False
    help_cmd = "getpid"
    description = "Get session pid"
    version = 1
    author = "Spencer Adolph"
    argument_class = GetpidArguments
    attackmapping = []

    async def create_go_tasking(self, taskData: MythicCommandBase.PTTaskMessageAllData) -> MythicCommandBase.PTTaskCreateTaskingMessageResponse:
        # Get session pid

        # Usage:
        # ======
        #   getpid [flags]

        # Flags:
        # ======
        #        -h, --help           display help
        #        -t, --timeout int    command timeout in seconds (default: 60)

        pid_results = await getpid(taskData)

        await SendMythicRPCResponseCreate(MythicRPCResponseCreateMessage(
            TaskID=taskData.Task.ID,
            Response=pid_results.encode("UTF8"),
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

async def getpid(taskData: PTTaskMessageAllData):
    interact, isBeacon = await SliverAPI.create_sliver_interact(taskData)
    return f"{interact.pid}"
