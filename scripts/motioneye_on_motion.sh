#!/usr/bin/env bash
# 
# Simple script to be used with motionEye's motion notifications
# which will trigger a binary sensor to on or off over MQTT or HTTP.
# e.g. bash /home/pi/motioneye_on_motion.sh motion_ended_http
# 

# Configure this to refer to your Home Assistant instance
HOSTNAME="hassio.local"
HOME_ASSISTANT_URL="http://${HOSTNAME}:8123/api"
ACCESS_TOKEN=""
BINARY_SENSOR="binary_sensor.motion_detected"

# Configure this if you will use MQTT for communicating
MQTT_USER=""
MQTT_PASS=""
MQTT_TOPIC="homeassistant/binary-sensor/motion-detected"
MQTT_PORT=1883

function check_reqs_http() {
  if ! command -v curl > /dev/null; then
    echo "You don't have curl installed which is required to run this script"
    exit 1
  fi
}

function check_reqs_mqtt() {
  if ! command -v mosquitto_pub > /dev/null; then
    echo "You don't have mosquitto_pub (mosquitto-clients) installed which is required to run this script"
    exit 1
  fi
}

function motion_detected_mqtt() {
  check_reqs_mqtt
  mosquitto_pub -h $HOSTNAME -p "$MQTT_PORT" -u "$MQTT_USER" -P "$MQTT_PASS" -t "$MQTT_TOPIC" -m "ON"
}

function motion_ended_mqtt() {
  check_reqs_mqtt
  mosquitto_pub -h $HOSTNAME -p "$MQTT_PORT" -u "$MQTT_USER" -P "$MQTT_PASS" -t "$MQTT_TOPIC" -m "OFF"
}

function motion_detected_http() {
  check_reqs_http
  curl -X POST -H "x-ha-access:$ACCESS_TOKEN" -H "Content-Type: application/json" \
    -d '{"state": "on"}' "$HOME_ASSISTANT_URL/states/$BINARY_SENSOR"
}

function motion_ended_http() {
  check_reqs_http
  curl -X POST -H "x-ha-access:$ACCESS_TOKEN" -H "Content-Type: application/json" \
    -d '{"state": "off"}' "$HOME_ASSISTANT_URL/states/$BINARY_SENSOR"
}

function trigger_ifttt_webhook() {
  check_reqs_http
  local IFTTT_TOKEN=""
  local EVENT_IDENTIFIER="motion_detected"
  curl "https://maker.ifttt.com/trigger/${EVENT_IDENTIFIER}/with/key/${IFTTT_TOKEN}"
}

"$@"
