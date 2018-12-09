"""
Shows the amount of usage in your Telenet Telemeter.
"""
import logging

import requests
import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_NAME, ATTR_ATTRIBUTION
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity
import homeassistant.util.dt as dt_util

_LOGGER = logging.getLogger(__name__)

RESOURCE_URL = 'https://api.prd.telenet.be/ocapi/public/?p=internetusage'

DEFAULT_NAME = 'Telemeter'
DEFAULT_ICON = 'mdi:train' # TODO: icon

# This is a cookie obtained from the mijn.telenet.be webportal
CONF_COOKIE = 'credential'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_COOKIE): cv.string,
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
})


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the Velo sensor."""

    name = config.get(CONF_NAME)
    credential = config[CONF_COOKIE]

    add_entities([TelemeterSensor(name, credential)], True)


class TelemeterSensor(Entity):
    def __init__(self, name, credential):
        self._name = name
        self._credential = credential
        self._state = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def icon(self):
        """Return the icon to use in the frontend, if any."""
        return '' # TODO: correct icon

    @property
    def state(self):
        """Return the state of the device."""
        return self._state

    @property
    def device_state_attributes(self):
        # TODO: return correct attrs
        if self._state is None or self._attrs is None:
            return None

        return {}

    def make_request(self):
        """Perform the API request to OCAPI (Telenet)"""
        request = requests.Request("GET", RESOURCE_URL).prepare()
        try:
            with requests.Session() as sess:
                response = sess.send(request, timeout=10)

            telemeter_usage = response.json()
            return telemeter_usage['internetusage'][0]
        except requests.exceptions.RequestException as ex:
            _LOGGER.error("Error fetching data: %s from %s failed with %s",
                          request, request.url, ex)

    def update(self):
        usage_current_month = self.make_request()['availableperiods'][0]

        # TODO: return correct state
        self._state = None
