from __future__ import absolute_import
import time

import octoprint.plugin
from octoprint.util import RepeatedTimer, ResettableTimer

MQTT_OCTOCHEESE_PAUSED="octoPrint/plugin/OctoCheese/paused"
MQTT_OCTOCHEESE_MESSAGE="octoPrint/plugin/OctoCheese/message"

class OctoCheese(octoprint.plugin.AssetPlugin,
					octoprint.plugin.SettingsPlugin,
					octoprint.plugin.ShutdownPlugin,
					octoprint.plugin.StartupPlugin,
					octoprint.plugin.TemplatePlugin):

	def __init__(self):
		self._stirringTimer = None
		self._cheesePause = None
		self._cheeseTempPause = None
		self._stirringOn = False
		self._directionForward = False
		self._cheeseTemp = -1
		self._cheeseTempCount = 0
		self._cheeseTempSensor = ""
		self.mqtt = False
		self.mqtt_publish = lambda *args, **kwargs: None
		self.mqtt_subscribe = lambda *args, **kwargs: None

	def catch_m950(self, comm_instance, phase, cmd, cmd_type, gcode, *args, **kwargs):
		retCmd = cmd
		# M950 S1 - Turn Stirrer on
		# M950 S0 - Turn Stirrer off
		if gcode and gcode == "M950":
			if cmd == "M950 S1":
				self._logger.debug(u"Stirring ON")
				retCmd = "M118 E1 Stirring ON"
				self._stirringOn = True
				self.restartStirringTimer()
			elif cmd == "M950 S0":
				self._logger.debug(u"Stirring OFF")
				stepper = self._settings.get(['stepper'])
				retCmd = [
					"M118 E1 Stirring OFF",
					"M18 {0}".format(stepper)
				]
				self._stirringOn = False
				self.restartStirringTimer()
			else:
				self._logger.debug(u"Invalid Stirring Command")
				retCmd = "M118 E1 Invalid M950 command"
		# M951 S100 - Wait 100s before continuing print
		# M951      - Cancel wait
		elif gcode and gcode == "M951":
			parts = cmd.split(" ")
			if len(parts) == 1:
				if self._cheesePause != None:
					self.cheesePauseEnd()
				self._printer.set_job_on_hold(False)
				retCmd = "M118 E1 Cancelling Timer - Resuming Print"
			elif len(parts) > 2 or parts[1][0] != "S":
				self._logger.debug(u"Invalid Stirring Pause")
				retCmd = "M118 E1 Invalid M951 command"
			else:
				pauseInSeconds = int(parts[1][1:])
				retCmd = "M118 E1 Sleeping for {0}s".format(pauseInSeconds)
				if self._cheesePause != None:
					self.cheesePauseEnd()
				self._printer.set_job_on_hold(True)
				self._cheesePause = ResettableTimer(pauseInSeconds, self.cheesePauseEnd)
				self._cheesePause.start()
		# M952 B38 - Wait for bed to hit 38C
		# M952 H38 - Wait for hotend to hit 38C
		# M952     - Cancel wait
		elif gcode and gcode == "M952":
			parts = cmd.split(" ")
			if len(parts) == 1:
				if self._cheeseTempPause != None:
					self.cheeseTempPauseEnd()
				self._printer.set_job_on_hold(False)
				retCmd = "M118 E1 Cancelling Temp Wait - Resuming Print"
			elif len(parts) > 2 or (parts[1][0] != "B" and parts[1][0] != "H"):
				self._logger.debug(u"Invalid Stirring Pause")
				retCmd = "M118 E1 Invalid M952 command"
			else:
				if self._cheeseTempPause != None:
					self.cheeseTempPauseEnd()
				self._cheeseTemp = int(parts[1][1:])
				self._cheeseTempSensor = parts[1][:1]
				retCmd = "M118 E1 Waiting for {0}C on {1}".format(self._cheeseTemp, self._cheeseTempSensor)
				self._printer.set_job_on_hold(True)
				self._cheeseTempPause = RepeatedTimer(3, self.cheeseTempPauseCallback, None, None, True)
				self._cheeseTempPause.start()
		# M953 STRING - Send MQTT String
		elif gcode and gcode == "M953":
			if self.mqtt:
				parts = cmd.split(" ")
				if len(parts) > 1:
					stringToSend = " ".join(parts[1:])
					self.mqtt_publish(MQTT_OCTOCHEESE_MESSAGE, stringToSend)
					retCmd = "M118 E1 Sent to MQTT: {0}".format(stringToSend)
				else:
					self._logger.debug(u"Invalid Text")
					retCmd = "M118 E1 Invalid M953 command"
		# M954 STRING - Send MQTT String and wait for user
		# M954        - Continue if a wait has been issued
		elif gcode and gcode == "M954":
			if self.mqtt:
				parts = cmd.split(" ")
				if len(parts) > 1:
					stringToSend = " ".join(parts[1:])
					self.mqtt_publish(MQTT_OCTOCHEESE_MESSAGE, stringToSend)
					self.mqtt_publish(MQTT_OCTOCHEESE_PAUSED, 1)
					self._printer.set_job_on_hold(True)
					retCmd = "M118 E1 Waiting for user to finish: {0}".format(stringToSend)
				else:
					self.mqtt_publish(MQTT_OCTOCHEESE_PAUSED, 0)
					self._printer.set_job_on_hold(False)
					retCmd = "M118 E1 Cancelled user wait"
		# M955 S1 RENNET              - Release Rennet
		# M955 S1 CALCIUM_CHLORIDE    - Release Calcium Chloride
		# M955 S1 ANNATTO             - Release Annatto
		# M955 S1 CULTURE             - Release Culture
		# M955 S0 RENNET              - Unrelease Rennet
		# M955 S0 CALCIUM_CHLORIDE    - Unrelease Calcium Chloride
		# M955 S0 ANNATTO             - Unrelease Annatto
		# M955 S0 CULTURE             - Unrelease Culture
		elif gcode and gcode == "M955":
			parts = cmd.split(" ")
			if len(parts) != 3 or parts[1][0] != "S":
				self._logger.debug(u"Invalid Servo Release Command")
				retCmd = "M118 E1 Invalid M955 command"
			releaseType = " ".join(parts[2:])
			release = int(parts[1][1:])

			servoPosition = 0
			servoNumber = 0

			if release == 0:
				servoPosition = 180
			else:
				servoPosition = 0

			if releaseType == "RENNET":
				servoNumber = self._settings.get_int(['rennetServo'])
			elif releaseType == "CALCIUM_CHLORIDE":
				servoNumber = self._settings.get_int(['calciumChlorideServo'])
			elif releaseType == "ANNATTO":
				servoNumber = self._settings.get_int(['annattoServo'])
			elif releaseType == "CULTURE":
				servoNumber = self._settings.get_int(['cultureServo'])

			retCmd = [
				"M118 E1 {1}: {0}".format(releaseType, "Resetting" if release == 0 else "Releasing")
				"M280 P{0} S{1}".format(servoNumber,servoPosition)
			]

			if release != 0:
				retCmd.append("M281 P{0}".format(servoNumber))

		return retCmd

	# Used by M954
	def cheeseMqttPauseEnd(self, topic, message, retained=None, qos=None, *args, **kwargs):
		if message == "0":
			self._printer.set_job_on_hold(False)
			self._printer.commands([
				"M118 E1 MQTT Cancelled user wait"
			])

	# Used by M952
	def cheeseTempPauseCallback(self):
		if (self._cheeseTempSensor != "" or self._cheeseTemp == -1):
			self.cheeseTempPauseEnd()
		temps = self._printer.get_current_temperatures()
		if temps != {}:
			if self._cheeseTempSensor == "B" and float(temps.get("bed").get("actual")) >= self._cheeseTemp:
				if self._cheeseTempCount >= 2:
					self.cheeseTempPauseEnd()
				else:
					self._cheeseTempCount += 1
			elif self._cheeseTempSensor == "H" and float(temps.get("tool0").get("actual")) >= self._cheeseTemp:
				if self._cheeseTempCount >= 2:
					self.cheeseTempPauseEnd()
				else:
					self._cheeseTempCount += 1
			else:
				self._cheeseTempCount = 0

	def cheeseTempPauseEnd(self):
		self._printer.set_job_on_hold(False)
		self._cheeseTempPause.cancel()
		self._cheeseTempPause = None
		self._cheeseTemp = -1
		self._cheeseTempCount = 0
		self._cheeseTempSensor = ""

	# Used by M951
	def cheesePauseEnd(self):
		self._printer.set_job_on_hold(False)
		self._cheesePause.cancel()
		self._cheesePause = None

	# Used by M950
	def restartStirringTimer(self):
		# stop the timer
		if self._stirringTimer:
			self._logger.debug(u"Stopping Stir Timer")
			self._stirringTimer.cancel()
			self._stirringTimer = None

		interval = self._settings.get_int(['interval'])
		if self._stirringOn and interval:
			self._logger.debug(u"Starting Stir Timer")
			self._stirringTimer = RepeatedTimer(interval, self.stirTimerCallback, None, None, True)
			self._stirringTimer.start()

	def stirTimerCallback(self):
		if (not self._stirringOn):
			self.restartStirringTimer()
		else:
			stepperStart = self._settings.get_int(['stepperStart'])
			stepperEnd = self._settings.get_int(['stepperEnd'])
			stepperSpeed = self._settings.get_int(['stepperSpeed'])
			stepper = self._settings.get(['stepper'])
			if (self._directionForward):
				self._printer.commands([
					'G0 {0}{1} F{2}'.format(stepper,stepperStart,stepperSpeed)
				])
			else:
				self._printer.commands([
					'G0 {0}{1} F{2}'.format(stepper,stepperEnd,stepperSpeed)
				])
			self._directionForward = (not self._directionForward)

	##-- StartupPlugin hooks

	def on_after_startup(self):
		self._logger.info(u"Starting OctoCheese")
		self.restartStirringTimer()

		helpers = self._plugin_manager.get_helpers("mqtt", "mqtt_publish", "mqtt_subscribe")
		if helpers:
			if "mqtt_publish" in helpers and "mqtt_subscribe" in helpers:
				self.mqtt = True
				self.mqtt_publish = helpers["mqtt_publish"]
				self.mqtt_subscribe = helpers["mqtt_subscribe"]
				self.mqtt_subscribe(MQTT_OCTOCHEESE_PAUSED, self.cheeseMqttPauseEnd)

	##-- ShutdownPlugin hooks

	def on_shutdown(self):
		self._logger.info(u"Stopping OctoCheese")
		self._stirringOn = False
		self.restartStirringTimer()


	##-- AssetPlugin hooks

	def get_assets(self):
		return dict(js=["js/OctoCheese.js"])

	##~~ SettingsPlugin mixin

	def get_settings_version(self):
		return 1

	def get_template_configs(self):
		return [
			dict(type="settings", name="OctoCheese", custom_bindings=False)
		]

	def get_settings_defaults(self):
		return dict(
			interval=15,
			stepper="X",
			stepperSpeed=1200,
			stepperStart=0,
			stepperEnd=100,
			rennetServo=0,
			calciumChlorideServo=1,
			annattoServo=2,
			cultureServo=3
		)

	def on_settings_initialized(self):
		self._logger.debug(u"OctoCheese on_settings_initialized()")
		self.restartStirringTimer()

	def on_settings_save(self, data):
		# make sure we don't get negative values
		for k in ('interval', 'stepperSpeed'):
			if data.get(k): data[k] = max(0, int(data[k]))
		# make sure we have a value between 0 and 3
		for k in ('rennetServo', 'calciumChlorideServo', 'annattoServo', 'cultureServo'):
			if data.get(k): data[k] = min(max(0, int(data[k])), 3)
		if (not (data.get('stepper') == 'X' or data.get('stepper') == 'Y' or data.get('stepper') == 'Z' or data.get('stepper') == 'E')):
			data['stepper'] = 'X'

		self._logger.debug(u"OctoCheese on_settings_save(%r)" % (data,))

		octoprint.plugin.SettingsPlugin.on_settings_save(self, data)
		self.restartStirringTimer()

	##~~ Softwareupdate hook

	def get_update_information(self):
		return dict(
			emergencyaction=dict(
				displayName="OctoCheese Plugin",
				displayVersion=self._plugin_version,

				# version check: github repository
				type="github_release",
				user="thomaspreece",
				repo="OctoCheese",
				current=self._plugin_version,

				# update method: pip
				pip="https://github.com/thomaspreece/OctoCheese/archive/{target_version}.zip"
			)
		)

__plugin_name__ = "OctoCheese"

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = OctoCheese()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information,
		"octoprint.comm.protocol.gcode.queuing": __plugin_implementation__.catch_m950,
	}
