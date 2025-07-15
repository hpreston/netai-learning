from typing import Optional, Dict, Any
from fastmcp import FastMCP
from genie.testbed import load
import asyncio


mcp = FastMCP()


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

    try:
        device.connect(learn_hostname=True, learn_os=True, log_stdout=True)
        output = device.parse(command)
        # Disconnect in the background without waiting
        asyncio.create_task(asyncio.to_thread(device.disconnect))
        return output
    except Exception as e:
        print(f"Error executing command '{command}': {e}")
        return None


if __name__ == "__main__":
    mcp.run(transport="http", port=8002, log_level="DEBUG")
