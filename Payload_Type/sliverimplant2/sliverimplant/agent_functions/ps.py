from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *
from mythic_container.PayloadBuilder import *

from sliver import InteractiveBeacon, sliver_pb2
from ..utils.sliver_connect import sliver_implant_clients

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
        await ps(taskData)

        taskResponse = MythicCommandBase.PTTaskCreateTaskingMessageResponse(
            TaskID=taskData.Task.ID,
            Success=True,
            Completed=True,
        )
        return taskResponse

    async def process_response(self, task: PTTaskMessageAllData, response: any) -> PTTaskProcessResponseMessageResponse:
        resp = PTTaskProcessResponseMessageResponse(TaskID=task.Task.ID, Success=True)
        return resp

async def ps(taskData: PTTaskMessageAllData):
    interact = sliver_implant_clients[f"{taskData.Payload.UUID}"]

    if (isinstance(interact, InteractiveBeacon)):
        # TODO: fix this
        await SendMythicRPCResponseCreate(MythicRPCResponseCreateMessage(
            TaskID=taskData.Task.ID,
            Response="bug in sliver-py 1.5.x, not supported for beacons, fixed for sliver 1.6.x\n".encode("UTF8"),
        ))
        return

    ps_results = await interact.ps()

    processes = []
    for individual_ps in ps_results:
        processes.append(
            MythicRPCProcessCreateData(
                Host=taskData.Callback.Host,
                ProcessID=individual_ps.Pid,
                ParentProcessID=individual_ps.Ppid,
                Name=individual_ps.Executable,
                User=individual_ps.Owner,
                Architecture=individual_ps.Architecture,
                CommandLine=" ".join(individual_ps.CmdLine),
            )
        )

    await SendMythicRPCProcessCreate(MythicRPCProcessesCreateMessage(
        TaskID=taskData.Task.ID,
        Processes=processes,
    ))
