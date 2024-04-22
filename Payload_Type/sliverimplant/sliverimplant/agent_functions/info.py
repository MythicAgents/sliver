from ..SliverRequests import SliverAPI

from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *
from mythic_container.PayloadBuilder import *

class InfoArguments(TaskArguments):
    def __init__(self, command_line, **kwargs):
        super().__init__(command_line, **kwargs)
        self.args = []

    async def parse_arguments(self):
        pass


class Info(CommandBase):
    cmd = "info"
    needs_admin = False
    help_cmd = "info"
    description = "Get information about a Sliver by name, or for the active Sliver"
    version = 1
    author = "Spencer Adolph"
    argument_class = InfoArguments
    attackmapping = []

    async def create_go_tasking(self, taskData: MythicCommandBase.PTTaskMessageAllData) -> MythicCommandBase.PTTaskCreateTaskingMessageResponse:
        # Command: info <sliver name/session>
        # About: Get information about a Sliver by name, or for the active Sliver.

        # Usage:
        # ======
        #   info [flags] [session]

        # Args:
        # =====
        #   session  string    session ID

        # Flags:
        # ======
        #        -h, --help           display help
        #        -t, --timeout int    command timeout in seconds (default: 60)

        info_results = await info(taskData)

        await SendMythicRPCResponseCreate(MythicRPCResponseCreateMessage(
            TaskID=taskData.Task.ID,
            Response=info_results.encode("UTF8"),
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

async def info(taskData: PTTaskMessageAllData):
    interact, isBeacon = await SliverAPI.create_sliver_interact(taskData)

    #             Session ID: d7e28b37-88be-44f9-ba31-8913bf535d1a
    #               Name: FUNNY_DRIVEWAY
    #           Hostname: ubuntu
    #               UUID: c744e366-d14c-4bf3-94c3-558012eda8a1
    #           Username: root
    #                UID: 0
    #                GID: 0
    #                PID: 120952
    #                 OS: linux
    #            Version: Linux ubuntu 6.5.0-27-generic
    #             Locale: en-US
    #               Arch: amd64
    #          Active C2: mtls://192.168.17.129:443
    #     Remote Address: 192.168.17.129:50072
    #          Proxy URL: 
    # Reconnect Interval: 1m0s
    #      First Contact: Fri Apr 12 21:11:25 CDT 2024 (28m16s ago)
    #       Last Checkin: Fri Apr 12 21:39:39 CDT 2024 (2s ago)

    responseString = []
    responseString.append(f"Session Id: {interact.session_id}")
    responseString.append(f"Name: {interact.name}")
    responseString.append(f"Hostname: {interact.hostname}")
    responseString.append(f"UUID: {interact.uuid}")
    responseString.append(f"Username: {interact.username}")
    responseString.append(f"UID: {interact.uid}")
    responseString.append(f"GID: {interact.gid}")
    responseString.append(f"PID: {interact.pid}")
    responseString.append(f"OS: {interact.os}")
    responseString.append(f"Version: {interact.version}")
    # responseString.append(f"Locale: {interact.L}")
    responseString.append(f"Arch: {interact.arch}")
    responseString.append(f"Active C2: {interact.active_c2}")
    responseString.append(f"Remote Address: {interact.remote_address}")
    responseString.append(f"Proxy URL: {interact.proxy_url}")
    responseString.append(f"Reconnect Interval: {interact.reconnect_interval}")
    # responseString.append(f"First Contact: {interact.last_checkin}")
    responseString.append(f"Last Checkin: {interact.last_checkin}")

    finalResponse = "\n".join(responseString)

    return finalResponse
