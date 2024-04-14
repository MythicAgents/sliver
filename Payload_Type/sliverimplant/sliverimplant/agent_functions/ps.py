from ..SliverRequests import SliverAPI

from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *
from mythic_container.PayloadBuilder import *

class PsArguments(TaskArguments):
    def __init__(self, command_line, **kwargs):
        super().__init__(command_line, **kwargs)
        self.args = []

    async def parse_arguments(self):
        pass


class Ps(CommandBase):
    cmd = "ps"
    needs_admin = False
    help_cmd = "ps"
    description = "List processes on remote system."
    version = 1
    author = "Spencer Adolph"
    argument_class = PsArguments
    attackmapping = []
    supported_ui_features = ["process_browser:list"]

    async def create_go_tasking(self, taskData: MythicCommandBase.PTTaskMessageAllData) -> MythicCommandBase.PTTaskCreateTaskingMessageResponse:        
        # Command: ps <options>
        # About: List processes on remote system.

        # Usage:
        # ======
        #   ps [flags]

        # Flags:
        # ======
        # TODO:  -e, --exe           string    filter based on executable name
        # TODO:  -h, --help                    display help
        # TODO:  -O, --overflow                overflow terminal width (display truncated rows)
        # TODO:  -o, --owner         string    filter based on owner
        # TODO:  -p, --pid           int       filter based on pid (default: -1)
        # TODO:  -c, --print-cmdline           print command line arguments
        # TODO:  -S, --skip-pages    int       skip the first n page(s) (default: 0)
        # TODO:  -t, --timeout       int       command timeout in seconds (default: 60)
        # TODO:  -T, --tree                    print process tree

        ps_results = await SliverAPI.ps(taskData)

        processes = []
        for ps in ps_results:
            processes.append(
                MythicRPCProcessCreateData(
                    Host=taskData.Callback.Host,
                    ProcessID=ps.Pid,
                    ParentProcessID=ps.Ppid,
                    Name=ps.Executable,
                    User=ps.Owner,
                    Architecture=ps.Architecture,
                    CommandLine=" ".join(ps.CmdLine),
                )
            )

        await SendMythicRPCProcessCreate(MythicRPCProcessesCreateMessage(
            TaskID=taskData.Task.ID,
            Processes=processes,
        ))

        taskResponse = MythicCommandBase.PTTaskCreateTaskingMessageResponse(
            TaskID=taskData.Task.ID,
            Success=True,
            Completed=True,
        )
        return taskResponse

    async def process_response(self, task: PTTaskMessageAllData, response: any) -> PTTaskProcessResponseMessageResponse:
        resp = PTTaskProcessResponseMessageResponse(TaskID=task.Task.ID, Success=True)
        return resp
