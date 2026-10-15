import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.helpers import label_registry

from ..constants import *


class DeleteLabelService:
    def __init__(self, hass):
        self._hass = hass

    def register(self):
        self._hass.services.async_register(
            DOMAIN,
            'delete_label',
            self.handle,
            schema=vol.Schema({
                vol.Required(FIELD_NAME): cv.string,
            }),
        )

    async def handle(self, request):
        labelName = request.data[FIELD_NAME]
        labelRegistry = label_registry.async_get(self._hass)

        for entry in list(labelRegistry.labels.values()):
            if entry.name == labelName:
                labelRegistry.async_delete(entry.label_id)
                break
