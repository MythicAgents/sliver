from ..SliverRequests import SliverAPI


from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *
from mythic_container.PayloadBuilder import *
import gzip

class CatArguments(TaskArguments):
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


class Cat(CommandBase):
    cmd = "cat"
    needs_admin = False
    help_cmd = "cat"
    description = "cat a file"
    version = 1
    author = "Spencer Adolph"
    argument_class = CatArguments
    attackmapping = []

    async def create_go_tasking(self, taskData: MythicCommandBase.PTTaskMessageAllData) -> MythicCommandBase.PTTaskCreateTaskingMessageResponse:
        # Command: cat <remote path> 
        # About: Cat a remote file to stdout.

        # Usage:
        # ======
        #   cat [flags] path

        # Args:
        # =====
        #   path  string    path to the file to print

        # Flags:
        # ======
        # TODO:  -c, --colorize-output           colorize output
        # TODO:  -F, --file-type       string    force a specific file type (binary/text) if looting (optional)
        # TODO:  -h, --help                      display help
        # TODO:  -x, --hex                       display as a hex dump
        # TODO:  -X, --loot                      save output as loot
        # TODO:  -n, --name            string    name to assign loot (optional)
        # TODO:  -t, --timeout         int       command timeout in seconds (default: 60)
        # TODO:  -T, --type            string    force a specific loot type (file/cred) if looting (optional)

        # just download and don't create a file, show the output to user
        # sliver py doesn't have a direct 'cat' method to use
        plaintext = await download(taskData, taskData.args.get_arg('full_path'))

        await SendMythicRPCResponseCreate(MythicRPCResponseCreateMessage(
            TaskID=taskData.Task.ID,
            Response=f"{plaintext.decode('utf-8')}".encode("UTF8"),
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

async def download(taskData: PTTaskMessageAllData, full_path: str):
    # TODO: this is duplicated in the download.py command, consider refactoring
    interact, isBeacon = await SliverAPI.create_sliver_interact(taskData)

    download_results = await interact.download(remote_path=full_path)

    if (isBeacon):
        download_results = await download_results

    plaintext = gzip.decompress(download_results.Data)

    return plaintext


