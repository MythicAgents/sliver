from ..SliverRequests import SliverAPI

from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *
from mythic_container.PayloadBuilder import *

class BeaconsArguments(TaskArguments):
    def __init__(self, command_line, **kwargs):
        super().__init__(command_line, **kwargs)
        self.args = []

    async def parse_arguments(self):
        pass


class Beacons(CommandBase):
    cmd = "beacons"
    needs_admin = False
    help_cmd = "beacons"
    description = "Get the list of beacons that Sliver is aware of."
    version = 1
    author = "Spencer Adolph"
    argument_class = BeaconsArguments
    attackmapping = []

    async def create_go_tasking(self, taskData: MythicCommandBase.PTTaskMessageAllData) -> MythicCommandBase.PTTaskCreateTaskingMessageResponse:
        # Manage beacons

        # Usage:
        # ======
        #   beacons [flags]

        # Flags:
        # ======
        # TODO:  -f, --filter    string    filter beacons by substring
        # TODO:  -e, --filter-re string    filter beacons by regular expression
        # TODO:  -F, --force               force killing of the beacon
        # TODO:  -k, --kill      string    kill a beacon
        # TODO:  -K, --kill-all            kill all beacons

        # Sub Commands:
        # =============
        # TODO:  prune  Prune stale beacons automatically
        # TODO:  rm     Remove a beacon
        # TODO:  watch  Watch your beacons

        
        # 'beacons' with no options
        response = await beacons_list(taskData)

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

async def beacons_list(taskData: PTTaskMessageAllData):
    client = await SliverAPI.create_sliver_client(taskData)
    beacons = await client.beacons()

    # TODO: match sliver formatting

    #  ID         Name          Transport   Hostname   Username   Operating System   Last Check-In   Next Check-In 
    # ========== ============= =========== ========== ========== ================== =============== ===============
    #  d90a2ec6   DARK_MITTEN   mtls        ubuntu     ubuntu     linux/amd64        2s              1m4s          

    # What to show if no beacons?

    return f"{beacons}"

