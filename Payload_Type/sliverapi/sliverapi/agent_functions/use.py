from ..SliverRequests import SliverAPI

from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *
from mythic_container.PayloadBuilder import *
import json


class UseArguments(TaskArguments):
    def __init__(self, command_line, **kwargs):
        super().__init__(command_line, **kwargs)
        self.args = [
            CommandParameter(
                name="id",
                description="beacon or session ID",
                type=ParameterType.String
            ),
        ]

    async def parse_arguments(self):
        self.load_args_from_json_string(self.command_line)


class Use(CommandBase):
    cmd = "use"
    needs_admin = False
    help_cmd = "use"
    description = "Use an implant."
    version = 1
    author = "Spencer Adolph"
    argument_class = UseArguments
    attackmapping = []

    async def create_go_tasking(self, taskData: MythicCommandBase.PTTaskMessageAllData) -> MythicCommandBase.PTTaskCreateTaskingMessageResponse:
        # Command: use [sliver name/session]
        # About: Switch the active Sliver, a valid name must be provided (see sessions).

        # Usage:
        # ======
        #   use [flags] [id]

        # Args:
        # =====
        #   id  string    beacon or session ID

        # Flags:
        # ======
        #        -h, --help           display help
        #        -t, --timeout int    command timeout in seconds (default: 60)

        # Sub Commands:
        # =============
        # TODO:  beacons   Switch the active beacon
        # TODO:  sessions  Switch the active session

        sliver_id = taskData.args.get_arg('id')
        response = await use(taskData, sliver_id)

        await SendMythicRPCResponseCreate(MythicRPCResponseCreateMessage(
            TaskID=taskData.Task.ID,
            Response=response.encode("UTF8"),
        ))
        
        taskResponse = MythicCommandBase.PTTaskCreateTaskingMessageResponse(
            TaskID=taskData.Task.ID,
            Success=True,
            Completed=True,
            TaskStatus="success" if response[1] != '!' else "not found",  # TODO: don't hard code response[1], handle with try/catch errors
        )

        return taskResponse

    async def process_response(self, task: PTTaskMessageAllData, response: any) -> PTTaskProcessResponseMessageResponse:
        resp = PTTaskProcessResponseMessageResponse(TaskID=task.Task.ID, Success=True)
        return resp

async def use(taskData: PTTaskMessageAllData, sliver_id: int):
    client = await SliverAPI.create_sliver_client(taskData)

    beacon_info = await client.beacon_by_id(sliver_id)
    session_info = await client.session_by_id(sliver_id)

    if (not beacon_info and not session_info):
        # TODO: throw error and catch in use.py, and handle sending mythic errors gracefully
        # taskResponse = PTTaskCreateTaskingMessageResponse(
        #     TaskID=taskData.Task.ID,
        #     Success=False,
        #     Completed=True,
        #     Error="id not found in sliver",
        #     TaskStatus=f"[!] no session or beacon found with ID {sliver_id}",
        # )
        # return taskResponse
        return f"[!] no session or beacon found with ID {sliver_id}"

    # TODO: match sliver formatting
    # [*] Active session FUNNY_DRIVEWAY (586a4bdf-ffaf-4136-8387-45cc983ecc0f)

    isBeacon = beacon_info is not None
    implant_info = beacon_info or session_info

    # check if payload already exists, if so, skip to creating the callback
    search = await SendMythicRPCPayloadSearch(MythicRPCPayloadSearchMessage(
        PayloadUUID=sliver_id
    ))

    if (len(search.Payloads) == 0):
        # create the payload
        # TODO: figure out mappings for windows or mac...
        sliver_os_table = {
            'linux': 'Linux'
        }

        # TODO: only include 'shell' for interactive sessions, not beacons
        # print(f"taskid: {taskData.Task.ID}")

        new_payload = MythicRPCPayloadCreateFromScratchMessage(
            TaskID=taskData.Task.ID,
            PayloadConfiguration=MythicRPCPayloadConfiguration(
                payload_type="sliverimplant",
                uuid=sliver_id,
                selected_os=sliver_os_table[implant_info.OS],                 
                description=f"(no download) using sliver {'beaconing' if isBeacon else 'interactive'} implant for {sliver_id}",
                build_parameters=[],
                c2_profiles=[],
                # TODO: figure out if possible to not specify these manually
                commands=['ifconfig', 'download', 'upload', 'ls', 'ps', 'ping', 'whoami', 'screenshot', 'netstat', 'getgid', 'getuid', 'getpid', 'cat', 'cd', 'pwd', 'info', 'execute', 'mkdir', 'shell', 'terminate', 'rm']
            ),
        )
        scratchBuild = await SendMythicRPCPayloadCreateFromScratch(new_payload)

    # create the callback
    extra_info = json.dumps({
        # TODO: if buildparams changes, then this won't work anymore (could make it more resilient)
        "slivercfg_fileid": taskData.BuildParameters[0].Value,
        "type": 'beacon' if isBeacon else 'session'
    })
    response = await SendMythicRPCCallbackCreate(MythicRPCCallbackCreateMessage(
        PayloadUUID=sliver_id,
        C2ProfileName="",
        IntegrityLevel=3,
        Host=implant_info.Hostname,
        User=implant_info.Username,
        Ip=implant_info.RemoteAddress.split(':')[0],
        ExtraInfo=extra_info,
        PID=implant_info.PID
    ))

    return f"[*] Active session FUNNY_DRIVEWAY ({sliver_id})"


