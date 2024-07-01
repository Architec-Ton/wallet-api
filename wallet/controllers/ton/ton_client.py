from TonTools import TonCenterClient


class TonClient:

    def __init__(self):
        self.tc_client = TonCenterClient(
            base_url="https://testnet.toncenter.com/api/v2/",
            key="88d5912ad2394e5cbae97a351bb6a3e1174e09f7956d096beaae3acab91324da",
        )
