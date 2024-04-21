from ..SliverRequests import SliverAPI

from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *
from mythic_container.PayloadBuilder import *

from sliver import SliverClientConfig, SliverClient, client_pb2

from tabulate import tabulate

class ProfilesArguments(TaskArguments):
    def __init__(self, command_line, **kwargs):
        super().__init__(command_line, **kwargs)
        self.args = [
            CommandParameter(
                name="list",
                cli_name="list",
                display_name="profiles",
                type=ParameterType.Boolean,
                default_value=True,
                description="profiles",
                parameter_group_info=[
                    ParameterGroupInfo(
                        required=False,
                        group_name="Default",
                        ui_position=1
                    ),
            ]),
            CommandParameter(
                name="new",
                cli_name="new",
                display_name="profiles new",
                type=ParameterType.Boolean,
                default_value=True,
                description="profiles new",
                parameter_group_info=[
                    ParameterGroupInfo(
                        required=False,
                        group_name="new",
                        ui_position=1
                    ),
            ]),
            CommandParameter(
                name="new_beacon",
                cli_name="new_beacon",
                display_name="profiles new beacon",
                type=ParameterType.Boolean,
                default_value=True,
                description="profiles new beacon",
                parameter_group_info=[
                    ParameterGroupInfo(
                        required=False,
                        group_name="new beacon",
                        ui_position=1
                    ),
            ]),
            CommandParameter(
                name="rm",
                cli_name="rm",
                display_name="profiles rm",
                type=ParameterType.Boolean,
                default_value=True,
                description="profiles rm",
                parameter_group_info=[
                    ParameterGroupInfo(
                        required=False,
                        group_name="rm",
                        ui_position=1
                    ),
            ]),
            CommandParameter(
                name="generate",
                cli_name="generate",
                display_name="profiles generate",
                type=ParameterType.Boolean,
                default_value=True,
                description="profiles generate",
                parameter_group_info=[
                    ParameterGroupInfo(
                        required=False,
                        group_name="generate",
                        ui_position=1
                    ),
            ]),
            CommandParameter(
                name="profile_name",
                cli_name="profile_name",
                display_name="profile name",
                type=ParameterType.String,
                description="name of the profile",
                # validation_func=self.validate_not_empty_string,
                parameter_group_info=[
                    ParameterGroupInfo(
                        required=True,
                        group_name="new",
                        ui_position=100
                    ),
                    ParameterGroupInfo(
                        required=True,
                        group_name="new beacon",
                        ui_position=100
                    ),
                ]),
            CommandParameter(
                name="profile_choice",
                cli_name="profile_choice",
                display_name="profile choice",
                type=ParameterType.ChooseOne,
                dynamic_query_function=self.get_profiles,
                description="profile to choose",
                parameter_group_info=[
                    ParameterGroupInfo(
                        required=True,
                        group_name="rm",
                        ui_position=100
                    ),
                    ParameterGroupInfo(
                        required=True,
                        group_name="generate",
                        ui_position=100
                    ),
                ]),
            CommandParameter(
                name="os",
                cli_name="os",
                display_name="os",
                type=ParameterType.ChooseOne,
                choices=['linux', 'windows'],
                description="os",
                parameter_group_info=[
                    ParameterGroupInfo(
                        required=False,
                        group_name="new",
                        ui_position=2
                    ),
                    ParameterGroupInfo(
                        required=False,
                        group_name="new beacon",
                        ui_position=2
                    ),
                ]),
            CommandParameter(
                name="mtls",
                cli_name="mtls",
                display_name="mtls",
                type=ParameterType.String,
                description="mtls",
                parameter_group_info=[
                    ParameterGroupInfo(
                        required=False,
                        group_name="new",
                        ui_position=2
                    ),
                    ParameterGroupInfo(
                        required=False,
                        group_name="new beacon",
                        ui_position=2
                    ),
                ]),
            CommandParameter(
                name="skip_symbols",
                cli_name="skip_symbols",
                display_name="skip symbols",
                type=ParameterType.Boolean,
                description="skip symbols",
                parameter_group_info=[
                    ParameterGroupInfo(
                        required=False,
                        group_name="new",
                        ui_position=2
                    ),
                    ParameterGroupInfo(
                        required=False,
                        group_name="new beacon",
                        ui_position=2
                    ),
                ]),
            CommandParameter(
                name="seconds",
                cli_name="seconds",
                display_name="seconds",
                type=ParameterType.Number,
                default_value=60,
                description="seconds",
                parameter_group_info=[
                    ParameterGroupInfo(
                        required=False,
                        group_name="new beacon",
                        ui_position=50
                    ),
                ]),
        ]

    # def validate_not_empty_string(self, x: str):
    #     if (len(x) == 0):
    #         raise ValueError('Input cannot be an empty string')
    #     return True

    # TODO: this is also duplicated in the below profiles_list
    async def get_profiles(self, inputMsg: PTRPCDynamicQueryFunctionMessage) -> PTRPCDynamicQueryFunctionMessageResponse:
        profile_names = []

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
        profiles = await client.implant_profiles()
        for profile in profiles:
            profile_names.append(profile.Name)

        return PTRPCDynamicQueryFunctionMessageResponse(Success=True, Choices=profile_names)

    async def parse_arguments(self):
        self.load_args_from_json_string(self.command_line)

