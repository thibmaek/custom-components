# VRT NWS

Displays the latest headline and breaking news item (if any) from [VRT NWS](https://www.vrt.be/vrtnws/nl/).
This will create two seperate sensors: `sensor.vrt_nws, sensor.vrt_nws_breaking`

![screenshot_vrt_nws](https://i.imgur.com/KyM04GO.png)

## Configuration

```yaml
sensor:
  - platform: vrtnws
    # Optional: set a scan interval
    update_interval: 180
```

### Troubleshooting

If you are not running Hass.io, [you might need to install `libxml2` and `libxml2-dev`](https://github.com/thibmaek/custom-components/issues/8) via your package manager like apt, or in your container.
