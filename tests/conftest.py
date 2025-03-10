import logging
import pytest
import colorlog

from pathlib import Path


def pytest_configure():
    handler = colorlog.StreamHandler()
    handler.setFormatter(
        colorlog.ColoredFormatter(
            "%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            log_colors={
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "bold_red",
            },
        )
    )
    logging.basicConfig(level=logging.INFO, handlers=[handler])


@pytest.fixture(autouse=True)
def setup_logging(caplog):
    caplog.set_level(logging.INFO)


@pytest.fixture(scope="session")
def root_dir():
    return Path(__file__).parent.parent


@pytest.fixture(scope="session")
def data_dir(root_dir):
    return root_dir / "data"
