from ..SliverRequests import SliverAPI

from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *
from mythic_container.PayloadBuilder import *

# from sliver import common_pb2

class OperatorsArguments(TaskArguments):
    def __init__(self, command_line, **kwargs):
        super().__init__(command_line, **kwargs)
        self.args = []

    async def parse_arguments(self):
        pass


class Operators(CommandBase):
    cmd = "operators"
    needs_admin = False
    help_cmd = "operators"
    description = "Manage operators"
    version = 1
    author = "Spencer Adolph"
    argument_class = OperatorsArguments
    attackmapping = []

    async def create_go_tasking(self, taskData: MythicCommandBase.PTTaskMessageAllData) -> MythicCommandBase.PTTaskCreateTaskingMessageResponse:
        # Manage operators

        # Usage:
        # ======
        #   operators [flags]

        # Flags:
        # ======
        # TODO:  -h, --help           display help
        # TODO:  -t, --timeout int    command timeout in seconds (default: 60)

        response = await operators(taskData)

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


async def operators(taskData: PTTaskMessageAllData):
    client = await SliverAPI.create_sliver_client(taskData)

    operators_results = await client.operators()

    # TODO: match sliver formatting

    return f"{operators_results}"
