"""
"""

import logging

from datetime import timedelta
import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_NAME, ATTR_ATTRIBUTION
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity
from homeassistant.util import Throttle

_LOGGER = logging.getLogger(__name__)

DEFAULT_ICON = 'mdi:newspaper'
CONF_UPDATE_INTERVAL = 'update_interval'

REQUIREMENTS = ['xmltodict==0.11.0', 'requests_xml==0.2.3']

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_UPDATE_INTERVAL, default=timedelta(seconds=180)): (
        vol.All(cv.time_period, cv.positive_timedelta)),
})


def setup_platform(hass, config, add_entities, discovery_info=None):
    """"""
    from requests_xml import XMLSession
    session = XMLSession()

    interval = config.get(CONF_UPDATE_INTERVAL)

    add_entities([
        VRTNWSFeedSensor(session, interval),
        VRTNWSBreakingSensor(session)
    ], True)


class VRTNWSBreakingSensor(Entity):
    """"""

    def __init__(self, session):
        """"""
        self._session = session
        self._state = None
        self._data = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return "VRT NWS (Breaking)"

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
        if self._data is None:
            return {
                ATTR_ATTRIBUTION: "https://www.vrt.be/vrtnws/nl/",
            }
        else:
            return {
                "Details": self._data['summary'].get('#text'),
                ATTR_ATTRIBUTION: "https://www.vrt.be/vrtnws/nl/",
            }

    @property
    def state(self):
        """Return the state of the device."""
        return self._state

    def update(self):
        """Set the state to the available amount of bikes as a number"""
        import xmltodict

        response = self._session.get('https://www.vrt.be/vrtnws/nl.rss.breaking.xml')
        entries = xmltodict.parse(response.xml.xml).get('feed').get('entry')

        if entries is None:
            self._state = "No breaking news"
            self._data = None
        else:
            self._data = entries[0]
            self._state = entries[0]["summary"].get("#text")


class VRTNWSFeedSensor(Entity):
    """"""

    def __init__(self, session, interval):
        """"""
        self._session = session
        self._state = None
        self._data = None
        self.update = Throttle(interval)(self._update)

    @property
    def name(self):
        """Return the name of the sensor."""
        return "VRT NWS"

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
        if self._data is None:
            return {
                ATTR_ATTRIBUTION: "https://www.vrt.be/vrtnws/nl/",
            }
        else:
            return {
                "Details": self._data['summary'].get('#text'),
                "Last updated": self._data['updated'],
                "Link": self._data['id'],
                "Picture": self.get_picture_url(self._data['link']),
                "Published": self._data['published'],
                "Tag": self._data['vrtns:nstag'].get('#text'),
                ATTR_ATTRIBUTION: "https://www.vrt.be/vrtnws/nl/",
            }

    @property
    def state(self):
        """Return the state of the device."""
        return self._state

    def get_picture_url(self, links_dict):
        """Get the entry's picture from the links dictionary."""
        pic = list(filter(lambda x: (x['@type'] == "image/jpeg"), links_dict))
        return pic[0].get("@href")


    def _update(self):
        """Set the state to the available amount of bikes as a number"""
        import xmltodict

        response = self._session.get('https://www.vrt.be/vrtnws/nl.rss.articles.xml')
        entries = xmltodict.parse(response.xml.xml).get('feed').get('entry')

        title = entries[0]["title"].get("#text")

        # Don't include this in the state because it appears too often and is not interesting
        if title == "LIVE : Het Journaal 1":
            return
        else:
            self._data = entries[0]
            self._state = title

