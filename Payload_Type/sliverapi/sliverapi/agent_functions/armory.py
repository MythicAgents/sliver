from ..SliverRequests import SliverAPI

from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *
from mythic_container.PayloadBuilder import *

# from sliver import common_pb2

class ArmoryArguments(TaskArguments):
    def __init__(self, command_line, **kwargs):
        super().__init__(command_line, **kwargs)
        self.args = []

    async def parse_arguments(self):
        pass


class Armory(CommandBase):
    cmd = "armory"
    needs_admin = False
    help_cmd = "armory"
    description = "Automatically download and install extensions/aliases"
    version = 1
    author = "Spencer Adolph"
    argument_class = ArmoryArguments
    attackmapping = []

    async def create_go_tasking(self, taskData: MythicCommandBase.PTTaskMessageAllData) -> MythicCommandBase.PTTaskCreateTaskingMessageResponse:
        # Automatically download and install extensions/aliases

        # Usage:
        # ======
        #   armory [flags]

        # Flags:
        # ======
        #        -h, --help                   display help
        # TODO:  -c, --ignore-cache           ignore metadata cache, force refresh
        # TODO:  -I, --insecure               skip tls certificate validation
        # TODO:  -p, --proxy        string    specify a proxy url (e.g. http://localhost:8080)
        #        -t, --timeout      string    download timeout (default: 15m)

        # Sub Commands:
        # =============
        # TODO:  install  Install an alias or extension
        # TODO:  search   Search for aliases and extensions by name (regex)
        # TODO:  update   Update installed an aliases and extensions

        response = await armory(taskData)

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


async def armory(taskData: PTTaskMessageAllData):
    # client = await SliverAPI.create_sliver_client(taskData)

    # armory_results = await client.armory()

    # TODO: match sliver formatting

    return "This command not yet implemented..."
