from ..SliverRequests import SliverAPI

from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *
from mythic_container.PayloadBuilder import *

# from sliver import common_pb2

class StageListenerArguments(TaskArguments):
    def __init__(self, command_line, **kwargs):
        super().__init__(command_line, **kwargs)
        self.args = []

    async def parse_arguments(self):
        pass


class StageListener(CommandBase):
    cmd = "stage_listener"
    needs_admin = False
    help_cmd = "stage_listener"
    description = "Starts a stager listener bound to a Sliver profile"
    version = 1
    author = "Spencer Adolph"
    argument_class = StageListenerArguments
    attackmapping = []

    async def create_go_tasking(self, taskData: MythicCommandBase.PTTaskMessageAllData) -> MythicCommandBase.PTTaskCreateTaskingMessageResponse:
        # Command: stage-listener <options>
        # About: Starts a stager listener bound to a Sliver profile.

        # Usage:
        # ======
        #   stage-listener [flags]

        # Flags:
        # ======
        # TODO:      --aes-encrypt-iv  string    encrypt stage with AES encryption iv
        # TODO:      --aes-encrypt-key string    encrypt stage with AES encryption key
        # TODO:  -c, --cert            string    path to PEM encoded certificate file (HTTPS only)
        # TODO:  -C, --compress        string    compress the stage before encrypting (zlib, gzip, deflate9, none) (default: none)
        #        -h, --help                      display help
        # TODO:  -k, --key             string    path to PEM encoded private key file (HTTPS only)
        # TODO:  -e, --lets-encrypt              attempt to provision a let's encrypt certificate (HTTPS only)
        # TODO:  -P, --prepend-size              prepend the size of the stage to the payload (to use with MSF stagers)
        # TODO:  -p, --profile         string    implant profile name to link with the listener
        # TODO:  -u, --url             string    URL to which the stager will call back to

        response = await stage_listener(taskData)

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


async def stage_listener(taskData: PTTaskMessageAllData):
    client = await SliverAPI.create_sliver_client(taskData)

    

    # start_tcp_stager_listener_result = await client.start_tcp_stager_listener()

    # TODO: match sliver formatting

    return "This command not yet implemented..."
