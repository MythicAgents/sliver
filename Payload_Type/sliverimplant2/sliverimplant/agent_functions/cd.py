from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *
from mythic_container.PayloadBuilder import *

from sliver import InteractiveBeacon
from ..utils.sliver_connect import sliver_implant_clients

class CdArguments(TaskArguments):
    def __init__(self, command_line, **kwargs):
        super().__init__(command_line, **kwargs)
        self.args = [
            CommandParameter(
                name="remote_path",
                description="path to the directory",
                type=ParameterType.String
            ),
        ]

    async def parse_arguments(self):
        self.load_args_from_json_string(self.command_line)

class Cd(CommandBase):
    cmd = "cd"
    needs_admin = False
    help_cmd = "cd"
    description = "Change directories"
    version = 1
    author = "Spencer Adolph"
    argument_class = CdArguments
    attackmapping = []

    async def create_go_tasking(self, taskData: MythicCommandBase.PTTaskMessageAllData) -> MythicCommandBase.PTTaskCreateTaskingMessageResponse:
        await cd(taskData)

        taskResponse = MythicCommandBase.PTTaskCreateTaskingMessageResponse(
            TaskID=taskData.Task.ID,
            Success=True,
            Completed=True
        )
        return taskResponse

    async def process_response(self, task: PTTaskMessageAllData, response: any) -> PTTaskProcessResponseMessageResponse:
        resp = PTTaskProcessResponseMessageResponse(TaskID=task.Task.ID, Success=True)
        return resp

async def cd(taskData: PTTaskMessageAllData):
    interact = sliver_implant_clients[f"{taskData.Payload.UUID}"]

    remote_path = taskData.args.get_arg('remote_path')

    cd_results = await interact.cd(remote_path=remote_path)

    if (isinstance(interact, InteractiveBeacon)):
        await SendMythicRPCResponseCreate(MythicRPCResponseCreateMessage(
            TaskID=taskData.Task.ID,
            Response="issued task, awaiting results\n".encode("UTF8"),
        ))
        cd_results = await cd_results

    await SendMythicRPCResponseCreate(MythicRPCResponseCreateMessage(
        TaskID=taskData.Task.ID,
        Response=f"{cd_results}".encode("UTF8"),
    ))
