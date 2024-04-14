from ..SliverRequests import SliverAPI

from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *
from mythic_container.PayloadBuilder import *

class RmArguments(TaskArguments):
    def __init__(self, command_line, **kwargs):
        super().__init__(command_line, **kwargs)
        self.args = [
            CommandParameter(
                name="full_path",
                description="absolute path to the file/folder",
                default_value='.',
                type=ParameterType.String,
                parameter_group_info=[ParameterGroupInfo(
                    required=False
                )]
            ),
        ]

    async def parse_arguments(self):
        self.load_args_from_json_string(self.command_line)


class Rm(CommandBase):
    cmd = "rm"
    needs_admin = False
    help_cmd = "rm"
    description = "List current directory"
    version = 1
    author = "Spencer Adolph"
    argument_class = RmArguments
    attackmapping = []
    supported_ui_features = ["file_browser:remove"]

    async def create_go_tasking(self, taskData: MythicCommandBase.PTTaskMessageAllData) -> MythicCommandBase.PTTaskCreateTaskingMessageResponse:
        # Command: rm [remote path]
        # About: Delete a remote file or directory.

        # Usage:
        # ======
        #   rm [flags] path

        # Args:
        # =====
        #   path  string    path to the file to remove

        # Flags:
        # ======
        # TODO:  -F, --force            ignore safety and forcefully remove files
        # TODO:  -h, --help             display help
        # TODO:  -r, --recursive        recursively remove files
        # TODO:  -t, --timeout   int    command timeout in seconds (default: 60)

        path_to_rm = taskData.args.get_arg('full_path')
        rm_results = await SliverAPI.rm(taskData, path_to_rm)

        # TODO: this should be refactored
        Name = path_to_rm.split('/')[-1]
        Parent = "/".join(path_to_rm.split('/')[:-1])

        await SendMythicRPCFileBrowserCreate(MythicRPCFileBrowserCreateMessage(
            TaskID=taskData.Task.ID,
            FileBrowser=MythicRPCFileBrowserData(
                Name=Name,
                ParentPath=Parent,
                IsFile=True,
                Files=[],
                Success=True,
                UpdateDeleted=True,
            ),
        ))

        await SendMythicRPCResponseCreate(MythicRPCResponseCreateMessage(
            TaskID=taskData.Task.ID,
            Response=f"{str(rm_results)}".encode("UTF8"),
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
