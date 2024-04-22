from ..SliverRequests import SliverAPI

from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *
from mythic_container.PayloadBuilder import *

class SshArguments(TaskArguments):
    def __init__(self, command_line, **kwargs):
        super().__init__(command_line, **kwargs)
        self.args = []

    async def parse_arguments(self):
        pass


class Ssh(CommandBase):
    cmd = "ssh"
    needs_admin = False
    help_cmd = "ssh"
    description = "Run an one-off SSH command via the implant"
    version = 1
    author = "Spencer Adolph"
    argument_class = SshArguments
    attackmapping = []

    async def create_go_tasking(self, taskData: MythicCommandBase.PTTaskMessageAllData) -> MythicCommandBase.PTTaskCreateTaskingMessageResponse:
        # Command: ssh
        # About: Run an one-off SSH command via the implant.

        # Usage:
        # ======
        #   ssh [flags] hostname [command...]

        # Args:
        # =====
        #   hostname  string         remote host to SSH to
        #   command   string list    command line with arguments

        # Flags:
        # ======
        #        -h, --help                       display help
        # TODO:  -c, --kerberos-config  string    path to remote Kerberos config file (default: /etc/krb5.conf)
        # TODO:  -k, --kerberos-keytab  string    path to Kerberos keytab file
        # TODO:  -r, --kerberos-realm   string    Kerberos realm
        # TODO:  -l, --login            string    username to use to connect
        # TODO:  -P, --password         string    SSH user password
        # TODO:  -p, --port             uint      SSH port (default: 22)
        # TODO:  -i, --private-key      string    path to private key file
        # TODO:  -u, --signed-user-cert string    path to user signed certificate (certificate based auth)
        # TODO:  -s, --skip-loot                  skip the prompt to use loot credentials
        #        -t, --timeout          int       command timeout in seconds (default: 60)

        response = await ssh(taskData)

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

async def ssh(taskData: PTTaskMessageAllData):
    # interact, isBeacon = await SliverAPI.create_sliver_interact(taskData)

    # ifconfig_results = await interact._stub()

    # if (isBeacon):
    #     ifconfig_results = await ifconfig_results

    return "This command not yet implemented..."
