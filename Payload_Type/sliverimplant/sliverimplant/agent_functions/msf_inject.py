from ..SliverRequests import SliverAPI

from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *
from mythic_container.PayloadBuilder import *

class MsfInjectArguments(TaskArguments):
    def __init__(self, command_line, **kwargs):
        super().__init__(command_line, **kwargs)
        self.args = []

    async def parse_arguments(self):
        pass


class MsfInject(CommandBase):
    cmd = "msf_inject"
    needs_admin = False
    help_cmd = "msf_inject"
    description = "Execute a metasploit payload in a remote process"
    version = 1
    author = "Spencer Adolph"
    argument_class = MsfInjectArguments
    attackmapping = []

    async def create_go_tasking(self, taskData: MythicCommandBase.PTTaskMessageAllData) -> MythicCommandBase.PTTaskCreateTaskingMessageResponse:
        # Command: inject [--pid] [--lhost] <options>
        # About: Execute a metasploit payload in a remote process.

        # Usage:
        # ======
        #   msf-inject [flags]

        # Flags:
        # ======
        # TODO:  -e, --encoder    string    msf encoder
        # TODO:  -h, --help                 display help
        # TODO:  -i, --iterations int       iterations of the encoder (default: 1)
        # TODO:  -L, --lhost      string    listen host
        # TODO:  -l, --lport      int       listen port (default: 4444)
        # TODO:  -m, --payload    string    msf payload (default: meterpreter_reverse_https)
        # TODO:  -p, --pid        int       pid to inject into (default: -1)
        # TODO:  -t, --timeout    int       command timeout in seconds (default: 60)

        response = await msf_inject(taskData)

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

async def msf_inject(taskData: PTTaskMessageAllData):
    # interact, isBeacon = await SliverAPI.create_sliver_interact(taskData)

    # ifconfig_results = await interact._stub()

    # if (isBeacon):
    #     ifconfig_results = await ifconfig_results

    return "This command not yet implemented..."
