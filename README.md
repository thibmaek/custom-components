# Custom Components

Collection of custom componets to use with Home Assistant. This repo mainly consists of useful sensor which use the Python `requests` package to fetch data from an HTTP endpoint. Since [protocol handling is not allowed](https://github.com/home-assistant/home-assistant/pull/18276#discussion_r231319479) in Home Assistant core, those components end up here.

## Custom updater

Each component is isolated in its own folder with a README and CHANGELOG. There is provided support for [custom_updater](https://github.com/custom-components/custom_updater) for every component which has a released status.

## Adding to Home Assistant

1. Create (if not already created) a folder in your `/config` directory called `custom_components`
2. Copy `<custom_component>/sensor.py` from this repo to the same location
3. Restart Home Assistant

e.g:

```plaintext
https://github.com/thibmaek/custom-components/telemeter/sensor.py
  --> /config/custom_components/telemeter/sensor.py
```
