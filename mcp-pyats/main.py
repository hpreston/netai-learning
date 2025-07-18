"""
This is an MCP server that uses pyATS to interact with network devices.

Created by: Hank Preston
Date: 2025-07-18
"""

from typing import Optional, Dict, Any
from fastmcp import FastMCP
from genie.testbed import load
import asyncio
import logging


mcp = FastMCP()

# Track connected devices and last time interacted with
#  Example:
#     device_name: {
#         "device_object": {},
#         "last_interaction": "2023-10-01T12:00:00Z"
#     }
connected_devices = {}


def get_pyats_device(
    device_name: str,
    username: str,
    password: str,
    ip_address: str,
    ssh_port: int = 22,
    network_os: Optional[str] = None,
) -> Optional[Any]:
    """
    Retrieves the PyATS device object for a given device name.

    Args:
        device_name (str): The logical name of the device.

    Returns:
        Optional[Any]: The PyATS device object if found, otherwise None.
    """
    logging.info(f"Creating new PyATS device object for {device_name}")

    if network_os is None:
        # Default to "ios" if not defined.  The function will attempt to auto-detect the OS.
        network_os = "ios"

    # Structure a dictionary for the device configuration that can be loaded by PyATS
    device_dict = {
        "devices": {
            device_name: {
                "os": network_os,
                "credentials": {
                    "default": {"username": username, "password": password}
                },
                "connections": {
                    "ssh": {"protocol": "ssh", "ip": ip_address, "port": ssh_port}
                },
            }
        }
    }
    testbed = load(device_dict)
    device = testbed.devices[device_name]

    return device


def _cleanup_connected_devices():
    """
    Cleans up the connected devices dictionary by removing devices that have not been interacted with
    for more than 5 minutes.
    """
    current_time = asyncio.get_event_loop().time()
    to_remove = [
        device_name
        for device_name, info in connected_devices.items()
        if current_time - info["last_interaction"] > 300  # 5 minutes
    ]
    for device_name in to_remove:
        logging.info(f"Removing inactive device: {device_name}")

        # Disconnect the device if it is connected
        device = connected_devices[device_name]["device_object"]
        if device.connected:
            asyncio.create_task(asyncio.to_thread(device.disconnect))

        # Remove from the connected devices dictionary
        del connected_devices[device_name]


@mcp.tool()
def send_show_command(
    command: str,
    device_name: str,
    username: str,
    password: str,
    ip_address: str,
    ssh_port: int = 22,
    network_os: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    """
    Sends a show command to a network device using PyATS and returns the parsed output.

    This function establishes an SSH connection to a network device, executes the specified
    show command, and returns the structured output. It uses PyATS device parsing capabilities
    to convert raw command output into structured data.

    Args:
        command (str): The show command to execute on the device (e.g., 'show version', 'show ip interface brief').
        device_name (str): A logical name for the device, used for identification in PyATS.
        username (str): SSH username for device authentication.
        password (str): SSH password for device authentication.
        ip_address (str): IP address or hostname of the target device.
        ssh_port (int, optional): SSH port number. Defaults to 22.
        network_os (str, optional): Network operating system type (e.g., 'ios', 'iosxe', 'nxos').
                                   If not specified, PyATS will attempt auto-detection.

    Returns:
        Optional[Dict[str, Any]]: Structured dictionary containing the parsed command output,
                                 or None if command execution fails.

    Raises:
        Exception: May raise various exceptions related to connection failures, authentication
                  errors, or command parsing issues. Exceptions are caught and logged.

    Example:
        >>> result = send_show_command(
        ...     command="show version",
        ...     device_name="router1",
        ...     username="admin",
        ...     password="cisco123",
        ...     ip_address="192.168.1.1",
        ...     network_os="iosxe"
        ... )
        >>> if result:
        ...     print(f"Device version: {result.get('version', {}).get('version', 'Unknown')}")
    """

    # Check if we have a device object already connected
    if device_name in connected_devices.keys():
        device = connected_devices[device_name]["device_object"]
        # Update last interaction time
        connected_devices[device_name][
            "last_interaction"
        ] = asyncio.get_event_loop().time()
    else:
        # Create a new device object if not already connected
        device = get_pyats_device(
            device_name=device_name,
            username=username,
            password=password,
            ip_address=ip_address,
            ssh_port=ssh_port,
            network_os=network_os,
        )
        if device is None:
            print(f"Failed to create device object for {device_name}")
            return None

        # Store the device object and last interaction time
        connected_devices[device_name] = {
            "device_object": device,
            "last_interaction": asyncio.get_event_loop().time(),
        }

    try:
        device.connect(
            learn_hostname=True,
            learn_os=True,
            log_stdout=True,
        )
        output = device.parse(command)
    except Exception as e:
        output = f"Error executing command '{command}': {e}"
    finally:
        # Clean up connected devices periodically
        _cleanup_connected_devices()

    return output


if __name__ == "__main__":
    mcp.run(transport="http", port=8002, log_level="DEBUG")
