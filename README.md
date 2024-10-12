# PyByteWatt

PyByteWatt is a Python package that provides an interface to interact with the Byte Watt API. It allows you to authenticate and retrieve battery data from Byte Watt systems.

## Installation

You can install PyByteWatt using pip:

```
pip install pybytewatt
```

## Usage

Here's a basic example of how to use PyByteWatt:

```python
import asyncio
import aiohttp
from pybytewatt import ByteWattAPI

async def main():
    async with aiohttp.ClientSession() as session:
        api = ByteWattAPI("your_username", "your_password", "auth_signature", "auth_timestamp", session)
        try:
            battery_data = await api.get_battery_data()
            print(battery_data)
        except Exception as e:
            print(f"An error occurred: {e}")

asyncio.run(main())
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
