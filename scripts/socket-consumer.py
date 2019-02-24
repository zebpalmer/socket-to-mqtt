#!/bin/usr/env python3
import os
import sys
import socket
import uuid
import logging
import paho.mqtt.client as paho


log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(stream=sys.stdout, level=os.environ.get("LOG_LEVEL", "INFO"), format=log_format)


def get_config():
    cfg = {}
    required = ["SOCKET_HOST", "SOCKET_PORT", "MQTT_HOST", "MQTT_PORT", "MQTT_TOPIC"]
    for env in required:
        if os.environ.get(env) is None:
            raise Exception(f"Missing Required config, env var: {env}")
        else:
            cfg[env] = os.environ[env]

    if not os.environ.get("MQTT_CLIENT_NAME"):
        cname = str(uuid.uuid4())
    else:
        cname = os.environ["MQTT_CLIENT_NAME"]
    cfg["MQTT_CLIENT_NAME"]: cname
    cfg["MQTT_TLS"]: os.environ.get("MQTT_TLS", False)
    cfg["LOG_LEVEL"]: os.environ.get("LOG_LEVEL", "INFO")
    return cfg


def get_mqtt(cfg):
    mqtt = paho.Client(cfg["MQTT_CLIENT_NAME"])
    if cfg['MQTT_TLS']:
        mqtt.tls_set()
    mqtt.connect(cfg["MQTT_HOST"], cfg["MQTT_PORT"])
    return mqtt


def get_sock(cfg):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_target = (cfg["SOCKET_HOST"], cfg["SOCKET_PORT"])
    sock.connect(sock_target)
    return sock.makefile()


def run(cfg):
    count = 0
    mqtt = get_mqtt(cfg)
    for x in get_sock(cfg):
        res, mid = mqtt.publish(cfg["MQTT_TOPIC"], x.strip())
        logging.debug(f"Res {res} mid {mid}")
        if res == 0:
            count += 1
            if count % 1000 == 0:  # log msg every 1000 messages published
                logging.info(f"Msg publish count: {count}")
        else:
            logging.warning(f"MSG Result status: {res} for message id {mid}")


if __name__ == "__main__":
    logging.info("Starting Consumer")
    try:
        cfg = get_config()
        logging.debug(f"Config: {cfg}")
        run(cfg)
    except Exception as e:
        logging.critical(f"EXCEPTION: {e}")
    finally:
        logging.warning(f"Exiting...")