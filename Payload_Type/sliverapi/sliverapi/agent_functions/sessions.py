from ..SliverRequests import SliverAPI

from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *
from mythic_container.PayloadBuilder import *
from tabulate import tabulate


class SessionsArguments(TaskArguments):
    def __init__(self, command_line, **kwargs):
        super().__init__(command_line, **kwargs)
        self.args = []

    async def parse_arguments(self):
        pass


class Sessions(CommandBase):
    cmd = "sessions"
    needs_admin = False
    help_cmd = "sessions"
    description = "Get the list of sessions that Sliver is aware of."
    version = 1
    author = "Spencer Adolph"
    argument_class = SessionsArguments
    attackmapping = []

    async def create_go_tasking(self, taskData: MythicCommandBase.PTTaskMessageAllData) -> MythicCommandBase.PTTaskCreateTaskingMessageResponse:      
        # Command: sessions <options>
        # About: List Sliver sessions, and optionally interact or kill a session.

        # Usage:
        # ======
        # sessions [flags]

        # Flags:
        # ======
        # TODO:  -C, --clean               clean out any sessions marked as [DEAD]
        # TODO:  -f, --filter    string    filter sessions by substring
        # TODO:  -e, --filter-re string    filter sessions by regular expression
        # TODO:  -F, --force               force session action without waiting for results
        #        -h, --help                display help
        # TODO:  -i, --interact  string    interact with a session
        # TODO:  -k, --kill      string    kill the designated session
        # TODO:  -K, --kill-all            kill all the sessions
        #        -t, --timeout   int       command timeout in seconds (default: 60)

        # Sub Commands:
        # =============
        # TODO: prune  Kill all stale/dead sessions

        # 'sessions' with no options
        response = await sessions_list(taskData)

        await SendMythicRPCResponseCreate(MythicRPCResponseCreateMessage(
            TaskID=taskData.Task.ID,
            Response=response.encode("UTF8"),
        ))

        taskResponse = MythicCommandBase.PTTaskCreateTaskingMessageResponse(
            TaskID=taskData.Task.ID,
            Success=True,
            Completed=True,
        )

        return taskResponse

    async def process_response(self, task: PTTaskMessageAllData, response: any) -> PTTaskProcessResponseMessageResponse:
        resp = PTTaskProcessResponseMessageResponse(TaskID=task.Task.ID, Success=True)
        return resp
    

async def sessions_list(taskData: PTTaskMessageAllData):
    client = await SliverAPI.create_sliver_client(taskData)
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

