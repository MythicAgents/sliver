from ..SliverRequests import SliverAPI

from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *
from mythic_container.PayloadBuilder import *

class ScreenshotArguments(TaskArguments):
    def __init__(self, command_line, **kwargs):
        super().__init__(command_line, **kwargs)
        self.args = []

    async def parse_arguments(self):
        pass


class Screenshot(CommandBase):
    cmd = "screenshot"
    needs_admin = False
    help_cmd = "screenshot"
    description = "Take a screenshot from the remote implant"
    version = 1
    author = "Spencer Adolph"
    argument_class = ScreenshotArguments
    attackmapping = []

    async def create_go_tasking(self, taskData: MythicCommandBase.PTTaskMessageAllData) -> MythicCommandBase.PTTaskCreateTaskingMessageResponse:
        # Command: screenshot
        # About: Take a screenshot from the remote implant.

        # Usage:
        # ======
        # screenshot [flags]

        # Flags:
        # ======
        # TODO: -h, --help              display help
        # TODO: -X, --loot              save output as loot
        # TODO: -n, --name    string    name to assign loot (optional)
        # TODO: -s, --save    string    save to file (will overwrite if exists)
        # TODO: -t, --timeout int       command timeout in seconds (default: 60)

        screenshot_results = await SliverAPI.screenshot(taskData)

        results = await SendMythicRPCFileCreate(MythicRPCFileCreateMessage(
            TaskID=taskData.Task.ID,
            RemotePathOnTarget="/tmp/this_is_weird",
            FileContents=screenshot_results,
            IsScreenshot=True,
            IsDownloadFromAgent=False,
            Filename="this_is_weird",
        ))

        await SendMythicRPCResponseCreate(MythicRPCResponseCreateMessage(
            TaskID=taskData.Task.ID,
            Response=f"agent file id == {results.AgentFileId}".encode("UTF8"),
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
