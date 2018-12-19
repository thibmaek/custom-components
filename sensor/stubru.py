"""
"""

import logging

import requests
import voluptuous as vol

import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import ATTR_ATTRIBUTION, CONF_NAME
from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)

DEFAULT_NAME = 'Studio Brussel'
DEFAULT_ICON = 'mdi:radio'

CONF_CHANNEL = 41

RESOURCE_URL = "https://services.vrt.be/epg/onair"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_CHANNEL): cv.positive_int,
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
})


def setup_platform(hass, config, add_entities, discovery_info=None):
    """"""
    channel_code = config[CONF_CHANNEL]
    name = config[CONF_NAME]

    add_entities([StuBruSensor(channel_code, name)], True)


class StuBruSensor(Entity):
    """"""

    def __init__(self, channel_code, name):
        """Initialize the Velo sensor."""
        self._name = name
        self._channel_code = channel_code
        self._state = None
        self._attrs = {}

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def icon(self):
        """Return the icon to use in the frontend, if any."""
        return DEFAULT_ICON

    @property
    def device_state_attributes(self):
        """Return the state attributes of the sensor."""
        if self._state is None or self._attrs is None:
            return

        return {
            'start_time': self._attrs['curr_program']['startTime'],
            'end_time': self._attrs['curr_program']['endTime'],
            'presenters': self._attrs['curr_program']['presenters'][0]['name'],
            'episode_title': self._attrs['curr_program']['episodeTitle'],
            'episode': self._attrs['curr_program']['episodeNumber'],
            'season_title': self._attrs['curr_program']['seasonTitle'],
            'season': self._attrs['curr_program']['seasonNumber'],
            'previous_program': self._attrs['prev_program']['title'],
            'next_program': self._attrs['next_program']['title'],
            ATTR_ATTRIBUTION: "Data provided by https://services.vrt.be/epg",
        }

    @property
    def state(self):
        """Return the state of the device."""
        return self._state

    def make_request(self):
        """Send a GET request to the VRT endpoint"""
        params = {'channel_code': self._channel_code}
        headers = {'accept': 'application/vnd.epg.vrt.be.onairs_1.2+json'}

        request = requests.Request("GET", RESOURCE_URL,
                                   headers=headers, params=params).prepare()
        try:
            with requests.Session() as sess:
                response = sess.send(request, timeout=10)

            return response.json()['onairs'][0]
        except requests.exceptions.RequestException as ex:
            _LOGGER.error("Error fetching data: %s from %s failed with %s",
                          request, request.url, ex)

    def update(self):
        """Set the state to the available amount of bikes as a number"""
        try:
            data = self.make_request()
            curr_program = data['now']
            if curr_program is None:
                return

            self._attrs = {
                'prev_program': data['previous'],
                'curr_program': curr_program,
                'next_program': data['next'],
            }
            self._state = curr_program['title']
        except KeyError:
            self._state = None
