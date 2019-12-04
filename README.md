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

- M950 S0   - Turn stirrer off or on
- M950 S1   - Turn stirrer on
- M951 S100 - Pause octoprint print job for 100 seconds
- M951      - Cancel previously issued wait (from OctoPrint Terminal only)
- M952 B38  - Pause octoprint print job until "bed" temperature is 38C
- M952 H38  - Pause octoprint print job until "hotend" temperature is 38C
- M952      - Cancel previously issued temperature wait (from OctoPrint Terminal only)
