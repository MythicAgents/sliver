from ..SliverRequests import SliverAPI

from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *
from mythic_container.PayloadBuilder import *

class ExecuteAssemblyArguments(TaskArguments):
    def __init__(self, command_line, **kwargs):
        super().__init__(command_line, **kwargs)
        self.args = []

    async def parse_arguments(self):
        pass


class ExecuteAssembly(CommandBase):
    cmd = "execute_assembly"
    needs_admin = False
    help_cmd = "execute_assembly"
    description = "(Windows Only) Executes the .NET assembly in a child process"
    version = 1
    author = "Spencer Adolph"
    argument_class = ExecuteAssemblyArguments
    attackmapping = []

    async def create_go_tasking(self, taskData: MythicCommandBase.PTTaskMessageAllData) -> MythicCommandBase.PTTaskCreateTaskingMessageResponse:
        # TODO: ensure this command is only loaded into windows implants...

        # Command: execute-assembly [local path to assembly] [arguments]
        # About: (Windows Only) Executes the .NET assembly in a child process.

        # Usage:
        # ======
        #   execute-assembly [flags] filepath [arguments...]

        # Args:
        # =====
        #   filepath   string         path the assembly file
        #   arguments  string list    arguments to pass to the assembly entrypoint (default: [])

        # Flags:
        # ======
        # TODO:  -M, --amsi-bypass                 Bypass AMSI on Windows (only supported when used with --in-process)
        # TODO:  -d, --app-domain        string    AppDomain name to create for .NET assembly. Generated randomly if not set.
        # TODO:  -a, --arch              string    Assembly target architecture: x86, x64, x84 (x86+x64) (default: x84)
        # TODO:  -c, --class             string    Optional class name (required for .NET DLL)
        # TODO:  -E, --etw-bypass                  Bypass ETW on Windows (only supported when used with --in-process)
        #        -h, --help                        display help
        # TODO:  -i, --in-process                  Run in the current sliver process
        # TODO:  -X, --loot                        save output as loot
        # TODO:  -m, --method            string    Optional method (a method is required for a .NET DLL)
        # TODO:  -n, --name              string    name to assign loot (optional)
        # TODO:  -P, --ppid              uint      parent process id (optional) (default: 0)
        # TODO:  -p, --process           string    hosting process to inject into (default: notepad.exe)
        # TODO:  -A, --process-arguments string    arguments to pass to the hosting process
        # TODO:  -r, --runtime           string    Runtime to use for running the assembly (only supported when used with --in-process)
        # TODO:  -s, --save                        save output to file
        #        -t, --timeout           int       command timeout in seconds (default: 60)

        response = await execute_assembly(taskData)

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

async def execute_assembly(taskData: PTTaskMessageAllData):
    # interact, isBeacon = await SliverAPI.create_sliver_interact(taskData)

    # ifconfig_results = await interact._stub()

    # if (isBeacon):
    #     ifconfig_results = await ifconfig_results

    return "This command not yet implemented..."
