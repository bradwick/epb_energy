# epb_energy/sensor.py
from datetime import datetime

import aiohttp
from homeassistant.helpers.entity import DeviceInfo

from .const import DOMAIN
from .api import EpbEnergyApiClient
from . import EpbEnergyUpdateCoordinator

"""Sensor platform for the EPB Energy integration."""
from homeassistant.components.sensor import SensorEntity, SensorStateClass, SensorDeviceClass
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
        self.id = entry.entry_id

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
        return SensorStateClass.TOTAL

    @property
    def device_class(self) -> SensorDeviceClass | None:
        return SensorDeviceClass.ENERGY

    @property
    def last_reset(self) -> datetime | None:
        return datetime.now()

    @property
    def device_info(self):
        """Return device information."""
        return {
            "identifiers": {(DOMAIN, self.unique_id)},
            "name": "EPB Energy",
            "manufacturer": "EPB",
            "model": "Energy Monitor",
        }

    @property
    def icon(self):
        return self._attr_icon

    @property
    def unique_id(self) -> str | None:
        return self.id
