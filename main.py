from dotenv import load_dotenv

load_dotenv()

import signal
import threading

from src.Presentation.mqtt_listener import MqttListener
from src.Utils.logger import setup_logger

shutdown_event = threading.Event()


def main():
    logger = setup_logger("Main")
    logger.info("Starting TFG Server...")

    mqtt_listener = MqttListener()
    mqtt_listener.start()

    def _handle_signal(signum, frame):
        logger.info(f"Received signal {signum}, shutting down...")
        try:
            mqtt_listener.stop()
        finally:
            shutdown_event.set()

    signal.signal(signal.SIGINT, _handle_signal)
    signal.signal(signal.SIGTERM, _handle_signal)

    try:
        shutdown_event.wait()
    except KeyboardInterrupt:
        _handle_signal(signal.SIGINT, None)


if __name__ == "__main__":
    main()
