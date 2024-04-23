from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *
from mythic_container.PayloadBuilder import *

class JobsArguments(TaskArguments):
    def __init__(self, command_line, **kwargs):
        super().__init__(command_line, **kwargs)
        self.args = [
            CommandParameter(
                name="list",
                cli_name="list",
                display_name="jobs",
                type=ParameterType.Boolean,
                default_value=True,
                description="jobs",
                parameter_group_info=[
                    ParameterGroupInfo(
                        required=False,
                        group_name="Default",
                        ui_position=1
                    ),
            ]),
            CommandParameter(
                name="kill",
                cli_name="kill",
                display_name="job id to kill",
                description="job id to kill",
                type=ParameterType.ChooseOne,
                dynamic_query_function=self.get_jobs,
                parameter_group_info=[
                    ParameterGroupInfo(
                        required=True,
                        group_name="kill",
                        ui_position=1
                    ),
                ]
            ),
        ]

    async def get_jobs(self, inputMsg: PTRPCDynamicQueryFunctionMessage) -> PTRPCDynamicQueryFunctionMessageResponse:
        job_ids = []

        # TODO: query some backend async to get these
        job_ids.append('one')
        job_ids.append('two')
        job_ids.append('three')

        return PTRPCDynamicQueryFunctionMessageResponse(Success=True, Choices=job_ids)

    async def parse_arguments(self):
        self.load_args_from_json_string(self.command_line)


class Jobs(CommandBase):
    cmd = "jobs"
    needs_admin = False
    help_cmd = "jobs"
    description = "Get the list of jobs"
    version = 1
    author = "Spencer Adolph"
    argument_class = JobsArguments
    attackmapping = []

    async def create_go_tasking(self, taskData: MythicCommandBase.PTTaskMessageAllData) -> MythicCommandBase.PTTaskCreateTaskingMessageResponse:

        # TODO: hypothetically deal with either listing jobs or killing the selected job

        await SendMythicRPCResponseCreate(MythicRPCResponseCreateMessage(
            TaskID=taskData.Task.ID,
            Response='success'.encode("UTF8"),
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
