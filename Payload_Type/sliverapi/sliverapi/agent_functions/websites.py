from ..SliverRequests import SliverAPI

from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *
from mythic_container.PayloadBuilder import *

# from sliver import common_pb2

class WebsitesArguments(TaskArguments):
    def __init__(self, command_line, **kwargs):
        super().__init__(command_line, **kwargs)
        self.args = []

    async def parse_arguments(self):
        pass


class Websites(CommandBase):
    cmd = "websites"
    needs_admin = False
    help_cmd = "websites"
    description = "Add content to HTTP(S) C2 websites to make them look more legit"
    version = 1
    author = "Spencer Adolph"
    argument_class = WebsitesArguments
    attackmapping = []

    async def create_go_tasking(self, taskData: MythicCommandBase.PTTaskMessageAllData) -> MythicCommandBase.PTTaskCreateTaskingMessageResponse:
        # Command: websites <options> <operation>
        # About: Add content to HTTP(S) C2 websites to make them look more legit.

        # Usage:
        # ======
        #   websites [flags] [name]

        # Args:
        # =====
        #   name  string    website name

        # Flags:
        # ======
        # TODO:  -h, --help           display help
        # TODO:  -t, --timeout int    command timeout in seconds (default: 60)

        # Sub Commands:
        # =============
        # TODO:  add-content   Add content to a website
        # TODO:  content-type  Update a path's content-type
        # TODO:  rm            Remove an entire website and all of its contents
        # TODO:  rm-content    Remove specific content from a website

        response = await websites(taskData)

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


async def websites(taskData: PTTaskMessageAllData):
    client = await SliverAPI.create_sliver_client(taskData)

    websites_results = await client.websites()

    # TODO: match sliver formatting

    return f"{websites_results}"
