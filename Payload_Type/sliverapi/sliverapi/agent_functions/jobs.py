from ..SliverRequests import SliverAPI

from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *
from mythic_container.PayloadBuilder import *

from sliver import SliverClientConfig, SliverClient, client_pb2
from tabulate import tabulate

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
                # type=ParameterType.Number,
                type=ParameterType.ChooseOne,
                dynamic_query_function=self.get_jobs,
                # default_value=-1,
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
        list_of_jobs = await client.jobs()
        for job_item in list_of_jobs:
            job_ids.append(f"{job_item.ID}")

        return PTRPCDynamicQueryFunctionMessageResponse(Success=True, Choices=job_ids)

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
        #        -h, --help            display help
        #        -k, --kill     int    kill a background job (default: -1)
        # TODO:  -K, --kill-all        kill all jobs
        #        -t, --timeout  int    command timeout in seconds (default: 60)

        if (taskData.parameter_group_name == 'Default'):
            response = await jobs_list(taskData)

        if (taskData.parameter_group_name == 'kill'):
            job_id = int(taskData.args.get_arg('kill'))
            response = await jobs_kill(taskData, job_id)
        
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


async def jobs_list(taskData: PTTaskMessageAllData):
    client = await SliverAPI.create_sliver_client(taskData)
    jobs = await client.jobs()

    if (len(jobs) == 0):
        return "[*] No active jobs"

    # TODO: match sliver formatting

    headers = ["ID", "Name", "Protocol", "Port"]
    data = [(job.ID, job.Name, job.Protocol, job.Port) for job in jobs]
    table = tabulate(data, headers=headers)

    return table


async def jobs_kill(taskData: PTTaskMessageAllData, job_id: int):
    client = await SliverAPI.create_sliver_client(taskData)
    kill_response = await client.kill_job(job_id=job_id)
    return f"[*] Successfully killed job #{kill_response.ID}"
