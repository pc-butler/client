import host_discovery
import wake_device
import asyncio
import sys
from datetime import datetime


async def perform_host_discovery():
    devices = host_discovery.find_hosts()  # ARP Scan local network
    host_discovery.update_database(devices)  # Update web server


async def wake_devices():
    queue = wake_device.get_queue()
    wake_device.wake_devices(queue)

async def main():
    now = datetime.now().strftime("%H-%M-%S")
    hostd_task = loop.create_task(perform_host_discovery())
    wake_task = loop.create_task(wake_devices())
    await asyncio.wait([hostd_task, wake_task])


if __name__ == "__main__":
    print("Starting PC Butler...")
    try:
        loop = asyncio.get_event_loop()
        loop.run_forever()
    except KeyboardInterrupt:
        sys.exit()
