from homeassistant.helpers import config_validation as cv

from .constants import *
from .service.CleanupIgnoreLabelsService import CleanupIgnoreLabelsService
from .service.DeleteLabelService import DeleteLabelService
from .service.SetStateService import SetStateService

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)


async def async_setup(hass, _config):
    hass.data.setdefault(DOMAIN, {})

    CleanupIgnoreLabelsService(hass).register()
    DeleteLabelService(hass).register()
    SetStateService(hass).register()

    return True


async def async_setup_entry(hass, _entry):
    return True


async def async_unload_entry(hass, _entry):
    return True
