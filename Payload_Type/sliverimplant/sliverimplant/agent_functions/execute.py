from ..SliverRequests import SliverAPI


from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *
from mythic_container.PayloadBuilder import *

class ExecuteArguments(TaskArguments):
    def __init__(self, command_line, **kwargs):
        super().__init__(command_line, **kwargs)
        self.args = [
            CommandParameter(
                name="exe",
                description="exe to execute",
                type=ParameterType.String
            ),
            CommandParameter(
                name="args",
                description="args to pass to executable",
                type=ParameterType.Array
            ),
            CommandParameter(
                name="output",
                description="capture output or not",
                type=ParameterType.Boolean
            ),
        ]

    async def parse_arguments(self):
        self.load_args_from_json_string(self.command_line)


class Execute(CommandBase):
    cmd = "execute"
    needs_admin = False
    help_cmd = "execute"
    description = "Execute a program on the remote system"
    version = 1
    author = "Spencer Adolph"
    argument_class = ExecuteArguments
    attackmapping = []

    async def create_go_tasking(self, taskData: MythicCommandBase.PTTaskMessageAllData) -> MythicCommandBase.PTTaskCreateTaskingMessageResponse:
        # Execute a program on the remote system

        # Usage:
        # ======
        #   execute [flags] command [arguments...]

        # Args:
        # =====
        #   command    string         command to execute
        #   arguments  string list    arguments to the command

        # Flags:
        # ======
        #        -h, --help                    display help
        # TODO:  -S, --ignore-stderr           don't print STDERR output
        # TODO:  -X, --loot                    save output as loot
        # TODO:  -n, --name          string    name to assign loot (optional)
        # TODO:  -o, --output                  capture command output
        # TODO:  -P, --ppid          uint      parent process id (optional, Windows only) (default: 0)
        # TODO:  -s, --save                    save output to a file
        # TODO:  -E, --stderr        string    remote path to redirect STDERR to
        # TODO:  -O, --stdout        string    remote path to redirect STDOUT to
        #        -t, --timeout       int       command timeout in seconds (default: 60)
        # TODO:  -T, --token                   execute command with current token (windows only)

        execute_results = await execute(taskData)

        await SendMythicRPCResponseCreate(MythicRPCResponseCreateMessage(
            TaskID=taskData.Task.ID,
            Response=f"{str(execute_results)}".encode("UTF8"),
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

async def execute(taskData: PTTaskMessageAllData):
    interact, isBeacon = await SliverAPI.create_sliver_interact(taskData)

    # TODO: get these from function parameters and extract in the parent function instead
    exe = taskData.args.get_arg('exe')
    args = taskData.args.get_arg('args')
    output = taskData.args.get_arg('output')

    execute_results = await interact.execute(exe=exe, args=args, output=output)

    if (isBeacon):
        execute_results = await execute_results

    return execute_results
