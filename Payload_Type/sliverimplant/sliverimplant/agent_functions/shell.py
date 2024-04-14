from ..SliverRequests import SliverAPI

from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *
from mythic_container.PayloadBuilder import *

class ShellArguments(TaskArguments):
    def __init__(self, command_line, **kwargs):
        super().__init__(command_line, **kwargs)
        self.args = []

    async def parse_arguments(self):
        pass


class Shell(CommandBase):
    cmd = "shell"
    needs_admin = False
    help_cmd = "shell"
    description = "Interactive Shell"
    version = 1
    author = "Spencer Adolph"
    argument_class = ShellArguments
    attackmapping = []
    supported_ui_features = ['task_response:interactive']

    async def create_go_tasking(self, taskData: MythicCommandBase.PTTaskMessageAllData) -> MythicCommandBase.PTTaskCreateTaskingMessageResponse:
        # Start an interactive shell

        # Usage:
        # ======
        #   shell [flags]

        # Flags:
        # ======
        # TODO:  -h, --help                 display help
        # TODO:  -y, --no-pty               disable use of pty on macos/linux
        # TODO:  -s, --shell-path string    path to shell interpreter
        # TODO:  -t, --timeout    int       command timeout in seconds (default: 60)

        await SliverAPI.shell(taskData)

        taskResponse = MythicCommandBase.PTTaskCreateTaskingMessageResponse(
            TaskID=taskData.Task.ID,
            Success=True,
            Completed=True
        )
        return taskResponse

    async def process_response(self, task: PTTaskMessageAllData, response: any) -> PTTaskProcessResponseMessageResponse:
        resp = PTTaskProcessResponseMessageResponse(TaskID=task.Task.ID, Success=True)
        return resp
