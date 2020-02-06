# OctoPrint-OctoCheese

OctoPrint Plugin that controls a cheese making device running Marlin. Provides several new Gcode commands for stirring, wait for x seconds, wait for x temperature and sending notifications.

## Setup

1. Install via the bundled [Plugin Manager](https://github.com/foosel/OctoPrint/wiki/Plugin:-Plugin-Manager)
or manually using this URL:

```
https://github.com/thomaspreece/OctoCheese/archive/master.zip
```

1. Restart OctoPrint

## Configuration

Configure via the OctoPrint settings UI.

## Gcode

- M950 S0                   - Turn stirrer off or on
- M950 S1                   - Turn stirrer on
- M951 S100                 - Pause octoprint print job for 100 seconds
- M951                      - Cancel previously issued wait (from OctoPrint Terminal only)
- M952 B38                  - Pause octoprint print job until "bed" temperature is over 38C for at least 9s
- M952 H38                  - Pause octoprint print job until "hotend" temperature is over 38C for at least 9s
- M952                      - Cancel previously issued temperature wait (from OctoPrint Terminal only)
- M953 STRING               - Send STRING to MQTT
- M954 STRING               - Send STRING to MQTT and wait for user
- M954                      - Cancel previously issued wait for user
- M955 S1 RENNET            - Release Rennet
- M955 S0 RENNET            - Unrelease Rennet
- M955 S1 CALCIUM_CHLORIDE  - Release Calcium Chloride
- M955 S0 CALCIUM_CHLORIDE  - Unrelease Calcium Chloride
- M955 S1 ANNATTO           - Release Annatto
- M955 S0 ANNATTO           - Unrelease Annatto
- M955 S1 CULTURE           - Release Culture
- M955 S0 CULTURE           - Unrelease Culture
