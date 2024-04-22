from ..SliverRequests import SliverAPI

from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *
from mythic_container.PayloadBuilder import *

from sliver import SliverClientConfig, SliverClient, client_pb2
from tabulate import tabulate

class RegenerateArguments(TaskArguments):
    def __init__(self, command_line, **kwargs):
        super().__init__(command_line, **kwargs)
        self.args = [
            CommandParameter(
                name="implant-name",
                cli_name="implant-name",
                display_name="implant-name",
                description="implant-name",
                # type=ParameterType.Number,
                type=ParameterType.ChooseOne,
                dynamic_query_function=self.get_implants,
                # default_value=-1,
                parameter_group_info=[
                    ParameterGroupInfo(
                        required=True,
                        group_name="Default",
                        ui_position=1
                    ),
                ]
            ),
        ]

    async def get_implants(self, inputMsg: PTRPCDynamicQueryFunctionMessage) -> PTRPCDynamicQueryFunctionMessageResponse:
        implant_names = []

        # TODO: this is quick and dirty, could refactor this (and put into SliverAPI file)
        this_payload = await SendMythicRPCPayloadSearch(MythicRPCPayloadSearchMessage(
            CallbackID=inputMsg.Callback,
            PayloadUUID=inputMsg.PayloadUUID
        ))

        filecontent = await SendMythicRPCFileGetContent(MythicRPCFileGetContentMessage(
            AgentFileId=this_payload.Payloads[0].BuildParameters[0].Value
        ))

        config = SliverClientConfig.parse_config(filecontent.Content)
        client = SliverClient(config)
        await client.connect()
        list_of_implants = await client.implant_builds()
        for key, value in list_of_implants.items():
            implant_names.append(key)

        return PTRPCDynamicQueryFunctionMessageResponse(Success=True, Choices=implant_names)



    async def parse_arguments(self):
        self.load_args_from_json_string(self.command_line)


class Regenerate(CommandBase):
    cmd = "regenerate"
    needs_admin = False
    help_cmd = "regenerate"
    description = "Regenerate an implant"
    version = 1
    author = "Spencer Adolph"
    argument_class = RegenerateArguments
    attackmapping = []

    async def create_go_tasking(self, taskData: MythicCommandBase.PTTaskMessageAllData) -> MythicCommandBase.PTTaskCreateTaskingMessageResponse:
        # Regenerate an implant

        # Usage:
        # ======
        #   regenerate [flags] implant-name

        # Args:
        # =====
        #   implant-name  string    name of the implant

        # Flags:
        # ======
        #        -h, --help              display help
        #        -s, --save    string    directory/file to the binary to
        #        -t, --timeout int       command timeout in seconds (default: 60)

        response = await regenerate(taskData)

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


async def regenerate(taskData: PTTaskMessageAllData):
    client = await SliverAPI.create_sliver_client(taskData)
    implant_name = taskData.args.get_arg('implant-name')
    regenerate_result = await client.regenerate_implant(implant_name=implant_name)
    implant_bytes = regenerate_result.File.Data

    # TODO: match sliver formatting

    return f"generated {regenerate_result.File.Name}"
