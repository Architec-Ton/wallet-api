import logging

from tonsdk.utils import Address

from .ton.ton_client import TonClient
from .wallet_controller import WalletController


class BankController:

    def __init__(self):
        self.client = TonClient()

    async def get_banks(self, address: Address):
        bnks = await WalletController().get_assets(address, only_active=False, include_symbols=["BNK"])

        if len(bnks) > 0 and bnks[0].amount is not None:
            return bnks[0].amount

        return 0

    async def get_stacked_banks(self, address: Address):
        # jetton_master = await JettonMaster.filter(symbol="BNK").first()
        #
        # if jetton_master is None:
        #     return 0
        #
        # cell = Cell()
        # cell.bits.write_address(Address(address))
        # stack = [["tvm.Slice", bytes_to_b64str(cell.to_boc(False))]]
        # stake_address_raw = await self.client.tc_client.run_get_method(
        #     "calculate_stake_address", jetton_master.address.to_string(), stack
        # )
        # cell_out = Cell.one_from_boc(base64.b64decode(stake_address_raw[0][1]["bytes"]))
        # stake_address = read_address(cell_out)
        # cell = Cell()
        # cell.bits.write_address(Address(address))
        # stack = [["tvm.Slice", bytes_to_b64str(cell.to_boc(False))]]
        # amount_time_raw = await self.client.tc_client.run_get_method(
        #     "amountTime", stake_address.to_string(), stack
        # )
        # logging.info("---" * 40)
        # logging.info(amount_time_raw)
        # logging.info(f"stake_address: {base64.b64decode(stake_address[1][1]['bytes'])}")

        return 0

    async def get_arcs(self, address: Address):
        arcs = await WalletController().get_assets(address, only_active=False, include_symbols=["ARC"])
        logging.info(arcs)
        if len(arcs) > 0 and arcs[0].amount is not None:
            logging.info(f"amount: {arcs[0].amount}")
            return arcs[0].amount

        return 0

    async def get_stacked_arcs(self, address: Address):
        return 0

    # async def get_transaction(self, address: Address, limit: int = 3):
