from ..SliverRequests import SliverAPI

from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *
from mythic_container.PayloadBuilder import *

class MtlsArguments(TaskArguments):
    def __init__(self, command_line, **kwargs):
        super().__init__(command_line, **kwargs)
        self.args = [
            CommandParameter(
                name="lport",
                cli_name="l",
                display_name="lport",
                description="tcp listen port (default: 8888)",
                default_value=8888,
                type=ParameterType.Number
            ),
        ]

    async def parse_arguments(self):
        self.load_args_from_json_string(self.command_line)


class Mtls(CommandBase):
    cmd = "mtls"
    needs_admin = False
    help_cmd = "mtls"
    description = "Start an mTLS listener"
    version = 1
    author = "Spencer Adolph"
    argument_class = MtlsArguments
    attackmapping = []

    async def create_go_tasking(self, taskData: MythicCommandBase.PTTaskMessageAllData) -> MythicCommandBase.PTTaskCreateTaskingMessageResponse:
        # Start an mTLS listener

        # Usage:
        # ======
        #   mtls [flags]

        # Flags:
        # ======
        # TODO:  -h, --help                 display help
        # TODO:  -L, --lhost      string    interface to bind server to
        #        -l, --lport      int       tcp listen port (default: 8888)
        # TODO:  -p, --persistent           make persistent across restarts
        # TODO:  -t, --timeout    int       command timeout in seconds (default: 60)

        # 'mtls -l <port>'
        port = taskData.args.get_arg('lport')
        response = await SliverAPI.mtls_start(taskData, port)
        
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
