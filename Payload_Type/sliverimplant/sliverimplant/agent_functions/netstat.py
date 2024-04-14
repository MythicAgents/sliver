from ..SliverRequests import SliverAPI

from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *
from mythic_container.PayloadBuilder import *

class NetstatArguments(TaskArguments):
    def __init__(self, command_line, **kwargs):
        super().__init__(command_line, **kwargs)
        self.args = []

    async def parse_arguments(self):
        pass


class Netstat(CommandBase):
    cmd = "netstat"
    needs_admin = False
    help_cmd = "netstat"
    description = "Print network connection information"
    version = 1
    author = "Spencer Adolph"
    argument_class = NetstatArguments
    attackmapping = []

    async def create_go_tasking(self, taskData: MythicCommandBase.PTTaskMessageAllData) -> MythicCommandBase.PTTaskCreateTaskingMessageResponse:
        # Print network connection information

        # Usage:
        # ======
        #   netstat [flags]

        # Flags:
        # ======
        # TODO:  -h, --help           display help
        # TODO:  -4, --ip4            display information about IPv4 sockets
        # TODO:  -6, --ip6            display information about IPv6 sockets
        # TODO:  -l, --listen         display information about listening sockets
        # TODO:  -n, --numeric        display numeric addresses (disable hostname resolution)
        # TODO:  -T, --tcp            display information about TCP sockets
        # TODO:  -t, --timeout int    command timeout in seconds (default: 60)
        # TODO:  -u, --udp            display information about UDP sockets

        netstat_results = await SliverAPI.netstat(taskData)

        await SendMythicRPCResponseCreate(MythicRPCResponseCreateMessage(
            TaskID=taskData.Task.ID,
            Response=f"{str(netstat_results)}".encode("UTF8"),
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
