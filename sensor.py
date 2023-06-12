# epb_energy/sensor.py
from datetime import datetime

import aiohttp

from .const import DOMAIN
from .api import EpbEnergyApiClient

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
        client = EpbEnergyApiClient(self._username, self._password)
        self._state = await client.get_data()

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
