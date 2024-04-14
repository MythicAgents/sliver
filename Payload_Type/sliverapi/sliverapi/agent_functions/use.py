from ..SliverRequests import SliverAPI

from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *
from mythic_container.PayloadBuilder import *

class UseArguments(TaskArguments):
    def __init__(self, command_line, **kwargs):
        super().__init__(command_line, **kwargs)
        self.args = [
            CommandParameter(
                name="id",
                description="beacon or session ID",
                type=ParameterType.String
            ),
        ]

    async def parse_arguments(self):
        self.load_args_from_json_string(self.command_line)


class Use(CommandBase):
    cmd = "use"
    needs_admin = False
    help_cmd = "use"
    description = "Use an implant."
    version = 1
    author = "Spencer Adolph"
    argument_class = UseArguments
    attackmapping = []

    async def create_go_tasking(self, taskData: MythicCommandBase.PTTaskMessageAllData) -> MythicCommandBase.PTTaskCreateTaskingMessageResponse:
        # Command: use [sliver name/session]
        # About: Switch the active Sliver, a valid name must be provided (see sessions).

        # Usage:
        # ======
        #   use [flags] [id]

        # Args:
        # =====
        #   id  string    beacon or session ID

        # Flags:
        # ======
        # TODO:  -h, --help           display help
        # TODO:  -t, --timeout int    command timeout in seconds (default: 60)

        # Sub Commands:
        # =============
        # TODO:  beacons   Switch the active beacon
        # TODO:  sessions  Switch the active session

        sliver_id = taskData.args.get_arg('id')
        response = await SliverAPI.use(taskData, sliver_id)

        await SendMythicRPCResponseCreate(MythicRPCResponseCreateMessage(
            TaskID=taskData.Task.ID,
            Response=response.encode("UTF8"),
        ))
        
        taskResponse = MythicCommandBase.PTTaskCreateTaskingMessageResponse(
            TaskID=taskData.Task.ID,
            Success=True,
            Completed=True,
            TaskStatus="success" if response[1] != '!' else "not found",  # TODO: don't hard code response[1], handle with try/catch errors
        )

        return taskResponse

    async def process_response(self, task: PTTaskMessageAllData, response: any) -> PTTaskProcessResponseMessageResponse:
        resp = PTTaskProcessResponseMessageResponse(TaskID=task.Task.ID, Success=True)
        return resp
