# epb_energy/__init__.py
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from const import DOMAIN, CONF_USERNAME, CONF_PASSWORD
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import Config, HomeAssistant

"""The EPB Energy integration."""

DOMAIN = DOMAIN


async def async_setup(hass: HomeAssistant, config: Config):
    """Set up this integration using YAML is not supported."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up this integration using UI."""
    return True
