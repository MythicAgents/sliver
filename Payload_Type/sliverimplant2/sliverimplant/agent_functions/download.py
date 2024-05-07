from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *
from mythic_container.PayloadBuilder import *

import gzip

from sliver import InteractiveBeacon
from ..utils.sliver_connect import sliver_implant_clients

class DownloadArguments(TaskArguments):
    def __init__(self, command_line, **kwargs):
        super().__init__(command_line, **kwargs)
        self.args = [
            CommandParameter(
                name="remote_path",
                description="path to file",
                type=ParameterType.String
            ),
            # TODO: recurse parameter
        ]

    async def parse_arguments(self):
        self.load_args_from_json_string(self.command_line)

class Download(CommandBase):
    cmd = "download"
    needs_admin = False
    help_cmd = "download"
    description = "Download a file"
    version = 1
    author = "Spencer Adolph"
    argument_class = DownloadArguments
    attackmapping = []
    supported_ui_features = ["file_browser:download"]

    async def create_go_tasking(self, taskData: MythicCommandBase.PTTaskMessageAllData) -> MythicCommandBase.PTTaskCreateTaskingMessageResponse:
        await download(taskData)

        taskResponse = MythicCommandBase.PTTaskCreateTaskingMessageResponse(
            TaskID=taskData.Task.ID,
            Success=True,
            Completed=True
        )
        return taskResponse

    async def process_response(self, task: PTTaskMessageAllData, response: any) -> PTTaskProcessResponseMessageResponse:
        resp = PTTaskProcessResponseMessageResponse(TaskID=task.Task.ID, Success=True)
        return resp

async def download(taskData: PTTaskMessageAllData):
    interact = sliver_implant_clients[f"{taskData.Payload.UUID}"]

    remote_path = taskData.args.get_arg('remote_path')

    download_results = await interact.download(remote_path=remote_path)

    if (isinstance(interact, InteractiveBeacon)):
        await SendMythicRPCResponseCreate(MythicRPCResponseCreateMessage(
            TaskID=taskData.Task.ID,
            Response="issued task, awaiting results\n".encode("UTF8"),
        ))
        download_results = await download_results

    unzipped_data = gzip.decompress(download_results.Data)

    # TODO: update the file browser and indicate it was downloaded?
    results = await SendMythicRPCFileCreate(MythicRPCFileCreateMessage(
        TaskID=taskData.Task.ID,
        RemotePathOnTarget=remote_path,
        FileContents=unzipped_data,
        IsScreenshot=False,
        IsDownloadFromAgent=True,
        Filename=f"{remote_path}.tar.gz" if download_results.IsDir else remote_path
        # Filename=taskData.args.get_arg('remote_path').split('/')[-1],
    ))

    # TODO: browser script to download button
    await SendMythicRPCResponseCreate(MythicRPCResponseCreateMessage(
        TaskID=taskData.Task.ID,
        Response=f"downloaded to mythic, file id == {results.AgentFileId}".encode("UTF8"),
    ))
