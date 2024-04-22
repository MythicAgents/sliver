from ..SliverRequests import SliverAPI

from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *
from mythic_container.PayloadBuilder import *

class ChtimesArguments(TaskArguments):
    def __init__(self, command_line, **kwargs):
        super().__init__(command_line, **kwargs)
        self.args = []

    async def parse_arguments(self):
        pass


class Chtimes(CommandBase):
    cmd = "chtimes"
    needs_admin = False
    help_cmd = "chtimes"
    description = "Change access and modification times on a file (timestomp)"
    version = 1
    author = "Spencer Adolph"
    argument_class = ChtimesArguments
    attackmapping = []

    async def create_go_tasking(self, taskData: MythicCommandBase.PTTaskMessageAllData) -> MythicCommandBase.PTTaskCreateTaskingMessageResponse:
        # Change access and modification times on a file (timestomp)

        # Usage:
        # ======
        #   chtimes [flags] path atime mtime

        # Args:
        # =====
        #   path   string    path to the file to remove
        #   atime  string    Last accessed time in DateTime format, i.e. 2006-01-02 15:04:05
        #   mtime  string    Last modified time in DateTime format, i.e. 2006-01-02 15:04:05

        # Flags:
        # ======
        #        -h, --help           display help
        #        -t, --timeout int    command timeout in seconds (default: 60)

        response = await chtimes(taskData)

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

async def chtimes(taskData: PTTaskMessageAllData):
    # interact, isBeacon = await SliverAPI.create_sliver_interact(taskData)

    # ifconfig_results = await interact._stub()

    # if (isBeacon):
    #     ifconfig_results = await ifconfig_results

    return "This command not yet implemented..."
