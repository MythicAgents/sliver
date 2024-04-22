from ..SliverRequests import SliverAPI

from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *
from mythic_container.PayloadBuilder import *

class ProcdumpArguments(TaskArguments):
    def __init__(self, command_line, **kwargs):
        super().__init__(command_line, **kwargs)
        self.args = []

    async def parse_arguments(self):
        pass


class Procdump(CommandBase):
    cmd = "procdump"
    needs_admin = False
    help_cmd = "procdump"
    description = "Dumps the process memory given a process identifier"
    version = 1
    author = "Spencer Adolph"
    argument_class = ProcdumpArguments
    attackmapping = []

    async def create_go_tasking(self, taskData: MythicCommandBase.PTTaskMessageAllData) -> MythicCommandBase.PTTaskCreateTaskingMessageResponse:
        # Command: procdump [pid]
        # About: Dumps the process memory given a process identifier (pid)

        # Usage:
        # ======
        #   procdump [flags]

        # Flags:
        # ======
        #        -h, --help                display help
        # TODO:  -X, --loot                save output as loot
        # TODO:  -N, --loot-name string    name to assign when adding the memory dump to the loot store (optional)
        # TODO:  -n, --name      string    target process name
        # TODO:  -p, --pid       int       target pid (default: -1)
        # TODO:  -s, --save      string    save to file (will overwrite if exists)
        #        -t, --timeout   int       command timeout in seconds (default: 60)

        response = await procdump(taskData)

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

async def procdump(taskData: PTTaskMessageAllData):
    # interact, isBeacon = await SliverAPI.create_sliver_interact(taskData)

    # ifconfig_results = await interact._stub()

    # if (isBeacon):
    #     ifconfig_results = await ifconfig_results

    return "This command not yet implemented..."
