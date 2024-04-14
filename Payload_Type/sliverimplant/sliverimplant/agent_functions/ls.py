from ..SliverRequests import SliverAPI

from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *
from mythic_container.PayloadBuilder import *

class LsArguments(TaskArguments):
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


class Ls(CommandBase):
    cmd = "ls"
    needs_admin = False
    help_cmd = "ls"
    description = "List current directory"
    version = 1
    author = "Spencer Adolph"
    argument_class = LsArguments
    attackmapping = []
    supported_ui_features = ["file_browser:list"]

    async def create_go_tasking(self, taskData: MythicCommandBase.PTTaskMessageAllData) -> MythicCommandBase.PTTaskCreateTaskingMessageResponse:
        # Command: ls <remote path>
        # About: List remote files in current directory, or path if provided.

        # Usage:
        # ======
        #   ls [flags] [path]

        # Args:
        # =====
        #   path  string    path to enumerate (default: .)

        # Flags:
        # ======
        # TODO:  -h, --help            display help
        # TODO:  -m, --modified        sort by modified time
        # TODO:  -r, --reverse         reverse sort order
        # TODO:  -s, --size            sort by size
        # TODO:  -t, --timeout  int    command timeout in seconds (default: 60)

        path_to_ls = taskData.args.get_arg('full_path')
        ls_results = await SliverAPI.ls(taskData, path_to_ls)

        # PATH will always be the 'directory' that is queried
        # Files will always be files/directories inside the path

        # This is the shape of data that sliver offers

        # Path: "/home"
        # Exists: true
        # Files {
        #   Name: "ubuntu"
        #   IsDir: true
        #   Size: 4096
        #   ModTime: 1712706688
        #   Mode: "drwxr-x---"
        # }
        # timezone: "CDT"
        # timezoneOffset: -18000

        files = []
        if ls_results.Files != []:
            for file in ls_results.Files:
                files.append(MythicRPCFileBrowserDataChildren(
                        Name=file.Name,
                        IsFile=not file.IsDir,
                        Permissions={"perms": file.Mode},
                        ModifyTime=file.ModTime,
                        Size=file.Size
                    )
                )

        Name = ls_results.Path.split('/')[-1]
        Parent = "/".join(ls_results.Path.split('/')[:-1])

        # # edge case (probably check length of parent path list instead)
        if Parent == '':
            Parent = '/'

        # # TODO: refactor all of this for edge cases
        if path_to_ls == '/':
            Name = '/'
            Parent = ''

        # TODO: currently unable to directly list a file, only directories

        await SendMythicRPCFileBrowserCreate(MythicRPCFileBrowserCreateMessage(
            TaskID=taskData.Task.ID,
            FileBrowser=MythicRPCFileBrowserData(
                Name=Name,
                ParentPath=Parent,
                IsFile=False,
                Files=files,
                # Success=True
            ),
        ))

        await SendMythicRPCResponseCreate(MythicRPCResponseCreateMessage(
            TaskID=taskData.Task.ID,
            Response=f"{str(ls_results)}".encode("UTF8"),
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
