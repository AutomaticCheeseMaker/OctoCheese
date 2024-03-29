# OctoPrint-OctoCheese

OctoPrint Plugin that controls a cheese making device running Marlin. Provides several new Gcode commands for stirring, wait for x seconds, wait for x temperature and sending notifications to MQTT.

Sending notifications to MQTT allows you to integrate with Home Assistant to get notifications on your mobile or via your home's smart devices.

![OctoCheese and Home Assistant](./images/OctoCheese.png)

The above image shows my current setup with OctoPrint + OctoCheese running on the left browser window and my Home Assistant dashboard on the right browser window.

## Setup

1. Install via the bundled [Plugin Manager](https://github.com/foosel/OctoPrint/wiki/Plugin:-Plugin-Manager)
or manually using this URL:

```
https://github.com/thomaspreece/OctoCheese/archive/main.zip
```

2. Install MQTT Plugin (Only required for MQTT messages & Home Assistant Integration). Once installed you will need to configure the plugin to talk to your MQTT server. You will also want to set the `Base Topic` setting to  `octoPrint/` and enable progress and temperature messages in the MQTT settings as shown in the image below.

![MQTT plugin settings](./images/OctoCheese-Settings.png)

3. Restart OctoPrint

## Configuration

Configure via the OctoPrint settings UI. By default the plugin assumes:
- The X Axis is the stirring stepper
- The water heater is plugged into the "Bed" heater port
- The water heater temperature is plugged into the "Bed" temperature port
- The Milk temperature is plugged into the "Hotend" temperature port

If using the [CheeseMaker Circuit](https://github.com/AutomaticCheeseMaker/CheeseMaker-Circuit) then the above assumptions are correct

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

## Example GCode
You can find gcode for testing different functionality of the Cheese-o-matic inside of the `Test_Programs` folder. You'll also find full gcode for making cheeses inside the `Cheese_Programs` folder.

## Home Assistant Integration
To use with Home Assistant you need to have MQTT enabled as detailed above. You then need to add the contents of `./home_assistant/configuration.yaml` to your home assistant `configuration.yaml` file. This will provide you with all the sensors to use in your dashboards. An example dashboard is provided in `./home_assistant/dashboard.yaml`

## Known Bugs

- Currently there is an issue where the firmware on the Arduino will disconnect requiring a power cycle when too many consecutive message GCodes are issued (M953 & M954).
