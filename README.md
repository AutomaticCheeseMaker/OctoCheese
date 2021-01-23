# OctoPrint-OctoCheese

OctoPrint Plugin that controls a cheese making device running Marlin. Provides several new Gcode commands for stirring, wait for x seconds, wait for x temperature and sending notifications.

## Setup

1. Install via the bundled [Plugin Manager](https://github.com/foosel/OctoPrint/wiki/Plugin:-Plugin-Manager)
or manually using this URL:

  `https://github.com/thomaspreece/OctoCheese/archive/master.zip`
`
2. Install MQTT Plugin (Only required for MQTT messages)

3. Restart OctoPrint

## Configuration

Configure via the OctoPrint settings UI. By default the plugin assumes:
- The X Axis is the stirring stepper 
- The water heater is plugged into the "Bed" heater port
- The water heater temperature is plugged into the "Bed" temperature port 
- The Milk temperature is plugged into the "Hotend" temperature port

## Gcode

- M950 S0                   - Turn stirrer off
- M950 S1                   - Turn stirrer on
- M951 S100                 - Pause octoprint print job for 100 seconds
- M951                      - Cancel previously issued wait (from OctoPrint Terminal only)
- M140 S38                  - Heat "bed" (water bath) to 38C
- M952 B38                  - Pause octoprint print job until "bed" temperature (water temperature) is over 38C for at least 9s
- M952 H38                  - Pause octoprint print job until "hotend" temperature (milk temperature) is over 38C for at least 9s
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
