from ..SliverRequests import SliverAPI

from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *
from mythic_container.PayloadBuilder import *

class ExecuteShellcodeArguments(TaskArguments):
    def __init__(self, command_line, **kwargs):
        super().__init__(command_line, **kwargs)
        self.args = []

    async def parse_arguments(self):
        pass


class ExecuteShellcode(CommandBase):
    cmd = "execute_shellcode"
    needs_admin = False
    help_cmd = "execute_shellcode"
    description = "Executes the given shellcode in the implant's process"
    version = 1
    author = "Spencer Adolph"
    argument_class = ExecuteShellcodeArguments
    attackmapping = []

    async def create_go_tasking(self, taskData: MythicCommandBase.PTTaskMessageAllData) -> MythicCommandBase.PTTaskCreateTaskingMessageResponse:
        # Command: execute-shellcode [local path to raw shellcode]
        # About: Executes the given shellcode in the implant's process.

        # ++ Shellcode ++
        # Shellcode files should be binary encoded, you can generate Sliver shellcode files with the generate command:
        # 	generate --format shellcode

        # Usage:
        # ======
        #   execute-shellcode [flags] filepath

        # Args:
        # =====
        #   filepath  string    path the shellcode file

        # Flags:
        # ======
        # TODO:  -A, --architecture   string    architecture of the shellcode: 386, amd64 (used with --shikata-ga-nai flag) (default: amd64)
        # TODO:  -h, --help                     display help
        # TODO:  -i, --interactive              Inject into a new process and interact with it
        # TODO:  -I, --iterations     int       number of encoding iterations (used with --shikata-ga-nai flag) (default: 1)
        # TODO:  -p, --pid            uint      Pid of process to inject into (0 means injection into ourselves) (default: 0)
        # TODO:  -n, --process        string    Process to inject into when running in interactive mode (default: c:\windows\system32\notepad.exe)
        # TODO:  -r, --rwx-pages                Use RWX permissions for memory pages
        # TODO:  -S, --shikata-ga-nai           encode shellcode using shikata ga nai prior to execution
        # TODO:  -t, --timeout        int       command timeout in seconds (default: 60)

        response = await execute_shellcode(taskData)

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

async def execute_shellcode(taskData: PTTaskMessageAllData):
    # interact, isBeacon = await SliverAPI.create_sliver_interact(taskData)

    # ifconfig_results = await interact._stub()

    # if (isBeacon):
    #     ifconfig_results = await ifconfig_results

    return "This command not yet implemented..."
