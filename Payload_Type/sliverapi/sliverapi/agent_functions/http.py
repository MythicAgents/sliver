from ..SliverRequests import SliverAPI

from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *
from mythic_container.PayloadBuilder import *

# from sliver import common_pb2

class HttpArguments(TaskArguments):
    def __init__(self, command_line, **kwargs):
        super().__init__(command_line, **kwargs)
        self.args = []

    async def parse_arguments(self):
        pass


class Http(CommandBase):
    cmd = "http"
    needs_admin = False
    help_cmd = "http"
    description = "Start an HTTP listener"
    version = 1
    author = "Spencer Adolph"
    argument_class = HttpArguments
    attackmapping = []

    async def create_go_tasking(self, taskData: MythicCommandBase.PTTaskMessageAllData) -> MythicCommandBase.PTTaskCreateTaskingMessageResponse:
        # Start an HTTP listener

        # Usage:
        # ======
        #   http [flags]

        # Flags:
        # ======
        # TODO:  -D, --disable-otp                 disable otp authentication
        # TODO:  -d, --domain            string    limit responses to specific domain
        #        -h, --help                        display help
        # TODO:  -L, --lhost             string    interface to bind server to
        # TODO:  -J, --long-poll-jitter  string    server-side long poll jitter (default: 2s)
        # TODO:  -T, --long-poll-timeout string    server-side long poll timeout (default: 1s)
        # TODO:  -l, --lport             int       tcp listen port (default: 80)
        # TODO:  -p, --persistent                  make persistent across restarts
        #        -t, --timeout           int       command timeout in seconds (default: 60)
        # TODO:  -w, --website           string    website name (see websites cmd)

        response = await http(taskData)

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


async def http(taskData: PTTaskMessageAllData):
    client = await SliverAPI.create_sliver_client(taskData)

    http_result = await client.start_http_listener()

    # TODO: match sliver formatting

    return f"{http_result}"
