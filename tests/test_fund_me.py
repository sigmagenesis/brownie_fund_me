from scripts.helpful_scripts import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from scripts.deploy import deploy_fund_me
from brownie import network, accounts, exceptions
import pytest


def test_can_fund_and_withdraw():
    account = get_account()
    fund_me_contract = deploy_fund_me()
    entrance_fee = fund_me_contract.getEntranceFee() + 100
    tx = fund_me_contract.fund({"from": account, "value": entrance_fee})
    tx.wait(1)

    assert fund_me_contract.addressToAmountFunded(account.address) == entrance_fee

    tx2 = fund_me_contract.withdraw({"from": account})
    tx2.wait(1)

    assert fund_me_contract.addressToAmountFunded(account.address) == 0


def test_only_owner_can_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("only for local testing")
    fund_me_contract = deploy_fund_me()
    bad_actor = accounts.add()
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me_contract.withdraw({"from": bad_actor})
