# epb_energy/config_flow.py

"""Config flow for EPB Energy integration."""
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant import config_entries, exceptions
import aiohttp
from voluptuous import Any

from .const import DOMAIN


async def validate_input(hass: HomeAssistant, data: dict) -> dict[str, Any]:
    """Validate the user input allows us to connect.

    Data has the keys from DATA_SCHEMA with values provided by the user.
    """
    # Validate the data can be used to set up a connection.
    login_url = "https://api.epb.com/web/api/v1/login/"
    async with aiohttp.ClientSession() as session:
        async with session.post(
                login_url,
                json={"username": data["username"], "password": data["password"], "grant_type": "PASSWORD"},
        ) as response:
            if not (response.status >= 200 and response.status < 300):
                raise InvalidAuth

    # If your PyPI package is not built with async, pass your methods
    # to the executor:
    # await hass.async_add_executor_job(
    #     your_validate_func, data["username"], data["password"]
    # )

    # If you cannot connect:
    # throw CannotConnect
    # If the authentication is wrong:
    # InvalidAuth

    # Return info that you want to store in the config entry.
    # "Title" is what is displayed to the user for this hub device
    # It is stored internally in HA as part of the device config.
    # See `async_step_user` below for how this is used
    return {"title": data["host"]}


class EPBEnergyFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle an EPB Energy config flow."""

    errors = {}

    async def async_step_user(self, user_input=None):
        """Handle a flow initiated by the user."""

        errors = {}
        if user_input is None:
            return await self._show_config_form()
        else:
            try:
                info = await validate_input(self.hass, user_input)

                return self.async_create_entry(title=info["title"], data=user_input)
            except InvalidAuth:
                errors["base"] = "invalid_auth"

        # Validate and store user input

        return self.async_create_entry(
            title=user_input["username"],
            data={
                "username": user_input["username"],
                "password": user_input["password"],
            },
            errors=errors
        )

    async def _show_config_form(self, errors=None):
        """Show the configuration form to the user."""
        # Implement the configuration form
        # Use vol.Schema to define the form fields and validation

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required("username"): str,
                    vol.Required("password"): str,
                }
            ),
            errors=errors or {},
        )
