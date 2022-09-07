import json

import pytest
from engi_cli.blockchain_api import get_account, get_health


@pytest.mark.asyncio
async def test_health():
    result = await get_health()
    health = result["health"]
    assert "Engi" in health["chain"]
    assert health["peerCount"] > 0
    assert health["status"] == "ONLINE"


@pytest.mark.asyncio
async def test_create_user(user):
    assert not user.error
    result = json.loads(user.json())
    print(result)
    assert result["UserName"] == "cck197"
    assert len(result["Mnemonic"].split()) == 12
    assert "WalletAddress" in result


@pytest.mark.asyncio
async def test_get_account(user):
    # the wallet is created but the account is not
    # TODO add script to fund the account
    result = await get_account(user.wallet_address)
    assert result["account"] == None
