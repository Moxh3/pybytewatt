import pytest
from pybytewatt import ByteWattAPI

@pytest.mark.asyncio
async def test_bytewatt_api_initialization():
    api = ByteWattAPI("test_user", "test_pass")
    assert api.username == "test_user"
    assert api.password == "test_pass"
    assert api.timeout.total == 5.0

@pytest.mark.asyncio
async def test_bytewatt_api_custom_timeout():
    api = ByteWattAPI("test_user", "test_pass", timeout=15.0)
    assert api.timeout.total == 15.0
