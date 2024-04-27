from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *
from mythic_container.PayloadBuilder import *

from ..utils.sliver_connect import sliver_server_clients

class MtlsArguments(TaskArguments):
    def __init__(self, command_line, **kwargs):
        super().__init__(command_line, **kwargs)
        self.args = [
            CommandParameter(
                name="lhost",
                cli_name="lhost",
                display_name="lhost",
                description="interface to bind server to",
                type=ParameterType.String,
                default_value='0.0.0.0'
            ),
            CommandParameter(
                name="lport",
                cli_name="lport",
                display_name="lport",
                description="tcp listen port",
                type=ParameterType.Number,
                default_value=8888
            ),
            CommandParameter(
                name="persistent",
                cli_name="persistent",
                display_name="persistent",
                description="make persistent across restarts",
                type=ParameterType.Boolean,
                default_value=False
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
        await mtls_start(taskData)
        
        taskResponse = MythicCommandBase.PTTaskCreateTaskingMessageResponse(
            TaskID=taskData.Task.ID,
            Success=True,
            Completed=True
        )
        return taskResponse

    async def process_response(self, task: PTTaskMessageAllData, response: any) -> PTTaskProcessResponseMessageResponse:
        resp = PTTaskProcessResponseMessageResponse(TaskID=task.Task.ID, Success=True)
        return resp


async def mtls_start(taskData: PTTaskMessageAllData):
    lhost = taskData.args.get_arg('lhost')
    lport = taskData.args.get_arg('lport')
    persistent = taskData.args.get_arg('persistent')

    client = sliver_server_clients[f"{taskData.Payload.UUID}"]

    job_id = await client.start_mtls_listener(
        host=lhost,
        port=lport,
        persistent=persistent,
    )

    await SendMythicRPCResponseCreate(MythicRPCResponseCreateMessage(
        TaskID=taskData.Task.ID,
        Response=f"[*] Successfully started job #{job_id}".encode("UTF8"),
    ))
