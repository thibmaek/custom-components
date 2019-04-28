# motionEye on motion

Simple bash script to publish an MQTT or HTTP event when motion has been detected by motionEye.

## Requirements

- curl
- mosquitto_pub

## Setup

Edit the script with your editor and fill in the required credentials for:

- HTTP events: `HOSTNAME, ACCESS_TOKEN, BINARY_SENSOR`
  - `ACCESS_TOKEN` should be a Home Assistant long-lived access token.
  - `HOSTNAME` should be the mdns name /ip of your Home Assistant instance
- MQTT events: `HOSTNAME, MQTT_USER, MQTT_PASS`
  - `HOSTNAME` should be the mdns name of your Home Assistant instance
  - You can optionally configure the topic and MQTT port.

## Install

1. Clone this script somewhere
2. In motionEye, under __Motion Notifications__ enable __Run A Command__
3. Configure the start and end command to have reliable results.

| Function Call | Argument | Example | Extra
|---|---|---|---
| trigger_ifttt_webhook | $event name | `bash motioneye_on_motion.sh trigger_ifttt_webhook motion_detected` | Defaults to `motion_detected` if no arg provided
| motion_detected_mqtt, motion_ended_mqtt | Camera id | `bash motioneye_on_motion.sh motion_detected_mqtt garage-cam` | With the camera id given the topic will look like: `homeassistant/binary-sensor/motion-detected/garage-cam`
| motion_detected_http, motion_ended_http | Binary Sensor entity | `bash motioneye_on_motion.sh motion_ended_http binary_sensor.motion_detected` | The binary sensor will default to `binary_sensor.motion_detected` or whatever is defined as `BINARY_SENSOR` in the script.
