from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *
from mythic_container.PayloadBuilder import *

from tabulate import tabulate

from sliver import InteractiveBeacon
from ..utils.sliver_connect import sliver_implant_clients

class NetstatArguments(TaskArguments):
    def __init__(self, command_line, **kwargs):
        super().__init__(command_line, **kwargs)
        self.args = [
            CommandParameter(
                name="ipv4",
                cli_name="ipv4",
                display_name="ipv4",
                type=ParameterType.Boolean,
                default_value=True,
                description="display information about IPv4 sockets",
                parameter_group_info=[
                    ParameterGroupInfo(
                        required=False,
                        group_name="Default",
                        ui_position=1
                    ),
            ]),
            CommandParameter(
                name="ipv6",
                cli_name="ipv6",
                display_name="ipv6",
                type=ParameterType.Boolean,
                default_value=False,
                description="display information about IPv6 sockets",
                parameter_group_info=[
                    ParameterGroupInfo(
                        required=False,
                        group_name="Default",
                        ui_position=2
                    ),
            ]),
            CommandParameter(
                name="listen",
                cli_name="listen",
                display_name="listen",
                type=ParameterType.Boolean,
                default_value=False,
                description="display information about listening sockets",
                parameter_group_info=[
                    ParameterGroupInfo(
                        required=False,
                        group_name="Default",
                        ui_position=3
                    ),
            ]),
            CommandParameter(
                name="tcp",
                cli_name="tcp",
                display_name="tcp",
                type=ParameterType.Boolean,
                default_value=True,
                description="display information about TCP sockets",
                parameter_group_info=[
                    ParameterGroupInfo(
                        required=False,
                        group_name="Default",
                        ui_position=4
                    ),
            ]),
            CommandParameter(
                name="udp",
                cli_name="udp",
                display_name="udp",
                type=ParameterType.Boolean,
                default_value=False,
                description="display information about UDP sockets",
                parameter_group_info=[
                    ParameterGroupInfo(
                        required=False,
                        group_name="Default",
                        ui_position=5
                    ),
            ]),
        ]

    async def parse_arguments(self):
        self.load_args_from_json_string(self.command_line)

class Netstat(CommandBase):
    cmd = "netstat"
    needs_admin = False
    help_cmd = "netstat"
    description = "Print network connection information"
    version = 1
    author = "Spencer Adolph"
    argument_class = NetstatArguments
    attackmapping = []

    async def create_go_tasking(self, taskData: MythicCommandBase.PTTaskMessageAllData) -> MythicCommandBase.PTTaskCreateTaskingMessageResponse:
        await netstat(taskData)

        taskResponse = MythicCommandBase.PTTaskCreateTaskingMessageResponse(
            TaskID=taskData.Task.ID,
            Success=True,
            Completed=True
        )
        return taskResponse

    async def process_response(self, task: PTTaskMessageAllData, response: any) -> PTTaskProcessResponseMessageResponse:
        resp = PTTaskProcessResponseMessageResponse(TaskID=task.Task.ID, Success=True)
        return resp

async def netstat(taskData: PTTaskMessageAllData):
    interact = sliver_implant_clients[f"{taskData.Payload.UUID}"]

    ipv4 = taskData.args.get_arg('ipv4')
    ipv6 = taskData.args.get_arg('ipv6')
    listen = taskData.args.get_arg('listen')
    tcp = taskData.args.get_arg('tcp')
    udp = taskData.args.get_arg('udp')

    netstat_results = await interact.netstat(tcp=tcp, udp=udp, ipv4=ipv4, ipv6=ipv6, listening=listen)

    if (isinstance(interact, InteractiveBeacon)):
        await SendMythicRPCResponseCreate(MythicRPCResponseCreateMessage(
            TaskID=taskData.Task.ID,
            Response="issued task, awaiting results\n".encode("UTF8"),
        ))
        netstat_results = await netstat_results

    # Formatting
    headers = ["Protocol", "Local Address", "Foreign Address", "State", "PID/Program Name"]
    data = [(entry.Protocol, f"{entry.LocalAddr.Ip}:{entry.LocalAddr.Port}", f"{entry.RemoteAddr.Ip}:{entry.RemoteAddr.Port}", entry.SkState, f"{entry.Process.Pid}/{entry.Process.Executable}") for entry in netstat_results.Entries]
    table = tabulate(data, headers=headers)

    await SendMythicRPCResponseCreate(MythicRPCResponseCreateMessage(
        TaskID=taskData.Task.ID,
        Response=table.encode("UTF8"),
    ))
