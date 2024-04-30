from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *
from mythic_container.PayloadBuilder import *
from mythic_container.MythicRPC import MythicRPCPayloadCreateFromScratchMessage, SendMythicRPCPayloadCreateFromScratch, MythicCommandBase, SendMythicRPCResponseCreate, MythicRPCResponseCreateMessage
from mythic_container.MythicGoRPC.send_mythic_rpc_payload_create_from_scratch import MythicRPCPayloadConfiguration

from sliver import SliverClient
from ..utils.sliver_connect import sliver_server_clients, sliver_os_table_lookup

class SyncArguments(TaskArguments):
    def __init__(self, command_line, **kwargs):
        super().__init__(command_line, **kwargs)
        self.args = []

    async def parse_arguments(self):
        pass


class Sync(CommandBase):
    cmd = "sync"
    needs_admin = False
    help_cmd = "sync"
    description = "Sync Sliver callbacks if not already tracked in Mythic."
    version = 1
    author = "Spencer Adolph"
    argument_class = SyncArguments
    attackmapping = []

    async def create_go_tasking(self, taskData: MythicCommandBase.PTTaskMessageAllData) -> MythicCommandBase.PTTaskCreateTaskingMessageResponse:
        client = sliver_server_clients[f"{taskData.Payload.UUID}"]
        slivercfg_fileid = taskData.BuildParameters[0].Value

        await sync_callbacks_from_sliver(client, slivercfg_fileid)

        await SendMythicRPCResponseCreate(MythicRPCResponseCreateMessage(
            TaskID=taskData.Task.ID,
            Response="[*] Synced Sessions and Beacons from Sliver into Mythic Callbacks.".encode("UTF8"),
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


# This function should be refactored to not use hard-coded CallbackID=1 or TaskID=1
# Re-implement at a later time
async def sync_callbacks_from_sliver(client: SliverClient, slivercfg_fileid: str):
    currentSessionsInSliver = await client.sessions()
    for currentSessionInSliver in currentSessionsInSliver:
        payloadInMythic = await SendMythicRPCPayloadSearch(MythicRPCPayloadSearchMessage(
            CallbackID=1,
            PayloadUUID=currentSessionInSliver.ID
        ))

        # is this session not already in Mythic?
        if (len(payloadInMythic.Payloads) == 0):
            # create the payload
            await SendMythicRPCPayloadCreateFromScratch(MythicRPCPayloadCreateFromScratchMessage(
                TaskID=1,
                PayloadConfiguration=MythicRPCPayloadConfiguration(
                    PayloadType="sliverimplant",
                    UUID=currentSessionInSliver.ID,
                    SelectedOS=sliver_os_table_lookup[f"{currentSessionInSliver.OS}"],
                    Description=f"sliver interactive implant {currentSessionInSliver.ID} (sync)",
                    BuildParameters=[
                        MythicRPCPayloadConfigurationBuildParameter(
                            name='configfile_id',
                            value=slivercfg_fileid
                        )
                    ],
                    C2Profiles=[],
                    Commands=[]
                ),
            ))

            # create the callback
            await SendMythicRPCCallbackCreate(MythicRPCCallbackCreateMessage(
                PayloadUUID=currentSessionInSliver.ID,
                C2ProfileName="",
                IntegrityLevel=3, # TODO: could change this to look at UID, Username, etc... (but keep in mind linux vs windows...)
                Host=currentSessionInSliver.Hostname,
                User=currentSessionInSliver.Username,
                Ip=currentSessionInSliver.RemoteAddress.split(':')[0],
                ExtraInfo="",
                PID=currentSessionInSliver.PID
            ))

    currentBeaconsInSliver = await client.beacons()
    for currentBeaconInSliver in currentBeaconsInSliver:
        payloadInMythic = await SendMythicRPCPayloadSearch(MythicRPCPayloadSearchMessage(
            CallbackID=1,
            PayloadUUID=currentBeaconInSliver.ID
        ))

        # is this beaconer not already in Mythic?
        if (len(payloadInMythic.Payloads) == 0):
            # create the payload
            await SendMythicRPCPayloadCreateFromScratch(MythicRPCPayloadCreateFromScratchMessage(
                TaskID=1,
                PayloadConfiguration=MythicRPCPayloadConfiguration(
                    PayloadType="sliverimplant",
                    UUID=currentBeaconInSliver.ID,
                    SelectedOS=sliver_os_table_lookup[f"{currentBeaconInSliver.OS}"],
                    Description=f"sliver beaconing implant {currentBeaconInSliver.ID} (sync)",
                    BuildParameters=[
                        MythicRPCPayloadConfigurationBuildParameter(
                            name='configfile_id',
                            value=slivercfg_fileid
                        )
                    ],
                    C2Profiles=[],
                    Commands=[]
                ),
            ))

            # create the callback
            await SendMythicRPCCallbackCreate(MythicRPCCallbackCreateMessage(
                PayloadUUID=currentBeaconInSliver.ID,
                C2ProfileName="",
                IntegrityLevel=3, # TODO: could change this to look at UID, Username, etc... (but keep in mind linux vs windows...)
                Host=currentBeaconInSliver.Hostname,
                User=currentBeaconInSliver.Username,
                Ip=currentBeaconInSliver.RemoteAddress.split(':')[0],
                ExtraInfo="",
                PID=currentBeaconInSliver.PID,
            ))

