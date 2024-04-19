from ..SliverRequests import SliverAPI

from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *
from mythic_container.PayloadBuilder import *

class Socks5Arguments(TaskArguments):
    def __init__(self, command_line, **kwargs):
        super().__init__(command_line, **kwargs)
        self.args = []

    async def parse_arguments(self):
        pass


class Socks5(CommandBase):
    cmd = "socks5"
    needs_admin = False
    help_cmd = "socks5"
    description = "In-band SOCKS5 Proxy"
    version = 1
    author = "Spencer Adolph"
    argument_class = Socks5Arguments
    attackmapping = []

    async def create_go_tasking(self, taskData: MythicCommandBase.PTTaskMessageAllData) -> MythicCommandBase.PTTaskCreateTaskingMessageResponse:
        # In-band SOCKS5 Proxy

        # Usage:
        # ======
        #   socks5 [flags]

        # Flags:
        # ======
        # TODO:  -h, --help           display help
        # TODO:  -t, --timeout int    router timeout in seconds (default: 60)

        # Sub Commands:
        # =============
        # TODO:  start  Start an in-band SOCKS5 proxy
        # TODO:  stop   Stop a SOCKS5 proxy

        response = await socks5(taskData)

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

async def socks5(taskData: PTTaskMessageAllData):
    # interact, isBeacon = await SliverAPI.create_sliver_interact(taskData)

    # ifconfig_results = await interact._stub()

    # if (isBeacon):
    #     ifconfig_results = await ifconfig_results

    return "This command not yet implemented..."
