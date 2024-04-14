from tabulate import tabulate
from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import SendMythicRPCFileGetContent, MythicRPCFileGetContentMessage
from sliver import SliverClientConfig, SliverClient
from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *
from mythic_container.PayloadBuilder import *
import json


async def create_sliver_client(taskData: PTTaskMessageAllData):
    filecontent = await SendMythicRPCFileGetContent(MythicRPCFileGetContentMessage(
        AgentFileId=taskData.BuildParameters[0].Value
    ))

    config = SliverClientConfig.parse_config(filecontent.Content)
    client = SliverClient(config)
    
    # TODO: cache this (global dict?) - can verify in this function if need to re-create
    await client.connect()

    return client

async def sessions_list(taskData: PTTaskMessageAllData):
    client = await create_sliver_client(taskData)
    sessions = await client.sessions()

    # This is the sliver formatting

    # ID         Transport   Remote Address         Hostname   Username   Operating System   Health  
    # ========== =========== ====================== ========== ========== ================== =========
    # 78c06ded   mtls        192.168.17.129:51042   ubuntu     root       linux/amd64        [ALIVE] 

    # TODO: match sliver formatting
    # what to show when no sessions?

    headers = ["ID", "Transport", "Remote Address", "Hostname", "Username", "Operating System", "Health"]
    data = [(session.ID, session.Transport, session.RemoteAddress, session.Hostname, session.Username, session.OS, "[DEAD]" if session.IsDead else "[ALIVE]") for session in sessions]
    table = tabulate(data, headers=headers)

    return table

async def profiles_list(taskData: PTTaskMessageAllData):
    client = await create_sliver_client(taskData)
    profiles = await client.implant_profiles()

    # TODO: match sliver formatting
    # show nothing if no profiles

    return f"{profiles}"

async def beacons_list(taskData: PTTaskMessageAllData):
    client = await create_sliver_client(taskData)
    beacons = await client.beacons()

    # TODO: match sliver formatting

    #  ID         Name          Transport   Hostname   Username   Operating System   Last Check-In   Next Check-In 
    # ========== ============= =========== ========== ========== ================== =============== ===============
    #  d90a2ec6   DARK_MITTEN   mtls        ubuntu     ubuntu     linux/amd64        2s              1m4s          

    # What to show if no beacons?

    return f"{beacons}"

async def implants_list(taskData: PTTaskMessageAllData):
    client = await create_sliver_client(taskData)
    implants = await client.implant_builds()

    # This is the sliver formatting

    #  Name             Implant Type   Template   OS/Arch           Format   Command & Control               Debug 
    # ================ ============== ========== ============= ============ =============================== =======
    #  DARK_MITTEN      beacon         sliver     linux/amd64   EXECUTABLE   [1] mtls://192.168.17.129:443   false 

    # TODO: match sliver formatting
    # how to show Template?
    # implant.Format is ValueType?
    # C2 only shows first URL
    # What to show if no implants?

    headers = ["Name", "Implant Type", "OS/Arch", "Command & Control", "Debug"]
    data = [(implant.FileName, "beacon" if implant.IsBeacon else "session", f"{implant.GOOS}/{implant.GOARCH}", implant.C2[0].URL, implant.Debug) for implant in implants.values()]
    table = tabulate(data, headers=headers)

    return table

async def jobs_list(taskData: PTTaskMessageAllData):
    client = await create_sliver_client(taskData)
    jobs = await client.jobs()

    # TODO: match sliver formatting

    #  ID   Name   Protocol   Port   Stage Profile 
    # ==== ====== ========== ====== ===============
    #  1    mtls   tcp        443                  

    # [*] No active jobs

    return f"{jobs}"

async def jobs_kill(taskData: PTTaskMessageAllData, job_id: int):
    client = await create_sliver_client(taskData)
    kill_response = await client.kill_job(job_id=job_id)

    # TODO: match sliver formatting

    # [*] Killing job #1 ...
    # [!] Job #1 stopped (tcp/mtls)
    # [*] Successfully killed job #1

    return f"{kill_response}"

async def mtls_start(taskData: PTTaskMessageAllData, port: int):
    client = await create_sliver_client(taskData)

    mtls_start_result = await client.start_mtls_listener(
        host = "0.0.0.0",
        port = port,
        persistent = False,
    )

    # TODO: match sliver formatting

    # [*] Starting mTLS listener ...
    # [*] Successfully started job #1

    return f"{mtls_start_result}"

async def use(taskData: PTTaskMessageAllData, sliver_id: int):
    client = await create_sliver_client(taskData)

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

        new_payload = MythicRPCPayloadCreateFromScratchMessage(
            TaskID=taskData.Task.ID,
            PayloadConfiguration=MythicRPCPayloadConfiguration(
                payload_type="sliverimplant",
                uuid=sliver_id,
                selected_os=sliver_os_table[implant_info.OS],                 
                description=f"sliver {'beaconing' if isBeacon else 'interactive'} implant for {sliver_id}",
                build_parameters=[],
                c2_profiles=[],
                # TODO: figure out if possible to not specify these manually
                commands=['ifconfig', 'download', 'upload', 'ls', 'ps', 'ping', 'whoami', 'screenshot', 'netstat', 'getgid', 'getuid', 'getpid', 'cat', 'cd', 'pwd', 'info', 'execute', 'mkdir', 'shell', 'terminate', 'rm']
            ),
        )
        await SendMythicRPCPayloadCreateFromScratch(new_payload)

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
