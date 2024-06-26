from ..SliverRequests import SliverAPI

from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *
from mythic_container.PayloadBuilder import *

from sliver import sliver_pb2

class PwdArguments(TaskArguments):
    def __init__(self, command_line, **kwargs):
        super().__init__(command_line, **kwargs)
        self.args = []

    async def parse_arguments(self):
        pass


class Pwd(CommandBase):
    cmd = "pwd"
    needs_admin = False
    help_cmd = "pwd"
    description = "Print working directory of the active session."
    version = 1
    author = "Spencer Adolph"
    argument_class = PwdArguments
    attackmapping = []

    async def create_go_tasking(self, taskData: MythicCommandBase.PTTaskMessageAllData) -> MythicCommandBase.PTTaskCreateTaskingMessageResponse: 
        # Command: pwd
        # About: Print working directory of the active session.

        # Usage:
        # ======
        #   pwd [flags]

        # Flags:
        # ======
        #        -h, --help           display help
        #        -t, --timeout int    command timeout in seconds (default: 60)
       
        response = await pwd(taskData)

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


async def pwd(taskData: PTTaskMessageAllData):
    interact, isBeacon = await SliverAPI.create_sliver_interact(taskData)

    pwd_results = await interact.pwd()

    # pwd_results = await interact._stub.Pwd(interact._request(sliver_pb2.PwdReq()))

    if (isBeacon):
        pwd_results = await pwd_results

    return f"{pwd_results}"

