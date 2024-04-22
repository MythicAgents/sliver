from ..SliverRequests import SliverAPI

from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *
from mythic_container.PayloadBuilder import *

from sliver import sliver_pb2, client_pb2

class MvArguments(TaskArguments):
    def __init__(self, command_line, **kwargs):
        super().__init__(command_line, **kwargs)
        self.args = [
            CommandParameter(
                name="src",
                cli_name="src",
                display_name="src",
                description="source file",
                type=ParameterType.String,
            ),
            CommandParameter(
                name="dst",
                cli_name="dst",
                display_name="dst",
                description="destination file",
                type=ParameterType.String,
            ),
        ]

    async def parse_arguments(self):
        self.load_args_from_json_string(self.command_line)


class Mv(CommandBase):
    cmd = "mv"
    needs_admin = False
    help_cmd = "mv"
    description = "Move or rename a file"
    version = 1
    author = "Spencer Adolph"
    argument_class = MvArguments
    attackmapping = []

    async def create_go_tasking(self, taskData: MythicCommandBase.PTTaskMessageAllData) -> MythicCommandBase.PTTaskCreateTaskingMessageResponse:
        # Move or rename a file

        # Usage:
        # ======
        #   mv [flags] src dst

        # Args:
        # =====
        #   src  string    path to source file
        #   dst  string    path to dest file

        # Flags:
        # ======
        #        -h, --help           display help
        #        -t, --timeout int    command timeout in seconds (default: 60)

        src = taskData.args.get_arg('src')
        dst = taskData.args.get_arg('dst')
        response = await mv(taskData, src, dst)

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

async def mv(taskData: PTTaskMessageAllData, src: str, dst: str):
    interact, isBeacon = await SliverAPI.create_sliver_interact(taskData)

    # TODO: figure out how to await the task completing
    mv_results = await interact._stub.Mv(interact._request(sliver_pb2.MvReq(Src=src, Dst=dst)))

    # if (isBeacon):
    #     mv_results = await mv_results

    return f"Tasked [*] {src} > {dst}"
