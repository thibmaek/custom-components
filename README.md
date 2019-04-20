# Custom Components

[![](https://img.shields.io/badge/check-my%20roadmap-5362F5.svg)](https://www.notion.so/thibmaek/35f17ce6deae47918e4e970d05a9dc2c?v=61cc36c732c64a318ce51ed4369b74ab)

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
