from ..SliverRequests import SliverAPI

from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *
from mythic_container.PayloadBuilder import *

from sliver import sliver_pb2, client_pb2

class TasksArguments(TaskArguments):
    def __init__(self, command_line, **kwargs):
        super().__init__(command_line, **kwargs)
        self.args = []

    async def parse_arguments(self):
        pass


class Tasks(CommandBase):
    cmd = "tasks"
    needs_admin = False
    help_cmd = "tasks"
    description = "Beacon task management"
    version = 1
    author = "Spencer Adolph"
    argument_class = TasksArguments
    attackmapping = []

    async def create_go_tasking(self, taskData: MythicCommandBase.PTTaskMessageAllData) -> MythicCommandBase.PTTaskCreateTaskingMessageResponse:
        # Beacon task management

        # Usage:
        # ======
        #   tasks [flags]

        # Flags:
        # ======
        # TODO:  -f, --filter     string    filter based on task type (case-insensitive prefix matching)
        #        -h, --help                 display help
        # TODO:  -O, --overflow             overflow terminal width (display truncated rows)
        # TODO:  -S, --skip-pages int       skip the first n page(s) (default: 0)
        #        -t, --timeout    int       command timeout in seconds (default: 60)

        # Sub Commands:
        # =============
        # TODO:  cancel  Cancel a pending beacon task
        # TODO:  fetch   Fetch the details of a beacon task

        response = await tasks(taskData)

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

async def tasks(taskData: PTTaskMessageAllData):
    interact, isBeacon = await SliverAPI.create_sliver_interact(taskData)

    if (not isBeacon):
        return "Beacon only command!"

    task_results = await interact._stub.GetBeaconTasks(client_pb2.Beacon(ID=interact.beacon_id))

    # if (isBeacon):
    #     ifconfig_results = await ifconfig_results

    return f"{task_results}"
