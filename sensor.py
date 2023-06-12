# epb_energy/sensor.py
from datetime import datetime

import aiohttp

from .const import DOMAIN
from .api import EpbEnergyApiClient
from . import EpbEnergyUpdateCoordinator

"""Sensor platform for the EPB Energy integration."""
from homeassistant.components.sensor import SensorEntity, SensorStateClass
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

    @property
    def name(self):
        """Return the name of the sensor."""
        return "EPB Energy"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.coordinator.api.kwh

    @property
    def native_unit_of_measurement(self):
        return "kWh"

    @property
    def state_class(self) -> SensorStateClass | str | None:
        return SensorStateClass.MEASUREMENT

    @property
    def last_reset(self) -> datetime | None:
        return datetime.today()

    @property
    def device_info(self):
        """Return device information."""
        return {
            "identifiers": {(DOMAIN, self.sensor_name)},
            "name": "EPB Energy",
            "manufacturer": "EPB",
            "model": "Energy Monitor",
        }

    @property
    def icon(self):
        return self._attr_icon
