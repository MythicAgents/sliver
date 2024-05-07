from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *
from mythic_container.PayloadBuilder import *

from tabulate import tabulate

from sliver import InteractiveBeacon
from ..utils.sliver_connect import sliver_implant_clients

class IfconfigArguments(TaskArguments):
    def __init__(self, command_line, **kwargs):
        super().__init__(command_line, **kwargs)
        self.args = []

    async def parse_arguments(self):
        pass

class Ifconfig(CommandBase):
    cmd = "ifconfig"
    needs_admin = False
    help_cmd = "ifconfig"
    description = "View network interface configurations"
    version = 1
    author = "Spencer Adolph"
    argument_class = IfconfigArguments
    attackmapping = []

    async def create_go_tasking(self, taskData: MythicCommandBase.PTTaskMessageAllData) -> MythicCommandBase.PTTaskCreateTaskingMessageResponse:
        await ifconfig(taskData)

        taskResponse = MythicCommandBase.PTTaskCreateTaskingMessageResponse(
            TaskID=taskData.Task.ID,
            Success=True,
            Completed=True
        )
        return taskResponse

    async def process_response(self, task: PTTaskMessageAllData, response: any) -> PTTaskProcessResponseMessageResponse:
        resp = PTTaskProcessResponseMessageResponse(TaskID=task.Task.ID, Success=True)
        return resp

async def ifconfig(taskData: PTTaskMessageAllData):
    interact = sliver_implant_clients[f"{taskData.Payload.UUID}"]

    ifconfig_results = await interact.ifconfig()

    if (isinstance(interact, InteractiveBeacon)):
        await SendMythicRPCResponseCreate(MythicRPCResponseCreateMessage(
            TaskID=taskData.Task.ID,
            Response="issued task, awaiting results\n".encode("UTF8"),
        ))
        ifconfig_results = await ifconfig_results

    headers = ["Interface", "Ip Address(s)", "MAC Address"]
    data = [(interface.Name, interface.IPAddresses, interface.MAC) for interface in ifconfig_results.NetInterfaces]
    table = tabulate(data, headers=headers)

    await SendMythicRPCResponseCreate(MythicRPCResponseCreateMessage(
        TaskID=taskData.Task.ID,
        Response=table.encode("UTF8"),
    ))
