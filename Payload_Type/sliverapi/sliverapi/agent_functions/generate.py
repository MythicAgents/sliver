from ..SliverRequests import SliverAPI

from mythic_container.MythicCommandBase import *
from mythic_container.PayloadBuilder import *
from mythic_container.MythicRPC import MythicRPCPayloadCreateFromScratchMessage, MythicCommandBase, SendMythicRPCPayloadCreateFromScratch, SendMythicRPCResponseCreate, MythicRPCResponseCreateMessage

from mythic_container.MythicGoRPC.send_mythic_rpc_payload_create_from_scratch import MythicRPCPayloadConfiguration

class GenerateArguments(TaskArguments):
    def __init__(self, command_line, **kwargs):
        super().__init__(command_line, **kwargs)
        self.args = [
            CommandParameter(
                name="os",
                cli_name="os",
                display_name="os",
                description="operating system",
                default_value='windows',
                type=ParameterType.ChooseOne,
                choices=["linux", "windows"]
            ),
            CommandParameter(
                name="mtls",
                cli_name="mtls",
                display_name="mtls",
                description="mtls ip:port to use",
                type=ParameterType.String,
            ),
        ]

    async def parse_arguments(self):
        self.load_args_from_json_string(self.command_line)


class Generate(CommandBase):
    cmd = "generate"
    needs_admin = False
    help_cmd = "generate"
    description = "Generate a new sliver binary"
    version = 1
    author = "Spencer Adolph"
    argument_class = GenerateArguments
    attackmapping = []

    async def create_go_tasking(self, taskData: MythicCommandBase.PTTaskMessageAllData) -> MythicCommandBase.PTTaskCreateTaskingMessageResponse:
        # Command: generate <options>
        # About: Generate a new sliver binary and saves the output to the cwd or a path specified with --save.

        # Flags:
        # ======
        # TODO:  -a, --arch               string    cpu architecture (default: amd64)
        # TODO:  -c, --canary             string    canary domain(s)
        # TODO:  -d, --debug                        enable debug features
        # TODO:  -O, --debug-file         string    path to debug output
        # TODO:  -G, --disable-sgn                  disable shikata ga nai shellcode encoder
        # TODO:  -n, --dns                string    dns connection strings
        # TODO:  -e, --evasion                      enable evasion features (e.g. overwrite user space hooks)
        # TODO:  -E, --external-builder             use an external builder
        # TODO:  -f, --format             string    Specifies the output formats, valid values are: 'exe', 'shared' (for dynamic libraries), 'service' (see `psexec` for more info) and 'shellcode' (windows only) (default: exe)
        # TODO:  -b, --http               string    http(s) connection strings
        # TODO:  -X, --key-exchange       int       wg key-exchange port (default: 1337)
        # TODO:  -w, --limit-datetime     string    limit execution to before datetime
        # TODO:  -x, --limit-domainjoined           limit execution to domain joined machines
        # TODO:  -F, --limit-fileexists   string    limit execution to hosts with this file in the filesystem
        # TODO:  -z, --limit-hostname     string    limit execution to specified hostname
        # TODO:  -L, --limit-locale       string    limit execution to hosts that match this locale
        # TODO:  -y, --limit-username     string    limit execution to specified username
        # TODO:  -k, --max-errors         int       max number of connection errors (default: 1000)
        # TODO:  -m, --mtls               string    mtls connection strings
        # TODO:  -N, --name               string    agent name
        # TODO:  -p, --named-pipe         string    named-pipe connection strings
        # TODO:  -o, --os                 string    operating system (default: windows)
        # TODO:  -P, --poll-timeout       int       long poll request timeout (default: 360)
        # TODO:  -j, --reconnect          int       attempt to reconnect every n second(s) (default: 60)
        # TODO:  -R, --run-at-load                  run the implant entrypoint from DllMain/Constructor (shared library only)
        # TODO:  -l, --skip-symbols                 skip symbol obfuscation
        # TODO:  -Z, --strategy           string    specify a connection strategy (r = random, rd = random domain, s = sequential)
        # TODO:  -T, --tcp-comms          int       wg c2 comms port (default: 8888)
        # TODO:  -i, --tcp-pivot          string    tcp-pivot connection strings
        # TODO:  -I, --template           string    implant code template (default: sliver)
        # TODO:  -g, --wg                 string    wg connection strings

        # Beacon specific things
        # TODO:  -D, --days               int       beacon interval days (default: 0)
        # TODO:  -H, --hours              int       beacon interval hours (default: 0)
        # TODO:  -J, --jitter             int       beacon interval jitter in seconds (default: 30)
        # TODO:  -M, --minutes            int       beacon interval minutes (default: 0)
        # TODO:  -S, --seconds            int       beacon interval seconds (default: 60)

        # Sub Commands:
        # =============
        # TODO:  beacon  Generate a beacon binary
        # TODO:  info    Get information about the server's compiler
        # TODO:  stager  Generate a stager using Metasploit (requires local Metasploit installation)

        os = taskData.args.get_arg('os')
        mtls = taskData.args.get_arg('mtls')
        sliverconfig_file_uuid = taskData.BuildParameters[0].Value

        sliver_os_table = {
            'linux': 'Linux'
        }

        # TODO: include 'shell' for sessions, but not for beaconers

        createMessage = MythicRPCPayloadCreateFromScratchMessage(
            TaskID=taskData.Task.ID,
            PayloadConfiguration=MythicRPCPayloadConfiguration(
                PayloadType="sliverimplant",
                SelectedOS=sliver_os_table[os],                 
                Description="generated payload: sliver implant",
                BuildParameters=[
                    MythicRPCPayloadConfigurationBuildParameter(
                        name='sliverconfig_file_uuid',
                        value=sliverconfig_file_uuid
                    ),
                    MythicRPCPayloadConfigurationBuildParameter(
                        name='os',
                        value=os
                    ),
                    MythicRPCPayloadConfigurationBuildParameter(
                        name='mtls',
                        value=f"mtls://{mtls}"
                    ),
                ],
                C2Profiles=[],
                Commands=['ifconfig', 'download', 'upload', 'ls', 'ps', 'ping', 'whoami', 'screenshot', 'netstat', 'getgid', 'getuid', 'getpid', 'cat', 'cd', 'pwd', 'info', 'execute', 'mkdir', 'shell', 'terminate', 'rm']
            ),
        )
        await SendMythicRPCPayloadCreateFromScratch(createMessage)
        
        await SendMythicRPCResponseCreate(MythicRPCResponseCreateMessage(
            TaskID=taskData.Task.ID,
            Response="generated implant".encode("UTF8"),
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
