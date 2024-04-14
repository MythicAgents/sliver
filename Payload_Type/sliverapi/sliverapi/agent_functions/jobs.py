from ..SliverRequests import SliverAPI

from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *
from mythic_container.PayloadBuilder import *

class JobsArguments(TaskArguments):
    def __init__(self, command_line, **kwargs):
        super().__init__(command_line, **kwargs)
        self.args = [
            CommandParameter(
                name="k",
                description="kill a background job",
                type=ParameterType.Number,
                default_value=-1,
                parameter_group_info=[ParameterGroupInfo(
                    required=False
                )]
            ),
        ]

    async def parse_arguments(self):
        self.load_args_from_json_string(self.command_line)


class Jobs(CommandBase):
    cmd = "jobs"
    needs_admin = False
    help_cmd = "jobs"
    description = "Get the list of jobs that Sliver is aware of."
    version = 1
    author = "Spencer Adolph"
    argument_class = JobsArguments
    attackmapping = []

    async def create_go_tasking(self, taskData: MythicCommandBase.PTTaskMessageAllData) -> MythicCommandBase.PTTaskCreateTaskingMessageResponse:
        # Command: jobs <options>
        # About: Manage jobs/listeners.

        # Usage:
        # ======
        #   jobs [flags]

        # Flags:
        # ======
        # TODO:  -h, --help            display help
        #        -k, --kill     int    kill a background job (default: -1)
        # TODO:  -K, --kill-all        kill all jobs
        # TODO:  -t, --timeout  int    command timeout in seconds (default: 60)


        if (taskData.args.get_arg('k') != -1):
            job_id = taskData.args.get_arg('k')
            response = await SliverAPI.jobs_kill(taskData, job_id)
        else:
            response = await SliverAPI.jobs_list(taskData)

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
