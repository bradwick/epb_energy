# epb_energy/sensor.py
from datetime import datetime

import aiohttp

from const import DOMAIN

"""Sensor platform for the EPB Energy integration."""
from homeassistant.helpers.entity import Entity


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the EPB Energy sensor platform."""

    username = config[DOMAIN]["username"]
    password = config[DOMAIN]["password"]

    # Initialize and add the sensor entity
    sensor = EPBEnergySensor(username, password)
    async_add_entities([sensor])


class EPBEnergySensor(Entity):
    """Representation of a sensor."""

    def __init__(self, username, password):
        """Initialize the sensor."""
        self._username = username
        self._password = password
        self._state = None

    async def async_update(self):
        """Fetch the latest power usage data."""
        async with aiohttp.ClientSession() as session:
            login_url = "https://api.epb.com/web/api/v1/login/"

            async with session.post(
                    login_url,
                    json={"username": self._username, "password": self._password, "grant_type": "PASSWORD"},
            ) as response:
                if response.status == 200:
                    # Authentication successful, retrieve account info
                    account_info_url = "https://api.epb.com/web/api/v1/account-links/"

                    async with session.get(account_info_url) as account_response:
                        if account_response.status == 200:
                            account_data = await account_response.json()
                            gis_id = account_data["premise"]["gis_id"]
                            account_num = account_data["power_account"]["account_id"]

                    data_url = "https://api.epb.com/web/api/v1/usage/power/permanent/compare/hourly"

                    async with session.post(
                            data_url,
                            json={"account_number": account_num, "gis_id": gis_id, "zone_id": "America/New_York",
                                  "usage_date": datetime.today().strftime('%Y-%m-%d')}
                    ) as data_response:
                        data = await data_response.json()
                        # Parse the data and update self._state
                        self._state = data["data"][datetime.now().strftime("%H")]["a"]["values"]["pos_kwh"]
                else:
                    # Authentication failed
                    self._state = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return "EPB Energy"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def device_info(self):
        """Return device information."""
        return {
            "identifiers": {(DOMAIN, self._username)},
            "name": "EPB Energy",
            "manufacturer": "EPB",
            "model": "Energy Monitor",
        }
