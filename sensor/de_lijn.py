"""
Shows the available amount of public city bikes for Velo Antwerpen.
For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/sensor.de_lijn/
"""

import logging

import requests
import voluptuous as vol

import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import ATTR_ATTRIBUTION, CONF_NAME
from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)

DEFAULT_NAME = 'De Lijn'
DEFAULT_ICON = 'mdi:bus'

CONF_LATITUDE = 'latitude'
CONF_LONGITUDE = 'longitude'

REQUIREMENTS = ['pytheline==0.0.4']

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_LATITUDE, default=0): cv.string,
    vol.Optional(CONF_LONGITUDE, default=0): cv.string,
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
})


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the Velo sensor."""
    from pytheline import deLijn
    api_client = deLijn()

    name = config.get(CONF_NAME)
    lat = config.get(CONF_LATITUDE)
    lon = config.get(CONF_LONGITUDE)

    add_entities([DeLijnSensor(name, lat, lon, api_client)], True)


class DeLijnSensor(Entity):
    """Get the available amount of bikes and set the selected station as attributes"""

    def __init__(self, name, lat, lon, api_client):
        """Initialize the NMBS sensor."""
        self._name = name
        self._lat = lat
        self._lon = lon
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
            ATTR_ATTRIBUTION: "",
        }

    @property
    def state(self):
        """Return the state of the device."""
        return self._state

    def update(self):
        """Set the state to the available amount of bikes as a number"""
        # coords = self._api_client.convert_location(self._lat, self._lon)
        connections = self._api_client.haltes_vertrekken(201549, 3)
        _LOGGER.error(connections)
        self._state = None
