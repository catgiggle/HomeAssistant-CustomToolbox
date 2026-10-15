# Custom Toolbox

This Home Assistant integration provides essential utility services for entity state manipulation and label maintenance.

It enables setting custom entity states and attributes directly in the state machine, as well as managing and
automatically cleaning up temporary labels in the Home Assistant label registry.

It is especially useful when you want to:

- Override entity states or attributes dynamically in automations, scripts, or testing scenarios without creating dummy
  helper entities.
- Inject simulated or temporary sensor values to test automation behavior.
- Clean up expired temporary labels (`ignore-until-YYYY_MM_DD`) automatically on a recurring schedule.
- Remove obsolete labels programmatically from the Home Assistant label registry.

## Installation

This integration is installed via **HACS**:

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=catgiggle&repository=HomeAssistant-CustomToolbox)

1. Click the button above to open the repository in HACS.
2. Click **Download** to download the integration.
3. Restart Home Assistant.

**Note:** Alternatively, you can add `https://github.com/catgiggle/HomeAssistant-CustomToolbox` as a custom repository
under **HACS → Integrations**.

## Configuration

Custom Toolbox is configured directly via the Home Assistant user interface:

1. Navigate to **Settings → Devices & services**.
2. Click **Add Integration** in the bottom right corner.
3. Search for **Custom Toolbox** and follow the prompt.

## Features

- Direct state and attributes modification for any entity via `set_state`
- Support for updating entity attributes via nested `attributes` dictionary
- Automated cleanup of date-stamped ignore labels (`ignore-until-YYYY_MM_DD`)
- Programmatic deletion of labels by name or identifier from the Home Assistant label registry
- Lightweight integration with zero external dependencies

## Services

This integration provides the following services:

### `custom_toolbox.set_state`

Sets or overrides the state and attributes of any entity directly in the Home Assistant state machine.

| Field        | Description                                                   |
|--------------|---------------------------------------------------------------|
| `entity_id`  | Entity ID whose state and attributes will be modified         |
| `state`      | New state value (optional, retains existing state if omitted) |
| `attributes` | Dictionary of attributes to set or update (optional)          |

### `custom_toolbox.delete_label`

Removes a specific label from the Home Assistant label registry by name or ID.

| Field  | Description                       |
|--------|-----------------------------------|
| `name` | Name or ID of the label to delete |

### `custom_toolbox.cleanup_ignore_labels`

Removes all labels matching `ignore-until-YYYY_MM_DD` that are older than the given date or malformed.

| Field    | Description                                                                   |
|----------|-------------------------------------------------------------------------------|
| `before` | Date threshold formatted as `YYYY-MM-DD` (optional, defaults to current date) |

## Usage Examples

### Setting Entity State and Nested Attributes

```yaml
action: custom_toolbox.set_state
data:
  entity_id: sensor.living_room_temperature
  state: "21.5"
  attributes:
    unit_of_measurement: "°C"
    device_class: temperature
    friendly_name: "Living Room Temperature"
    battery: 95
```

### Updating Attributes Without Changing State

```yaml
action: custom_toolbox.set_state
data:
  entity_id: binary_sensor.guest_mode
  attributes:
    reason: "Scheduled party"
    expires_in_hours: 4
```

### Cleaning Up Expired Ignore Labels (e.g. Daily Automation)

```yaml
automation:
  - alias: "Daily Cleanup of Expired Ignore Labels"
    trigger:
      - platform: time
        at: "03:00:00"
    action:
      - action: custom_toolbox.cleanup_ignore_labels
```

### Deleting a Specific Label

```yaml
action: custom_toolbox.delete_label
data:
  name: "ignore-until-2026_10_15"
```

## Notes

- Changes made by `set_state` are written directly to Home Assistant's runtime state machine. If the target entity
  belongs to an active physical integration or polling sensor, its state may be overwritten when that integration next
  updates.
- The `cleanup_ignore_labels` service is designed for temporary suppression workflows using label formats like
  `ignore-until-2026_10_15`. Labels with dates prior to the threshold (or unparseable suffixes) are safely purged from
  the registry.