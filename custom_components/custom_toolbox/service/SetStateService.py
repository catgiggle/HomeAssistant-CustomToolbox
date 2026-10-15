import homeassistant.helpers.config_validation as cv
import voluptuous as vol

from ..constants import *


class SetStateService:
    def __init__(self, hass):
        self._hass = hass

    def register(self):
        self._hass.services.async_register(
            DOMAIN,
            'set_state',
            self.handle,
            schema=vol.Schema({
                vol.Required(FIELD_ENTITY_ID): cv.entity_id,
                vol.Optional(FIELD_STATE): cv.string,
                vol.Optional(FIELD_ATTRIBUTES): dict,
            }),
        )

    async def handle(self, request):
        entityId = request.data[FIELD_ENTITY_ID]
        stateObject = self._hass.states.get(entityId)
        entityState = request.data.get(FIELD_STATE, stateObject.state if stateObject else None)
        entityAttributes = stateObject.attributes.copy() if stateObject else {}
        entityAttributes.update(request.data.get(FIELD_ATTRIBUTES, {}))

        self._hass.states.async_set(
            entityId,
            entityState,
            entityAttributes
        )
