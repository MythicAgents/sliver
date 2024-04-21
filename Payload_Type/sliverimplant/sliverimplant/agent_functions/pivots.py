from ..SliverRequests import SliverAPI

from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *
from mythic_container.PayloadBuilder import *

class PivotsArguments(TaskArguments):
    def __init__(self, command_line, **kwargs):
        super().__init__(command_line, **kwargs)
        self.args = []

    async def parse_arguments(self):
        pass


class Pivots(CommandBase):
    cmd = "pivots"
    needs_admin = False
    help_cmd = "pivots"
    description = "List pivots for the current session"
    version = 1
    author = "Spencer Adolph"
    argument_class = PivotsArguments
    attackmapping = []

    async def create_go_tasking(self, taskData: MythicCommandBase.PTTaskMessageAllData) -> MythicCommandBase.PTTaskCreateTaskingMessageResponse:
        # Command: pivots
        # About: List pivots for the current session. NOTE: pivots are only supported on sessions, not beacons.

        # Usage:
        # ======
        #   pivots [flags]

        # Flags:
        # ======
        #        -h, --help           display help
        #        -t, --timeout int    command timeout in seconds (default: 60)

        # Sub Commands:
        # =============
        # TODO:  details     Get details of a pivot listener
        # TODO:  graph       Get details of a pivot listener
        # TODO:  named-pipe  Start a named pipe pivot listener
        # TODO:  stop        Stop a pivot listener
        # TODO:  tcp         Start a TCP pivot listener

        response = await pivots(taskData)

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

async def pivots(taskData: PTTaskMessageAllData):
    # interact, isBeacon = await SliverAPI.create_sliver_interact(taskData)

    # ifconfig_results = await interact._stub()

    # if (isBeacon):
    #     ifconfig_results = await ifconfig_results

    return "This command not yet implemented..."
