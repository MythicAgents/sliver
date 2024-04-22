from ..SliverRequests import SliverAPI

from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *
from mythic_container.PayloadBuilder import *

# from sliver import common_pb2

class WgArguments(TaskArguments):
    def __init__(self, command_line, **kwargs):
        super().__init__(command_line, **kwargs)
        self.args = [
            # CommandParameter(
            #     name="n_port",
            #     cli_name="n_port",
            #     display_name="n_port",
            #     description="virtual tun interface listen port",
            #     type=ParameterType.Number
            # ),
        ]

    async def parse_arguments(self):
        self.load_args_from_json_string(self.command_line)


class Wg(CommandBase):
    cmd = "wg"
    needs_admin = False
    help_cmd = "wg"
    description = "Start a WireGuard listener"
    version = 1
    author = "Spencer Adolph"
    argument_class = WgArguments
    attackmapping = []

    async def create_go_tasking(self, taskData: MythicCommandBase.PTTaskMessageAllData) -> MythicCommandBase.PTTaskCreateTaskingMessageResponse:
        # Start a WireGuard listener

        # Usage:
        # ======
        #   wg [flags]

        # Flags:
        # ======
        #        -h, --help                 display help
        # TODO:  -x, --key-port   int       virtual tun interface key exchange port (default: 1337)
        # TODO:  -L, --lhost      string    interface to bind server to
        # TODO:  -l, --lport      int       udp listen port (default: 53)
        # TODO:  -n, --nport      int       virtual tun interface listen port (default: 8888)
        # TODO:  -p, --persistent           make persistent across restarts
        #        -t, --timeout    int       command timeout in seconds (default: 60)

        # n_port = taskData.args.get_arg('n_port')
        response = await wireguard(taskData)

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


async def wireguard(taskData: PTTaskMessageAllData):
    client = await SliverAPI.create_sliver_client(taskData)

    start_wg_listener_results = await client.start_wg_listener(tun_ip='0.0.0.0')

    # TODO: match sliver formatting

    return f"{start_wg_listener_results}"
