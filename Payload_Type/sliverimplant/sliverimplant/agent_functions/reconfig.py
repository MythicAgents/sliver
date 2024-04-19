from ..SliverRequests import SliverAPI

from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *
from mythic_container.PayloadBuilder import *

class ReconfigArguments(TaskArguments):
    def __init__(self, command_line, **kwargs):
        super().__init__(command_line, **kwargs)
        self.args = []

    async def parse_arguments(self):
        pass


class Reconfig(CommandBase):
    cmd = "reconfig"
    needs_admin = False
    help_cmd = "reconfig"
    description = "Reconfigure the active beacon/session"
    version = 1
    author = "Spencer Adolph"
    argument_class = ReconfigArguments
    attackmapping = []

    async def create_go_tasking(self, taskData: MythicCommandBase.PTTaskMessageAllData) -> MythicCommandBase.PTTaskCreateTaskingMessageResponse:
        # Reconfigure the active beacon/session

        # Usage:
        # ======
        #   reconfig [flags]

        # Flags:
        # ======
        # TODO:  -i, --beacon-interval    string    beacon callback interval
        # TODO:  -j, --beacon-jitter      string    beacon callback jitter (random up to)
        # TODO:  -h, --help                         display help
        # TODO:  -r, --reconnect-interval string    reconnect interval for implant
        # TODO:  -t, --timeout            int       command timeout in seconds (default: 60)

        response = await reconfig(taskData)

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

async def reconfig(taskData: PTTaskMessageAllData):
    # interact, isBeacon = await SliverAPI.create_sliver_interact(taskData)

    # ifconfig_results = await interact._stub()

    # if (isBeacon):
    #     ifconfig_results = await ifconfig_results

    return "This command not yet implemented..."
