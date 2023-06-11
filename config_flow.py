# epb_energy/config_flow.py

"""Config flow for EPB Energy integration."""
import voluptuous as vol
from homeassistant import config_entries

DOMAIN = "epb_energy"


class EPBEnergyFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle an EPB Energy config flow."""

    async def async_step_user(self, user_input=None):
        """Handle a flow initiated by the user."""
        if user_input is None:
            return self._show_config_form()

        # Validate and store user input

        return self.async_create_entry(
            title=user_input["username"],
            data={
                "username": user_input["username"],
                "password": user_input["password"],
            },
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
