# epb_energy/sensor.py
from datetime import datetime

import aiohttp

from .const import DOMAIN
from .api import EpbEnergyApiClient
from . import EpbEnergyUpdateCoordinator

"""Sensor platform for the EPB Energy integration."""
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the EPB Energy sensor platform."""
    # Initialize and add the sensor entity
    coordinator = hass.data[DOMAIN][entry.entry_id]
    sensor = EPBEnergySensor(coordinator, entry)
    async_add_entities([sensor], True)


class EPBEnergySensor(SensorEntity):
    """Representation of a sensor."""

    def __init__(self,
                 coordinator: EpbEnergyUpdateCoordinator,
                 entry: ConfigEntry):
        """Initialize the sensor."""
        super().__init__()
        self.coordinator = coordinator
        self.sensor_name = "energy_usage"
        self._attr_icon = "mdi:home-lightning-bolt"
        self.friendly_name: "EPB Energy Usage"

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
        return self.coordinator.api.get_data()

    @property
    def device_info(self):
        """Return device information."""
        return {
            "identifiers": {(DOMAIN, self._username)},
            "name": "EPB Energy",
            "manufacturer": "EPB",
            "model": "Energy Monitor",
        }
