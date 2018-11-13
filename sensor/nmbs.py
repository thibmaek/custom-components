"""
Shows the available amount of public city bikes for Velo Antwerpen.
For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/sensor.nmbs/
"""

import logging

import requests
import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_NAME, ATTR_ATTRIBUTION
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)

DEFAULT_NAME = 'NMBS'
DEFAULT_ICON = 'mdi:train'

CONF_STATION_FROM = 'station_from'
CONF_STATION_TO = 'station_to'

REQUIREMENTS = ['pyrail==0.0.3']

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_STATION_FROM): cv.string,
    vol.Required(CONF_STATION_TO): cv.string,
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
})


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the Velo sensor."""
    from pyrail import iRail
    api_client = iRail()

    name = config.get(CONF_NAME)
    station_from = config.get(CONF_STATION_FROM)
    station_to = config.get(CONF_STATION_TO)

    add_entities([NMBSSensor(name, station_from, station_to, api_client)], True)


class NMBSSensor(Entity):
    """Get the available amount of bikes and set the selected station as attributes"""

    def __init__(self, name, station_from, station_to, api_client):
        """Initialize the NMBS sensor."""
        self._name = name
        self._station_from = station_from
        self._station_to = station_to
        self._api_client = api_client
        self._state = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def unit_of_measurement(self):
        """Return the unit the value is expressed in."""
        return ""

    @property
    def icon(self):
        """Return the icon to use in the frontend, if any."""
        return DEFAULT_ICON

    @property
    def device_state_attributes(self):
        """Return the state attributes of the sensor."""
        return {
            ATTR_ATTRIBUTION: "https://api.irail.be/",
        }

    @property
    def state(self):
        """Return the state of the device."""
        return self._state

    def update(self):
        """Set the state to the available amount of bikes as a number"""
        connections = self._api_client.get_connections(self._station_from, self._station_to)
        next_connection = connections["connection"][0]
        self._state = "In 4 minutes, direction {0}".format(next_connection["departure"]["direction"]["name"])