class Profiles(CommandBase):
    cmd = "profiles"
    needs_admin = False
    help_cmd = "profiles"
    description = "Configure / List profiles."
    version = 1
    author = "Spencer Adolph"
    argument_class = ProfilesArguments
    attackmapping = []

    async def create_go_tasking(self, taskData: MythicCommandBase.PTTaskMessageAllData) -> MythicCommandBase.PTTaskCreateTaskingMessageResponse:
        # List existing profiles

        # Usage:
        # ======
        #   profiles [flags]

        # Sub Commands:
        # =============
        #  generate  Generate implant from a profile
        #  new       Create a new implant profile (interactive session)
        #  rm        Remove a profile

        if (taskData.parameter_group_name == 'Default'):
            response = await profiles_list(taskData)

        if (taskData.parameter_group_name == 'new' or taskData.parameter_group_name == 'new_beacon'):
            response = await profiles_new(taskData)

        if (taskData.parameter_group_name == 'rm'):
            response = await profiles_rm(taskData)
        
        if (taskData.parameter_group_name == 'generate'):
            return await profiles_generate(taskData)
        
    
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

async def profiles_list(taskData: PTTaskMessageAllData):
    client = await SliverAPI.create_sliver_client(taskData)
    profiles = await client.implant_profiles()

    # TODO: doesn't display multiple C2
    # TODO: confirm accessing output format with .keys will always be in the same order
    headers = ["Profile Name", "Implant Type", "Platform", "Command & Control", "Debug", "Format", "Obfuscation"]
    data = [(profile.Name, "beacon" if profile.Config.IsBeacon else "session", f"{profile.Config.GOOS}/{profile.Config.GOARCH}", profile.Config.C2[0].URL, profile.Config.Debug, client_pb2.OutputFormat.keys()[profile.Config.Format], "disabled" if not profile.Config.ObfuscateSymbols else "enabled") for profile in profiles]
    table = tabulate(data, headers=headers)

    return table

async def profiles_new(taskData: PTTaskMessageAllData):
    client = await SliverAPI.create_sliver_client(taskData)

    # TODO: handle if new_beacon

    profile_name = taskData.args.get_arg('profile_name')
    mtls = taskData.args.get_arg('mtls')
    os_type = taskData.args.get_arg('os')
    skip_symbols = taskData.args.get_arg('skip_symbols')
    is_beacon = taskData.parameter_group_name == 'new_beacon'
    # file_format = taskData.args.get_arg('format')
    # seconds = taskData.args.get_arg('seconds')

    new_profile = client_pb2.ImplantProfile(
        Name=profile_name,
        Config=client_pb2.ImplantConfig(
            IsBeacon=is_beacon,
            ObfuscateSymbols=not skip_symbols,
            GOOS=os_type,
            C2=[client_pb2.ImplantC2(URL=f'mtls://{mtls}')],
            GOARCH='amd64',
            Format=client_pb2.OutputFormat.EXECUTABLE,
        )
    )

    profile_create_results = await client.save_implant_profile(profile=new_profile)

    return f"[*] Saved new implant profile {profile_name}"

async def profiles_rm(taskData: PTTaskMessageAllData):
    client = await SliverAPI.create_sliver_client(taskData)
    profile_name = taskData.args.get_arg('profile_choice')
    delete_profile_result = await client.delete_implant_profile(profile_name=profile_name)
    return "Deleted Profile"

async def profiles_generate(taskData: PTTaskMessageAllData):
    return "Not yet implemented..."

