"""
Shows the available amount of public city bikes for Velo Antwerpen.
For more details about this platform, please refer to the documentation at

https://github.com/thibmaek/custom-components/sensor/velo_antwerpen
"""

import logging

import requests
import voluptuous as vol

import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import (ATTR_ATTRIBUTION, CONF_NAME)
from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)

__version__ = '1.1.0'

DEFAULT_NAME = 'Velo'

CONF_STATION_ID = 'station_id'

RESOURCE_URL = "https://www.velo-antwerpen.be/availability_map/getJsonObject"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_STATION_ID): cv.string,
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
})


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the Velo sensor."""
    name = config[CONF_NAME]
    station_id = config.get(CONF_STATION_ID)

    add_entities([VeloSensor(name, station_id)], True)


class VeloSensor(Entity):
    """Get the available amount of bikes and set the station attributes."""

    def __init__(self, name, station_id):
        """Initialize the Velo sensor."""
        self._name = name
        self._station_id = station_id
        self._attrs = {}
        self._station_data = {}
        self._state = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def unit_of_measurement(self):
        """Return the unit the value is expressed in."""
        return 'bikes'

    @property
    def icon(self):
        """Return the icon to use in the frontend, if any."""
        return 'mdi:bike'

    @property
    def state(self):
        """Return the state of the device."""
        return self._state

    @property
    def device_state_attributes(self):
        """Return the state attributes of the sensor."""
        if self._state is None or self._station_data is None:
            return {}

        return {
            'available_slots': int(self._station_data['slots']),
            'latitude': self._station_data['lat'],
            'longitude': self._station_data['long'],
            "station_address": self._station_data["address"],
            "station_id": int(self._station_id),
            "station_name": self._station_data['name'],
            "station_opened": self._station_data['status'] == 'OPN',
            ATTR_ATTRIBUTION: "https://www.velo-antwerpen.be/",
        }

    def make_request(self):
        """Perform the API request to the Velo Antwerpen API"""
        request = requests.Request("GET", RESOURCE_URL).prepare()
        try:
            with requests.Session() as sess:
                response = sess.send(request, timeout=10)

            station_data = response.json()
            result = list(
                filter(lambda x: (x['id'] == self._station_id), station_data))
            return result[0]
        except requests.exceptions.RequestException as ex:
            _LOGGER.error("Error fetching data: %s from %s failed with %s",
                          request, request.url, ex)

    def update(self):
        """Set the state to the available amount of bikes as a number"""
        try:
            station_data = self.make_request()
            self._station_data = station_data
            self._state = int(station_data["bikes"])
        except KeyError:
            self._state = None