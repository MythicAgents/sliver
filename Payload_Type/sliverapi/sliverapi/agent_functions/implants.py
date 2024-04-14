from ..SliverRequests import SliverAPI

from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *
from mythic_container.PayloadBuilder import *

class ImplantsArguments(TaskArguments):
    def __init__(self, command_line, **kwargs):
        super().__init__(command_line, **kwargs)
        self.args = []

    async def parse_arguments(self):
        pass


class Implants(CommandBase):
    cmd = "implants"
    needs_admin = False
    help_cmd = "implants"
    description = "Get the list of implants that Sliver is aware of."
    version = 1
    author = "Spencer Adolph"
    argument_class = ImplantsArguments
    attackmapping = []

    async def create_go_tasking(self, taskData: MythicCommandBase.PTTaskMessageAllData) -> MythicCommandBase.PTTaskCreateTaskingMessageResponse:
        # List implant builds

        # Usage:
        # ======
        #   implants [flags]

        # Flags:
        # ======
        # TODO:  -a, --arch          string    filter builds by cpu architecture
        # TODO:  -f, --format        string    filter builds by artifact format
        # TODO:  -h, --help                    display help
        # TODO:  -d, --no-debug                filter builds by debug flag
        # TODO:  -b, --only-beacons            filter beacons
        # TODO:  -s, --only-sessions           filter interactive sessions
        # TODO:  -o, --os            string    filter builds by operating system
        # TODO:  -t, --timeout       int       command timeout in seconds (default: 60)

        # Sub Commands:
        # =============
        # TODO:  rm  Remove implant build

        # 'implants' with no options
        response = await SliverAPI.implants_list(taskData)

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
