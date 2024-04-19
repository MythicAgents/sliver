from ..SliverRequests import SliverAPI

from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *
from mythic_container.PayloadBuilder import *

class ChownArguments(TaskArguments):
    def __init__(self, command_line, **kwargs):
        super().__init__(command_line, **kwargs)
        self.args = []

    async def parse_arguments(self):
        pass


class Chown(CommandBase):
    cmd = "chown"
    needs_admin = False
    help_cmd = "chown"
    description = "Change owner on a file or directory"
    version = 1
    author = "Spencer Adolph"
    argument_class = ChownArguments
    attackmapping = []

    async def create_go_tasking(self, taskData: MythicCommandBase.PTTaskMessageAllData) -> MythicCommandBase.PTTaskCreateTaskingMessageResponse:
        # Change owner on a file or directory

        # Usage:
        # ======
        #   chown [flags] path uid gid

        # Args:
        # =====
        #   path  string    path to the file to remove
        #   uid   string    User, e.g. root
        #   gid   string    Group, e.g. root

        # Flags:
        # ======
        # TODO:  -h, --help             display help
        # TODO:  -r, --recursive        recursively change permissions on files
        # TODO:  -t, --timeout   int    command timeout in seconds (default: 60)

        response = await chown(taskData)

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

async def chown(taskData: PTTaskMessageAllData):
    # interact, isBeacon = await SliverAPI.create_sliver_interact(taskData)

    # ifconfig_results = await interact._stub()

    # if (isBeacon):
    #     ifconfig_results = await ifconfig_results

    return "This command not yet implemented..."
