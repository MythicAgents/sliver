from ..SliverRequests import SliverAPI

from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *
from mythic_container.PayloadBuilder import *

from sliver import sliver_pb2, client_pb2

class InteractiveArguments(TaskArguments):
    def __init__(self, command_line, **kwargs):
        super().__init__(command_line, **kwargs)
        self.args = []

    async def parse_arguments(self):
        pass


class Interactive(CommandBase):
    cmd = "interactive"
    needs_admin = False
    help_cmd = "interactive"
    description = "Task a beacon to open an interactive session (Beacon only)"
    version = 1
    author = "Spencer Adolph"
    argument_class = InteractiveArguments
    attackmapping = []

    async def create_go_tasking(self, taskData: MythicCommandBase.PTTaskMessageAllData) -> MythicCommandBase.PTTaskCreateTaskingMessageResponse:
        # Task a beacon to open an interactive session (Beacon only)

        # Usage:
        # ======
        #   interactive [flags]

        # Flags:
        # ======
        # TODO:  -d, --delay      string    delay opening the session (after checkin) for a given period of time (default: 0s)
        # TODO:  -n, --dns        string    dns connection strings
        # TODO:  -h, --help                 display help
        # TODO:  -b, --http       string    http(s) connection strings
        # TODO:  -m, --mtls       string    mtls connection strings
        # TODO:  -p, --named-pipe string    namedpipe connection strings
        # TODO:  -i, --tcp-pivot  string    tcppivot connection strings
        # TODO:  -t, --timeout    int       command timeout in seconds (default: 60)
        # TODO:  -g, --wg         string    wg connection strings

        response = await interactive(taskData)

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

async def interactive(taskData: PTTaskMessageAllData):
    interact, isBeacon = await SliverAPI.create_sliver_interact(taskData)

    if (not isBeacon):
        return "Beacon Only..."

    # TODO: figure out how to wait for task to complete, or decide if don't worry about it
    interactive_results = await interact._stub.OpenSession(interact._request(sliver_pb2.OpenSession()))

    return "Tasked to create an interactive session!"
