import json
import logging
import os
import paho.mqtt.client as mqtt
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, Any, Callable
from dotenv import load_dotenv
from src.utils.logger import setup_logger

load_dotenv()

class MqttListener:
    def __init__(self):
        self._logger = setup_logger("MqttListener")

        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=os.getenv("MQTT_CLIENT_ID", "serv_mqtt"))
        self.client.username_pw_set(os.getenv("MQTT_USER"), os.getenv("MQTT_PASSWORD"))

        self.executor = ThreadPoolExecutor(max_workers=int(os.getenv("MQTT_MAX_WORKERS", 5)))

        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.client.on_disconnect = self._on_disconnect

        self.topics: Dict[str, Callable[[dict], None]] = {
            "cars/init": self._handle_cars_init,
            "cars/new": self._handle_cars_new,
            "cars/delete": self._handle_cars_delete,
        }

        self.broker_host = os.getenv("MQTT_BROKER_HOST", "localhost")
        self.broker_port = int(os.getenv("MQTT_BROKER_PORT", 1883))

    def start(self):
        """Starts the MQTT loop in a background thread."""
        try:
            self._logger.info(f"Connecting to MQTT Broker at {self.broker_host}:{self.broker_port}...")
            self.client.connect(self.broker_host, self.broker_port, keepalive=60)
            self.client.loop_start() 
            self._logger.info("MQTT Listener started (background loop).")
        except Exception as e:
            self._logger.critical(f"Failed to start MQTT Listener: {e}")
            raise

    def stop(self):
        """Stops the MQTT loop and shuts down the thread pool gracefully."""
        self._logger.info("Stopping MQTT Listener...")
        self.client.loop_stop()
        self.client.disconnect()
        self.executor.shutdown(wait=True)
        self._logger.info("MQTT Listener stopped and thread pool drained.")

    def _on_connect(self, client, userdata, flags, reason_code, properties=None):
        """
        Callback when connected to the broker.
        """
        if reason_code == 0:
            self._logger.info(f"Successfully connected to MQTT Broker.")
            # Subscribe to all topics defined in our routing table
            for topic in self.topics.keys():
                client.subscribe(topic, qos=1) # QoS 1 ensures at least once delivery
                self._logger.info(f"Subscribed to topic: {topic}")
        else:
            self._logger.error(f"Failed to connect. Reason code: {reason_code}")

    def _on_disconnect(self, client, userdata, flags, reason_code, properties=None):
        """
        Callback when disconnected.
        """
        self._logger.warning(f"Disconnected from MQTT Broker. Reason code: {reason_code}")

    def _on_message(self, client, userdata, msg):
        """
        Main Entry Point. 
        CRITICAL: This runs on the Network Thread. 
        We must offload work to the thread pool immediately to avoid blocking heartbeats.
        """
        topic = msg.topic
        try:
            payload = msg.payload.decode()
        except UnicodeDecodeError:
            self._logger.error(f"Received non-UTF8 payload on {topic}")
            return

        if topic in self.topics:
            self._logger.debug(f"Message received on {topic}. Offloading to worker thread.")
            self.executor.submit(self._process_message_task, topic, payload)
        else:
            self._logger.warning(f"No handler defined for topic {topic}. Message ignored.")

    def _process_message_task(self, topic: str, payload: str):
        """
        This runs inside a Worker Thread.
        Safe for JSON parsing and blocking DB calls.
        """
        try:
            data = json.loads(payload)

            handler_func = self.topics[topic]
            handler_func(data)

        except json.JSONDecodeError:
            self._logger.error(f"Malformed JSON received on {topic}. Payload: {payload}")
        except Exception as e:
            self._logger.exception(f"Unexpected error processing message on {topic}")


    # --- HANDLERS (Integration Points with Domain Layer) ---

    def _handle_cars_init(self, data: dict):
        self._logger.info(f"Processing 'cars/init' request.")
        # TODO: Call Domain Service here (e.g., self.car_service.initialize_cars(data))

    def _handle_cars_new(self, data: dict):
        self._logger.info(f"Processing 'cars/new' request for: {data.get('car_id', 'unknown')}")
        # TODO: Call Domain Service here

    def _handle_cars_delete(self, data: dict):
        self._logger.info(f"Processing 'cars/delete' request.")
        # TODO: Call Domain Service here