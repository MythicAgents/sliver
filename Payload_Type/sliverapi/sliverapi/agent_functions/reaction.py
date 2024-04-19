from ..SliverRequests import SliverAPI

from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *
from mythic_container.PayloadBuilder import *

# from sliver import common_pb2

class ReactionArguments(TaskArguments):
    def __init__(self, command_line, **kwargs):
        super().__init__(command_line, **kwargs)
        self.args = []

    async def parse_arguments(self):
        pass


class Reaction(CommandBase):
    cmd = "reaction"
    needs_admin = False
    help_cmd = "reaction"
    description = "Automate commands in reaction to event(s)"
    version = 1
    author = "Spencer Adolph"
    argument_class = ReactionArguments
    attackmapping = []

    async def create_go_tasking(self, taskData: MythicCommandBase.PTTaskMessageAllData) -> MythicCommandBase.PTTaskCreateTaskingMessageResponse:
        # Command: reaction
        # About: Automate commands in reaction to event(s). The built-in
        # reactions do not support variables or logic, they simply allow you to run verbatim
        # commands when an event occurs. To implement complex event-based logic we recommend
        # using SliverPy (Python) or sliver-script (TypeScript/JavaScript).

        # Reactable Events:
        #    session-connected  Triggered when a new session is opened to a target
        #      session-updated  Triggered on changes to session metadata
        # session-disconnected  Triggered when a session is closed (for any reason)
        #               canary  Triggered when a canary is burned or created
        #           watchtower  Triggered when implants are discovered on threat intel platforms
        #           loot-added  Triggered when a new piece of loot is added to the server
        #         loot-removed  Triggered when a piece of loot is removed from the server


        # Usage:
        # ======
        #   reaction [flags]

        # Flags:
        # ======
        # TODO:  -h, --help     display help

        # Sub Commands:
        # =============
        # TODO:  reload  Reload reactions from disk, replaces the running configuration
        # TODO:  save    Save current reactions to disk
        # TODO:  set     Set a reaction to an event
        # TODO:  unset   Unset an existing reaction

        response = await reaction(taskData)

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


async def reaction(taskData: PTTaskMessageAllData):
    # client = await SliverAPI.create_sliver_client(taskData)

    # reaction_result = await client._stub.rea

    # TODO: match sliver formatting

    return "This command not yet implemented..."
