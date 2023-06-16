import logging
from datetime import datetime

import aiohttp
from pytz import timezone

_LOGGER: logging.Logger = logging.getLogger(__package__)


class EpbEnergyApiClient:
    def __init__(self, username, password):
        self.session = aiohttp.ClientSession()
        self.username = username
        self.password = password
        self.kwh = 0

    async def login(self):
        login_url = "https://api.epb.com/web/api/v1/login/"
        async with self.session.post(
                login_url,
                json={"username": self.username, "password": self.password, "grant_type": "PASSWORD"},
        ) as response:
            if response.status != 200:
                return False
            json = await response.json()
            self.session.headers.add("X-User-Token", json["tokens"]["access"]["token"])
        return True

    async def get_data(self):

        await self.login()
        async with self.session as session:
            account_info_url = "https://api.epb.com/web/api/v1/account-links/"
            try:
                async with session.get(account_info_url) as account_response:

                    if account_response.status == 200:
                        account_data = await account_response.json()
                        gis_id = account_data[0]["premise"]["gis_id"]
                        account_num = account_data[0]["power_account"]["account_id"]

                    data_url = "https://api.epb.com/web/api/v1/usage/power/permanent/compare/hourly"
                    tz = timezone("EST")

                    async with session.post(
                            data_url,
                            json={"account_number": account_num, "gis_id": gis_id, "zone_id": "America/New_York",
                                  "usage_date": datetime.today().strftime('%Y-%m-%d')}
                    ) as data_response:
                        data = await data_response.json()
                        # Parse the data and update self._state

                        this_hour = int(datetime.now(tz).strftime("%H"))


                        self.kwh = data["data"][this_hour]["a"]["values"]["pos_kwh"]
            except Exception as e:
                _LOGGER.warning(e)
