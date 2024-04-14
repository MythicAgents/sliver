from ..SliverRequests import SliverAPI

from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *
from mythic_container.PayloadBuilder import *

class TerminateArguments(TaskArguments):
    def __init__(self, command_line, **kwargs):
        super().__init__(command_line, **kwargs)
        self.args = [
            CommandParameter(
                name="process_id",
                description="pid to kill",
                type=ParameterType.Number
            ),
        ]

    async def parse_arguments(self):
        self.load_args_from_json_string(self.command_line)


class Terminate(CommandBase):
    cmd = "terminate"
    needs_admin = False
    help_cmd = "terminate"
    description = "Kills a remote process designated by PID"
    version = 1
    author = "Spencer Adolph"
    argument_class = TerminateArguments
    attackmapping = []
    supported_ui_features = ['process_browser:kill']

    async def create_go_tasking(self, taskData: MythicCommandBase.PTTaskMessageAllData) -> MythicCommandBase.PTTaskCreateTaskingMessageResponse:
        # Command: terminate PID
        # About: Kills a remote process designated by PID

        # Usage:
        # ======
        #   terminate [flags] pid

        # Args:
        # =====
        #   pid  uint    pid

        # Flags:
        # ======
        # TODO:  -F, --force          disregard safety and kill the PID
        # TODO:  -h, --help           display help
        # TODO:  -t, --timeout int    command timeout in seconds (default: 60)

        pid_to_kill = taskData.args.get_arg('process_id')
        response = await SliverAPI.terminate(taskData, pid_to_kill)

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
