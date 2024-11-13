from pathlib import Path

import pytest

import nonebot
import nonebot.adapters

nonebot.adapters.__path__.append(  # type: ignore
    str((Path(__file__).parent.parent / "nonebot" / "adapters").resolve())
)


def pytest_configure(config: pytest.Config) -> None:
    pass


@pytest.fixture(scope="session", autouse=True)
def _init_adapter(nonebug_init: None):
    from nonebot.adapters.telegram import Adapter

    driver = nonebot.get_driver()
    driver.register_adapter(Adapter)
