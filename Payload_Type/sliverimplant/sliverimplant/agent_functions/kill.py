from ..SliverRequests import SliverAPI

from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *
from mythic_container.PayloadBuilder import *

from sliver import sliver_pb2, client_pb2


class KillArguments(TaskArguments):
    def __init__(self, command_line, **kwargs):
        super().__init__(command_line, **kwargs)
        self.args = []

    async def parse_arguments(self):
        pass


class Kill(CommandBase):
    cmd = "kill"
    needs_admin = False
    help_cmd = "kill"
    description = "Kill a remote implant process (does not delete file)"
    version = 1
    author = "Spencer Adolph"
    argument_class = KillArguments
    attackmapping = []

    async def create_go_tasking(self, taskData: MythicCommandBase.PTTaskMessageAllData) -> MythicCommandBase.PTTaskCreateTaskingMessageResponse:
        # Command: kill <implant name/session>
        # About: Kill a remote implant process (does not delete file).

        # Usage:
        # ======
        #   kill [flags]

        # Flags:
        # ======
        # TODO:  -F, --force          Force kill,  does not clean up
        #        -h, --help           display help
        #        -t, --timeout int    command timeout in seconds (default: 60)

        response = await kill(taskData)

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

async def kill(taskData: PTTaskMessageAllData):
    interact, isBeacon = await SliverAPI.create_sliver_interact(taskData)

    # TODO: not sure how to wait for this
    kill_results = await interact._stub.Kill(interact._request(sliver_pb2.KillReq()))

    # if (isBeacon):
    #     kill_results = await kill_results

    return "Tasked Kill!"
