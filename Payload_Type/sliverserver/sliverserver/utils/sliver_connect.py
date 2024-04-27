import asyncio
from typing import Dict
from sliver import SliverClientConfig, SliverClient, client_pb2

# global 'cache'
sliver_server_clients: Dict[str, SliverClient] = {}


async def connect_and_store_sliver_client(payload_uuid, config_file):
    config = SliverClientConfig.parse_config(config_file)
    client = SliverClient(config)
    await client.connect()

    sliver_server_clients[f"{payload_uuid}"] = client

    async def read_server_events():
        async for data in client.events():
            await handle_sliver_event(data)
    asyncio.create_task(read_server_events())

    return client


async def handle_sliver_event(event: client_pb2.Event):
    print(f"Got Sliver Event: {event.EventType}")
