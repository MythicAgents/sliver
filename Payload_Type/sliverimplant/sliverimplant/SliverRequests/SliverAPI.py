import asyncio
from mythic_container.MythicCommandBase import PTTaskMessageAllData
from mythic_container.MythicRPC import SendMythicRPCFileGetContent, MythicRPCFileGetContentMessage
from sliver import SliverClientConfig, SliverClient, client_pb2, sliver_pb2
from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *
from mythic_container.PayloadBuilder import *
import json

from mythic_container.LoggingBase import *
from mythic_container.MythicGoRPC import *

# TODO: make this better, if using identify all fields that will be used / handle emptying when exiting
global_dict = {
    'sliver_clients': {}
}

async def create_sliver_interact(taskData: PTTaskMessageAllData):
    # check to see if its cached
    if (f"{taskData.Callback.ID}" in global_dict['sliver_clients'].keys()):
        return global_dict['sliver_clients'][f"{taskData.Callback.ID}"]['interact'], global_dict['sliver_clients'][f"{taskData.Callback.ID}"]['isBeacon']

    extraInfoObj = json.loads(taskData.Callback.ExtraInfo)
    configfile = extraInfoObj['slivercfg_fileid']

    # otherwise get it
    filecontent = await SendMythicRPCFileGetContent(MythicRPCFileGetContentMessage(
        AgentFileId=configfile
    ))

    config = SliverClientConfig.parse_config(filecontent.Content)
    client = SliverClient(config)
    await client.connect()

    callback_extra_info = json.loads(taskData.Callback.ExtraInfo)
    isBeacon = callback_extra_info['type'] == 'beacon'
    if (isBeacon):
        interact = await client.interact_beacon(taskData.Payload.UUID)
    else:
        interact = await client.interact_session(taskData.Payload.UUID)

    # cache it for later
    # TODO: memory leak if this never gets removed? (why useful to implement 'exit' command)
    global_dict['sliver_clients'][f"{taskData.Callback.ID}"] = {
        'interact': interact,
        'isBeacon': isBeacon
    }

    return interact, isBeacon

async def shell(taskData: PTTaskMessageAllData):
    interact, isBeacon = await create_sliver_interact(taskData)

    # TODO: make a different beacon payload with that command not listed? (or take this command out manually with rpc?)
    if (isBeacon):
        return None # TODO: throw error and more gracefully handle with (not supported for beacons)
    
    # typed as rpcpb.SliverRPCClient in TS 
    # but here is 'SliverRPCStub' type (python)
    # (confirmed in pwd code which is working)
    _rpc = interact._stub # doing this to match the this._rpc in the client.ts
    request = interact._request # helper function?
    _tunnelStream = _rpc.TunnelData() # line 622 in client.ts (in the connect() function)

    global_dict['interact'] = interact 
    global_dict['tunnel_stream'] = _tunnelStream
    
    tunnel = sliver_pb2.Tunnel(SessionID=interact.session_id) # line 461/462 client.ts
    rpcTunnel = await _rpc.CreateTunnel(tunnel) # line 464

    tunnelId = rpcTunnel.TunnelID # line 468 in client.ts
    tunnelData = sliver_pb2.TunnelData() # line 469 in client.ts
    tunnelData.TunnelID = tunnelId
    tunnelData.SessionID = interact.session_id
    await _tunnelStream.write(tunnelData) # bind tunnel? (line 519 client.ts and tunnels.go#L128)

    global_dict['tunnel_id'] = tunnelId
    global_dict['session_id'] = interact.session_id

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

# TODO: move this somewhere else? (shell functionality might be its own file by this point...)
class MyLogger(Log):
    async def new_task(self, msg: LoggingMessage) -> None:
        if (not msg.Data.IsInteractiveTask):
            return

        # TODO: prevent follow up tasks after 'exit'

        # logger.info(msg)

        if msg.Data.DisplayParams == '':
            return
        
        # TODO: check if for this session / task, etc...

        interact = global_dict['interact']
        _tunnelStream = global_dict['tunnel_stream']
        tunnelId = global_dict['tunnel_id']
        sessionId = global_dict['session_id']

        if msg.Data.DisplayParams == 'exit\n':
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

