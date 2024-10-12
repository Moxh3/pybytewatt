# PyByteWatt

PyByteWatt is a Python package that provides an interface to interact with the Byte Watt API. It allows you to authenticate and retrieve battery data from Byte Watt systems.

## Installation

You can install ByteWatt API Client using pip:

```
pip install pybytewatt
```

## Usage

Here's a basic example of how to use ByteWatt API Client:

```python
import asyncio
from pybytewatt import ByteWattAPIClient

async def main():
    # Create an instance with a custom timeout of 15 seconds
    async with ByteWattAPIClient("your_username", "your_password", "auth_signature", "auth_timestamp", timeout=15.0) as client:
        try:
            battery_data = await client.get_battery_data()
            print(battery_data)
        except Exception as e:
            print(f"An error occurred: {e}")

asyncio.run(main())
```

The `ByteWattAPIClient` class accepts an optional `timeout` parameter (in seconds) for API requests. The default timeout is 10 seconds if not specified.

You can use it with an async context manager (`async with`) to ensure proper cleanup of resources.

If you prefer manual management, you can also use it like this:

```python
client = ByteWattAPIClient("your_username", "your_password", "auth_signature", "auth_timestamp", timeout=20.0)
try:
    battery_data = await client.get_battery_data()
    print(battery_data)
finally:
    await client.close()
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
