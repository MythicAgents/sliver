from ..SliverRequests import SliverAPI

from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *
from mythic_container.PayloadBuilder import *


class CursedArguments(TaskArguments):
    def __init__(self, command_line, **kwargs):
        super().__init__(command_line, **kwargs)
        self.args = []

    async def parse_arguments(self):
        pass


class Cursed(CommandBase):
    cmd = "cursed"
    needs_admin = False
    help_cmd = "cursed"
    description = "Chrome/electron post-exploitation tool kit"
    version = 1
    author = "Spencer Adolph"
    argument_class = CursedArguments
    attackmapping = []

    async def create_go_tasking(self, taskData: MythicCommandBase.PTTaskMessageAllData) -> MythicCommandBase.PTTaskCreateTaskingMessageResponse:
        # Chrome/electron post-exploitation tool kit (∩｀-´)⊃━☆ﾟ.*･｡ﾟ

        # Usage:
        # ======
        #   cursed [flags]

        # Flags:
        # ======
        # TODO:  -h, --help           display help
        # TODO:  -t, --timeout int    command timeout in seconds (default: 60)

        # Sub Commands:
        # =============
        # TODO:  chrome      Automatically inject a Cursed Chrome payload into a remote Chrome extension
        # TODO:  console     Start a JavaScript console connected to a debug target
        # TODO:  cookies     Dump all cookies from cursed process
        # TODO:  edge        Automatically inject a Cursed Chrome payload into a remote Edge extension
        # TODO:  electron    Curse a remote Electron application
        # TODO:  rm          Remove a Curse from a process
        # TODO:  screenshot  Take a screenshot of a cursed process debug target

        response = await cursed(taskData)

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


async def cursed(taskData: PTTaskMessageAllData):
    # client = await SliverAPI.create_sliver_client(taskData)

    # TODO: match sliver formatting

    return "This command not yet implemented..."
