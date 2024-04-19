from ..SliverRequests import SliverAPI

from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *
from mythic_container.PayloadBuilder import *

class MsfArguments(TaskArguments):
    def __init__(self, command_line, **kwargs):
        super().__init__(command_line, **kwargs)
        self.args = []

    async def parse_arguments(self):
        pass


class Msf(CommandBase):
    cmd = "msf"
    needs_admin = False
    help_cmd = "msf"
    description = "Execute a metasploit payload in the current process"
    version = 1
    author = "Spencer Adolph"
    argument_class = MsfArguments
    attackmapping = []

    async def create_go_tasking(self, taskData: MythicCommandBase.PTTaskMessageAllData) -> MythicCommandBase.PTTaskCreateTaskingMessageResponse:
        # Command: msf [--lhost] <options>
        # About: Execute a metasploit payload in the current process.

        # Usage:
        # ======
        #   msf [flags]

        # Flags:
        # ======
        # TODO:  -e, --encoder    string    msf encoder
        # TODO:  -h, --help                 display help
        # TODO:  -i, --iterations int       iterations of the encoder (default: 1)
        # TODO:  -L, --lhost      string    listen host
        # TODO:  -l, --lport      int       listen port (default: 4444)
        # TODO:  -m, --payload    string    msf payload (default: meterpreter_reverse_https)
        # TODO:  -t, --timeout    int       command timeout in seconds (default: 60)

        response = await msf(taskData)

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

async def msf(taskData: PTTaskMessageAllData):
    # interact, isBeacon = await SliverAPI.create_sliver_interact(taskData)

    # ifconfig_results = await interact._stub()

    # if (isBeacon):
    #     ifconfig_results = await ifconfig_results

    return "This command not yet implemented..."
