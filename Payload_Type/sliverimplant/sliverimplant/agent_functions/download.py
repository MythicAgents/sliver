from ..SliverRequests import SliverAPI


from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *
from mythic_container.PayloadBuilder import *

class DownloadArguments(TaskArguments):
    def __init__(self, command_line, **kwargs):
        super().__init__(command_line, **kwargs)
        self.args = [
            CommandParameter(
                name="full_path",
                description="path to file",
                type=ParameterType.String
            ),
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
        # Command: download [remote src] <local dst>
        # About: Download a file or directory from the remote system. Directories will be downloaded as a gzipped TAR file.

        # Usage:
        # ======
        #   download [flags] remote-path [local-path]

        # Args:
        # =====
        #   remote-path  string    path to the file or directory to download
        #   local-path   string    local path where the downloaded file will be saved (default: .)

        # Flags:
        # ======
        # TODO:  -F, --file-type string    force a specific file type (binary/text) if looting
        # TODO:  -h, --help                display help
        # TODO:  -X, --loot                save output as loot
        # TODO:  -n, --name      string    name to assign the download if looting
        # TODO:  -r, --recurse             recursively download all files in a directory
        # TODO:  -t, --timeout   int       command timeout in seconds (default: 60)
        # TODO:  -T, --type      string    force a specific loot type (file/cred) if looting

        plaintext = await SliverAPI.download(taskData, taskData.args.get_arg('full_path'))

        # TODO: update the file browser and indicate it was downloaded?
        results = await SendMythicRPCFileCreate(MythicRPCFileCreateMessage(
            TaskID=taskData.Task.ID,
            RemotePathOnTarget=taskData.args.get_arg('full_path'),
            FileContents=plaintext,
            IsScreenshot=False,
            IsDownloadFromAgent=True,
            # Filename=taskData.args.get_arg('full_path').split('/')[-1],
        ))

        await SendMythicRPCResponseCreate(MythicRPCResponseCreateMessage(
            TaskID=taskData.Task.ID,
            Response=f"agent file id == {results.AgentFileId}".encode("UTF8"),
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
