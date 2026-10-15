from datetime import date, datetime

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.helpers import label_registry

from ..constants import *


class CleanupIgnoreLabelsService:
    def __init__(self, hass):
        self._hass = hass

    def register(self):
        self._hass.services.async_register(
            DOMAIN,
            'cleanup_ignore_labels',
            self.handle,
            schema=vol.Schema({
                vol.Optional(FIELD_BEFORE): cv.date,
            }),
        )

    async def handle(self, request):
        beforeDate = request.data.get(FIELD_BEFORE) or date.today()
        labelRegistry = label_registry.async_get(self._hass)

        for entry in list(labelRegistry.labels.values()):
            shouldRemoveLabel = False

            if not entry.name.startswith(LABEL_IGNORE_UNTIL_PREFIX):
                continue

            try:
                entry_date = datetime.strptime(entry.name[len(LABEL_IGNORE_UNTIL_PREFIX):], DATE_FORMAT).date()

                if entry_date < beforeDate:
                    shouldRemoveLabel = True
            except Exception:
                shouldRemoveLabel = True

            if shouldRemoveLabel:
                labelRegistry.async_delete(entry.label_id)
