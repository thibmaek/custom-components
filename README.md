# Custom Components

Collection of custom componets to use with Home Assistant. This repo mainly consists of useful sensor which use the Python `requests` package to fetch data from an HTTP endpoint. Since [protocol handling is not allowed](https://github.com/home-assistant/home-assistant/pull/18276#discussion_r231319479) in Home Assistant core, those components end up here.

## Custom updater

Each component is isolated in its own folder with a README and CHANGELOG. There is provided support for [custom_updater](https://github.com/custom-components/custom_updater) for every component which has a released status.
