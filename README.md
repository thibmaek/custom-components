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
