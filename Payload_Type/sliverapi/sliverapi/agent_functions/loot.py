from ..SliverRequests import SliverAPI

from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *
from mythic_container.PayloadBuilder import *

# from sliver import common_pb2

class LootArguments(TaskArguments):
    def __init__(self, command_line, **kwargs):
        super().__init__(command_line, **kwargs)
        self.args = []

    async def parse_arguments(self):
        pass


class Loot(CommandBase):
    cmd = "loot"
    needs_admin = False
    help_cmd = "loot"
    description = "Store and share loot between operators"
    version = 1
    author = "Spencer Adolph"
    argument_class = LootArguments
    attackmapping = []

    async def create_go_tasking(self, taskData: MythicCommandBase.PTTaskMessageAllData) -> MythicCommandBase.PTTaskCreateTaskingMessageResponse:
        # Command: loot
        # About: Store and share loot between operators.

        # Usage:
        # ======
        #   loot [flags]

        # Flags:
        # ======
        # TODO:  -f, --filter  string    filter based on loot type
        # TODO:  -h, --help              display help
        # TODO:  -t, --timeout int       command timeout in seconds (default: 60)

        # Sub Commands:
        # =============
        # TODO:  creds   Add credentials to the server's loot store
        # TODO:  fetch   Fetch a piece of loot from the server's loot store
        # TODO:  local   Add a local file to the server's loot store
        # TODO:  remote  Add a remote file from the current session to the server's loot store
        # TODO:  rename  Re-name a piece of existing loot
        # TODO:  rm      Remove a piece of loot from the server's loot store

        response = await loot(taskData)

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


async def loot(taskData: PTTaskMessageAllData):
    # client = await SliverAPI.create_sliver_client(taskData)

    # loot_results = await client._stub.lootall()

    # TODO: match sliver formatting

    return "This command not yet implemented..."
