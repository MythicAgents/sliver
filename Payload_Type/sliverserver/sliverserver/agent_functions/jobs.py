from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *
from mythic_container.PayloadBuilder import *

from tabulate import tabulate
from ..utils.sliver_connect import sliver_server_clients

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
                display_name="jobs --kill",
                description="kill a job",
                type=ParameterType.ChooseOne,
                dynamic_query_function=self.get_job_ids,
                parameter_group_info=[
                    ParameterGroupInfo(
                        required=True,
                        group_name="kill job",
                        ui_position=1
                    ),
                ]
            ),
            CommandParameter(
                name="kill-all",
                cli_name="kill-all",
                display_name="jobs --kill-all",
                description="kill all jobs",
                type=ParameterType.Boolean,
                default_value=True,
                parameter_group_info=[
                    ParameterGroupInfo(
                        required=True,
                        group_name="kill all jobs",
                        ui_position=1
                    ),
                ]
            ),
        ]

    async def get_job_ids(self, inputMsg: PTRPCDynamicQueryFunctionMessage) -> PTRPCDynamicQueryFunctionMessageResponse:
        client = sliver_server_clients[f"{inputMsg.PayloadUUID}"]
        list_of_jobs = await client.jobs()

        job_ids = []
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
        if (taskData.parameter_group_name == 'Default'):
            await jobs_list(taskData)

        if (taskData.parameter_group_name == 'kill job'):
            await job_kill(taskData)

        if (taskData.parameter_group_name == 'kill all jobs'):
            await kill_all_jobs(taskData)
        
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
    client = sliver_server_clients[f"{taskData.Payload.UUID}"]
    
    jobs = await client.jobs()

    if (len(jobs) == 0):
        return await SendMythicRPCResponseCreate(MythicRPCResponseCreateMessage(
            TaskID=taskData.Task.ID,
            Response="[*] No active jobs".encode("UTF8"),
        ))

    # Formatting
    headers = ["ID", "Name", "Protocol", "Port"]
    data = [(job.ID, job.Name, job.Protocol, job.Port) for job in jobs]
    table = tabulate(data, headers=headers)

    await SendMythicRPCResponseCreate(MythicRPCResponseCreateMessage(
        TaskID=taskData.Task.ID,
        Response=table.encode("UTF8"),
    ))

async def job_kill(taskData: PTTaskMessageAllData):
    client = sliver_server_clients[f"{taskData.Payload.UUID}"]

    job_id = int(taskData.args.get_arg('kill'))
    
    kill_response = await client.kill_job(job_id=job_id)
    await SendMythicRPCResponseCreate(MythicRPCResponseCreateMessage(
        TaskID=taskData.Task.ID,
        Response=f"[*] Successfully killed job #{kill_response.ID}".encode("UTF8"),
    ))

async def kill_all_jobs(taskData: PTTaskMessageAllData):
    client = sliver_server_clients[f"{taskData.Payload.UUID}"]

    job_list = await client.jobs()

    for job in job_list:
        kill_response = await client.kill_job(job_id=job.ID)
        await SendMythicRPCResponseCreate(MythicRPCResponseCreateMessage(
            TaskID=taskData.Task.ID,
            Response=f"[*] Successfully killed job #{kill_response.ID}\n".encode("UTF8"),
        ))
