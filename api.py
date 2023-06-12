import logging
from datetime import datetime

import aiohttp

_LOGGER: logging.Logger = logging.getLogger(__package__)


class EpbEnergyApiClient:
    def __init__(self, username, password):
        self.session = aiohttp.ClientSession()
        self.username = username
        self.password = password
        self.token = None
        self.kwh = 0

    async def login(self):
        login_url = "https://api.epb.com/web/api/v1/login/"
        async with self.session.post(
                login_url,
                json={"username": self.username, "password": self.password, "grant_type": "PASSWORD"},
        ) as response:
            if response.status != 200:
                return False
            _LOGGER.warning(await response.text())
        _LOGGER.warning("done_logging in")
        return True

    async def get_data(self):
        _LOGGER.warning("here4")

        await self.login()
        async with self.session as session:
            _LOGGER.warning("here44")
            account_info_url = "https://api.epb.com/web/api/v1/account-links/"
            try:
                async with session.get(account_info_url) as account_response:
                    _LOGGER.warning("here444")

                    _LOGGER.warning(f"status: {account_response.status}")
                    _LOGGER.warning(f"response: {await account_response.text()}")
                    if account_response.status == 200:
                        account_data = await account_response.json()
                        gis_id = account_data["premise"]["gis_id"]
                        account_num = account_data["power_account"]["account_id"]
                    _LOGGER.warning("here5")


                    data_url = "https://api.epb.com/web/api/v1/usage/power/permanent/compare/hourly"

                    async with session.post(
                            data_url,
                            json={"account_number": account_num, "gis_id": gis_id, "zone_id": "America/New_York",
                                  "usage_date": datetime.today().strftime('%Y-%m-%d')}
                    ) as data_response:
                        data = await data_response.json()
                        # Parse the data and update self._state
                        _LOGGER.warning("here6")
                        _LOGGER.warning(data)
                        self.kwh = data["data"][datetime.now().strftime("%H")]["a"]["values"]["pos_kwh"]
            except Exception as e:
                _LOGGER.warning(e)
