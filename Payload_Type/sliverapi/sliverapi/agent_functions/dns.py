from ..SliverRequests import SliverAPI

from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *
from mythic_container.PayloadBuilder import *


class DnsArguments(TaskArguments):
    def __init__(self, command_line, **kwargs):
        super().__init__(command_line, **kwargs)
        self.args = []

    async def parse_arguments(self):
        pass


class Dns(CommandBase):
    cmd = "dns"
    needs_admin = False
    help_cmd = "dns"
    description = "Start a DNS listener"
    version = 1
    author = "Spencer Adolph"
    argument_class = DnsArguments
    attackmapping = []

    async def create_go_tasking(self, taskData: MythicCommandBase.PTTaskMessageAllData) -> MythicCommandBase.PTTaskCreateTaskingMessageResponse:
        # Start a DNS listener

        # Usage:
        # ======
        #   dns [flags]

        # Flags:
        # ======
        # TODO:  -D, --disable-otp           disable otp authentication
        # TODO:  -d, --domains     string    parent domain(s) to use for DNS c2
        # TODO:  -h, --help                  display help
        # TODO:  -L, --lhost       string    interface to bind server to
        # TODO:  -l, --lport       int       udp listen port (default: 53)
        # TODO:  -c, --no-canaries           disable dns canary detection
        # TODO:  -p, --persistent            make persistent across restarts
        # TODO:  -t, --timeout     int       command timeout in seconds (default: 60)

        response = await dns(taskData)

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


async def dns(taskData: PTTaskMessageAllData):
    client = await SliverAPI.create_sliver_client(taskData)

    dns_results = await client.start_dns_listener(domains=['1.example.com.'], host='192.168.17.129')

    # TODO: match sliver formatting

    return f"{dns_results}"
