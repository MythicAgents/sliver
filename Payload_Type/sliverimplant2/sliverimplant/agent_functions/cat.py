from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *
from mythic_container.PayloadBuilder import *

import gzip

from sliver import InteractiveBeacon
from ..utils.sliver_connect import sliver_implant_clients

class CatArguments(TaskArguments):
    def __init__(self, command_line, **kwargs):
        super().__init__(command_line, **kwargs)
        self.args = [
            CommandParameter(
                name="remote_path",
                description="path to file",
                type=ParameterType.String
            ),
        ]

    async def parse_arguments(self):
        self.load_args_from_json_string(self.command_line)

class Cat(CommandBase):
    cmd = "cat"
    needs_admin = False
    help_cmd = "cat"
    description = "cat a file (doesn't download)"
    version = 1
    author = "Spencer Adolph"
    argument_class = CatArguments
    attackmapping = []

    async def create_go_tasking(self, taskData: MythicCommandBase.PTTaskMessageAllData) -> MythicCommandBase.PTTaskCreateTaskingMessageResponse:
        await cat(taskData)

        taskResponse = MythicCommandBase.PTTaskCreateTaskingMessageResponse(
            TaskID=taskData.Task.ID,
            Success=True,
            Completed=True
        )
        return taskResponse

    async def process_response(self, task: PTTaskMessageAllData, response: any) -> PTTaskProcessResponseMessageResponse:
        resp = PTTaskProcessResponseMessageResponse(TaskID=task.Task.ID, Success=True)
        return resp

async def cat(taskData: PTTaskMessageAllData):
    interact = sliver_implant_clients[f"{taskData.Payload.UUID}"]

    remote_path = taskData.args.get_arg('remote_path')

    download_results = await interact.download(remote_path=remote_path)

    if (isinstance(interact, InteractiveBeacon)):
        await SendMythicRPCResponseCreate(MythicRPCResponseCreateMessage(
            TaskID=taskData.Task.ID,
            Response="issued task, awaiting results\n".encode("UTF8"),
        ))
        download_results = await download_results

    plaintext = gzip.decompress(download_results.Data)

    await SendMythicRPCResponseCreate(MythicRPCResponseCreateMessage(
        TaskID=taskData.Task.ID,
        Response=f"{plaintext.decode('utf-8')}".encode("UTF8"),
    ))
