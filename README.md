# Custom Components

Collection of custom componets to use with Home Assistant.

## sensor.velo_antwerpen

Shows the amount of free bikes in a favourite Velo Antwerpen bike station.

![screenshot_velo_antwerpen](https://user-images.githubusercontent.com/6213695/48092180-3fa40980-e20c-11e8-8049-e34c0ed802c2.png)

```yaml
sensor:
  - platform: velo_antwerpen
    station_id: '067'
```

## sensor.vrt_nws

Displays the latest headline and breaking news item (if any) from [VRT NWS](https://www.vrt.be/vrtnws/nl/).
This will create two seperate sensors: `sensor.vrt_nws, sensor.vrt_nws_breaking`

> If you are not running Hass.io, [you might need to install `libxml2` and `libxml2-dev`](https://github.com/thibmaek/custom-components/issues/8) via your package manager like apt, or in your container.

![screenshot_vrt_nws](https://i.imgur.com/KyM04GO.png)

```yaml
sensor:
  - platform: vrtnws
    # Optional: set a scan interval
    update_interval: 180
```
