import pytest
from pybytewatt import ByteWattAPI

@pytest.mark.asyncio
async def test_bytewatt_api_initialization():
    api = ByteWattAPI("test_user", "test_pass", "test_signature", "test_timestamp")
    assert api.username == "test_user"
    assert api.password == "test_pass"
    assert api.auth_signature == "test_signature"
    assert api.auth_timestamp == "test_timestamp"
    assert api.timeout.total == 5.0

@pytest.mark.asyncio
async def test_bytewatt_api_custom_timeout():
    api = ByteWattAPI("test_user", "test_pass", "test_signature", "test_timestamp", timeout=15.0)
    assert api.timeout.total == 15.0
