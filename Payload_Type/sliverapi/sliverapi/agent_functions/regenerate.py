from ..SliverRequests import SliverAPI

from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *
from mythic_container.PayloadBuilder import *

# from sliver import common_pb2

class RegenerateArguments(TaskArguments):
    def __init__(self, command_line, **kwargs):
        super().__init__(command_line, **kwargs)
        self.args = []

    async def parse_arguments(self):
        pass


class Regenerate(CommandBase):
    cmd = "regenerate"
    needs_admin = False
    help_cmd = "regenerate"
    description = "Regenerate an implant"
    version = 1
    author = "Spencer Adolph"
    argument_class = RegenerateArguments
    attackmapping = []

    async def create_go_tasking(self, taskData: MythicCommandBase.PTTaskMessageAllData) -> MythicCommandBase.PTTaskCreateTaskingMessageResponse:
        # Regenerate an implant

        # Usage:
        # ======
        #   regenerate [flags] implant-name

        # Args:
        # =====
        #   implant-name  string    name of the implant

        # Flags:
        # ======
        # TODO:  -h, --help              display help
        # TODO:  -s, --save    string    directory/file to the binary to
        # TODO:  -t, --timeout int       command timeout in seconds (default: 60)

        response = await regenerate(taskData)

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


async def regenerate(taskData: PTTaskMessageAllData):
    # client = await SliverAPI.create_sliver_client(taskData)

    # regenerate_result = await client.regenerate_implant()

    # TODO: match sliver formatting

    return "This command not yet implemented..."
