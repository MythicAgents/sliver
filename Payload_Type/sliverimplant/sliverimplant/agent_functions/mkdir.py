from ..SliverRequests import SliverAPI


from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *
from mythic_container.PayloadBuilder import *

class MkdirArguments(TaskArguments):
    def __init__(self, command_line, **kwargs):
        super().__init__(command_line, **kwargs)
        self.args = [
            CommandParameter(
                name="path",
                description="path to create dir",
                type=ParameterType.String
            ),
        ]

    async def parse_arguments(self):
        self.load_args_from_json_string(self.command_line)


class Mkdir(CommandBase):
    cmd = "mkdir"
    needs_admin = False
    help_cmd = "mkdir"
    description = "make directory"
    version = 1
    author = "Spencer Adolph"
    argument_class = MkdirArguments
    attackmapping = []

    async def create_go_tasking(self, taskData: MythicCommandBase.PTTaskMessageAllData) -> MythicCommandBase.PTTaskCreateTaskingMessageResponse:
        # Command: mkdir [remote path]
        # About: Create a remote directory.

        # Usage:
        # ======
        #   mkdir [flags] path

        # Args:
        # =====
        #   path  string    path to the directory to create

        # Flags:
        # ======
        #        -h, --help           display help
        #        -t, --timeout int    command timeout in seconds (default: 60)

        mkdir_results = await mkdir(taskData)

        await SendMythicRPCResponseCreate(MythicRPCResponseCreateMessage(
            TaskID=taskData.Task.ID,
            Response=f"{str(mkdir_results)}".encode("UTF8"),
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


async def mkdir(taskData: PTTaskMessageAllData):
    interact, isBeacon = await SliverAPI.create_sliver_interact(taskData)

    # TODO: get these from function parameters and extract in the parent function instead
    remote_path = taskData.args.get_arg('path')

    mkdir_results = await interact.mkdir(remote_path=remote_path)

    if (isBeacon):
        mkdir_results = await mkdir_results

    return mkdir_results
