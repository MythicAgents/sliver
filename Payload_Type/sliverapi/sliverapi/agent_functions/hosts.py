from ..SliverRequests import SliverAPI

from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *
from mythic_container.PayloadBuilder import *

from sliver import common_pb2

class HostsArguments(TaskArguments):
    def __init__(self, command_line, **kwargs):
        super().__init__(command_line, **kwargs)
        self.args = []

    async def parse_arguments(self):
        pass


class Hosts(CommandBase):
    cmd = "hosts"
    needs_admin = False
    help_cmd = "hosts"
    description = "Manage the database of hosts"
    version = 1
    author = "Spencer Adolph"
    argument_class = HostsArguments
    attackmapping = []

    async def create_go_tasking(self, taskData: MythicCommandBase.PTTaskMessageAllData) -> MythicCommandBase.PTTaskCreateTaskingMessageResponse:
        # Manage the database of hosts

        # Usage:
        # ======
        #   hosts [flags]

        # Flags:
        # ======
        # TODO:  -h, --help           display help
        # TODO:  -t, --timeout int    command timeout in seconds (default: 60)

        # Sub Commands:
        # =============
        # TODO:  ioc  Manage tracked IOCs on a given host
        # TODO:  rm   Remove a host from the database

        response = await hosts(taskData)

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


async def hosts(taskData: PTTaskMessageAllData):
    client = await SliverAPI.create_sliver_client(taskData)

    hosts_list = await client._stub.Hosts(common_pb2.Empty())

    # TODO: match sliver formatting

    return f"{hosts_list}"
