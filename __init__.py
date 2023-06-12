# epb_energy/__init__.py
import logging
from datetime import timedelta

from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import EpbEnergyApiClient
from .const import DOMAIN, CONF_USERNAME, CONF_PASSWORD
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import Config, HomeAssistant

"""The EPB Energy integration."""

DOMAIN = DOMAIN

SCAN_INTERVAL = timedelta(hours=1)

_LOGGER: logging.Logger = logging.getLogger(__package__)


async def async_setup(hass: HomeAssistant, config: Config):
    """Set up this integration using YAML is not supported."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up this integration using UI."""
    _LOGGER.warning("here1")

    if hass.data.get(DOMAIN) is None:
        hass.data.setdefault(DOMAIN, {})

    _LOGGER.warning(f"data {hass.data.get(DOMAIN)}")
    _LOGGER.warning(f"entry {entry.data}")

    client = EpbEnergyApiClient(entry.data.get("username"), entry.data.get("password"))
    coordinator = EpbEnergyUpdateCoordinator(hass, client)

    await coordinator.async_refresh()

    hass.data[DOMAIN][entry.entry_id] = coordinator

    if entry.options.get("sensor", True):
        coordinator.platforms.append("sensor")
        hass.async_add_job(
            hass.config_entries.async_forward_entry_setup(entry, "sensor")
        )
    _LOGGER.warning("here2")

    return True



class EpbEnergyUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    def __init__(self, hass: HomeAssistant, client: EpbEnergyApiClient) -> None:
        """Initialize."""
        self.api = client
        self.platforms = []

        super().__init__(hass, _LOGGER, name=DOMAIN, update_interval=SCAN_INTERVAL)

    async def _async_update_data(self):
        """Update data via library."""
        _LOGGER.warning("here3")

        try:
            return await self.api.get_data()
        except Exception as exception:
            raise UpdateFailed() from exception