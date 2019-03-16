# Telemeter

Displays information about your Telenet interner usage (Telemeter).

![screenshot_telemeter](https://i.imgur.com/pFo1ie3.png)

## Configuration

This sensor requires you to provide a cookie to authenticate with OCAPI (Telenet's API).
You can obtain a cookie by going to [Mijn Telenet](https://mijn.telenet.be) and copying that page's cookie.

The cookie can be copied by opening your browser's console and entering `document.cookie` or by inspecting __Doc__ in the Network tab and copying the cookie.

The sensor will poll the OCAPI every 10 minutes about your usage.

```yaml
sensor:
  # For optional configuration see the section below.
  - platform: telemeter
    name: "Telemeter"
    cookie: 'AMCV_...'
```

### Optional configuration

__include_offpeak: bool (false)__
Offpeak usage does not count towards the bandwidth volume cap Telenet sets. By default it won't be shown or included.
If you want to display the offpeak usage set this option to true:

```yaml
include_offpeak: true
```

The total usage will be calculated as `peak_usage + offpeak_usage`. If this option is not enabled the offpeak usage will still be added as an attribute to the sensor.
