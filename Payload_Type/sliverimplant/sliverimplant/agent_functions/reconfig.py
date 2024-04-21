from ..SliverRequests import SliverAPI

from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *
from mythic_container.PayloadBuilder import *

from sliver import sliver_pb2

class ReconfigArguments(TaskArguments):
    def __init__(self, command_line, **kwargs):
        super().__init__(command_line, **kwargs)
        self.args = [
            CommandParameter(
                name="beacon_interval",
                description="beacon_interval in seconds",
                type=ParameterType.Number,
            ),
        ]

    async def parse_arguments(self):
        self.load_args_from_json_string(self.command_line)


class Reconfig(CommandBase):
    cmd = "reconfig"
    needs_admin = False
    help_cmd = "reconfig"
    description = "Reconfigure the active beacon/session"
    version = 1
    author = "Spencer Adolph"
    argument_class = ReconfigArguments
    attackmapping = []

    async def create_go_tasking(self, taskData: MythicCommandBase.PTTaskMessageAllData) -> MythicCommandBase.PTTaskCreateTaskingMessageResponse:
        # Reconfigure the active beacon/session

        # Usage:
        # ======
        #   reconfig [flags]

        # Flags:
        # ======
        #        -i, --beacon-interval    string    beacon callback interval
        # TODO:  -j, --beacon-jitter      string    beacon callback jitter (random up to)
        #        -h, --help                         display help
        # TODO:  -r, --reconnect-interval string    reconnect interval for implant
        #        -t, --timeout            int       command timeout in seconds (default: 60)

        beacon_interval = taskData.args.get_arg('beacon_interval')
        response = await reconfig(taskData, beacon_interval)

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

async def reconfig(taskData: PTTaskMessageAllData, beacon_interval_seconds: int):
    interact, isBeacon = await SliverAPI.create_sliver_interact(taskData)

    if (not isBeacon):
        return "Beacon only command!"
    
    beacon_interval = beacon_interval_seconds * 1000000000

    reconfig_results = await interact._stub.Reconfigure(interact._request(sliver_pb2.ReconfigureReq(BeaconInterval=beacon_interval)))

    # if (isBeacon):
    #     ifconfig_results = await ifconfig_results

    return "Tasked Reconfig!"
