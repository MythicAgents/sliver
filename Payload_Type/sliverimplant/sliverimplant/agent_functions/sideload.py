from ..SliverRequests import SliverAPI

from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *
from mythic_container.PayloadBuilder import *

class SideloadArguments(TaskArguments):
    def __init__(self, command_line, **kwargs):
        super().__init__(command_line, **kwargs)
        self.args = []

    async def parse_arguments(self):
        pass


class Sideload(CommandBase):
    cmd = "sideload"
    needs_admin = False
    help_cmd = "sideload"
    description = "Load and execute a shared library in memory in a remote process"
    version = 1
    author = "Spencer Adolph"
    argument_class = SideloadArguments
    attackmapping = []

    async def create_go_tasking(self, taskData: MythicCommandBase.PTTaskMessageAllData) -> MythicCommandBase.PTTaskCreateTaskingMessageResponse:
        # Command: sideload <options> <filepath to DLL>
        # About: Load and execute a shared library in memory in a remote process.

        # Usage:
        # ======
        #   sideload [flags] filepath [args...]

        # Args:
        # =====
        #   filepath  string         path the shared library file
        #   args      string list    arguments for the binary (default: [])

        # Flags:
        # ======
        # TODO:  -e, --entry-point       string    Entrypoint for the DLL (Windows only)
        #        -h, --help                        display help
        # TODO:  -k, --keep-alive                  don't terminate host process once the execution completes
        # TODO:  -X, --loot                        save output as loot
        # TODO:  -n, --name              string    name to assign loot (optional)
        # TODO:  -P, --ppid              uint      parent process id (optional) (default: 0)
        # TODO:  -p, --process           string    Path to process to host the shellcode (default: c:\windows\system32\notepad.exe)
        # TODO:  -A, --process-arguments string    arguments to pass to the hosting process
        # TODO:  -s, --save                        save output to file
        #        -t, --timeout           int       command timeout in seconds (default: 60)
        # TODO:  -w, --unicode                     Command line is passed to unmanaged DLL function in UNICODE format. (default is ANSI)

        response = await sideload(taskData)

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

async def sideload(taskData: PTTaskMessageAllData):
    # interact, isBeacon = await SliverAPI.create_sliver_interact(taskData)

    # ifconfig_results = await interact._stub()

    # if (isBeacon):
    #     ifconfig_results = await ifconfig_results

    return "This command not yet implemented..."
