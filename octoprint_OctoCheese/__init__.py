from __future__ import absolute_import
import time

import octoprint.plugin
from octoprint.util import RepeatedTimer, ResettableTimer

class OctoCheese(octoprint.plugin.AssetPlugin,
					octoprint.plugin.SettingsPlugin,
					octoprint.plugin.ShutdownPlugin,
					octoprint.plugin.StartupPlugin,
					octoprint.plugin.TemplatePlugin):

	def __init__(self):
		self._stirringTimer = None
		self._cheesePause = None
		self._stirringOn = False
		self._directionForward = False

	def catch_m950(self, comm_instance, phase, cmd, cmd_type, gcode, *args, **kwargs):
		if gcode and gcode == "M950":
			if cmd == "M950 S1":
				self._logger.debug(u"Stirring ON")
				cmd = ""
				self._stirringOn = True
				self._restartTimer()
			elif cmd == "M950 S0":
				self._logger.debug(u"Stirring OFF")
				cmd = ""
				self._stirringOn = False
				self._restartTimer()
			else:
				self._logger.debug(u"Invalid Stirring Command")
		# M951 S100
		elif gcode and gcode == "M951":
			parts = cmd.split(" ")
			if len(parts) != 2 or parts[1][0] != "S":
				self._logger.debug(u"Invalid Stirring Pause")
			else:
				self._printer.set_job_on_hold(True)
				pauseInSeconds = int(parts[1][:1])
				if self._cheesePause != None:
					self.cheesePauseCallback()
				self._cheesePause = ResettableTimer(pauseInSeconds, self.cheesePauseCallback)
				self._cheesePause.start()
		return cmd,

	def cheesePauseCallback(self):
		self._printer.set_job_on_hold(False)
		self._cheesePause.cancel()
		self._cheesePause = None

	def _restartTimer(self):
		# stop the timer
		if self._stirringTimer:
			self._logger.debug(u"Stopping Stir Timer")
			self._stirringTimer.cancel()
			self._stirringTimer = None

		interval = self._settings.get_int(['interval'])
		if self._stirringOn and interval:
			self._logger.debug(u"Starting Stir Timer")
			self._stirringTimer = RepeatedTimer(interval, self.StirTimerCallback, None, None, True)
			self._stirringTimer.start()

	def StirTimerCallback(self):
		if (not self._stirringOn):
			self._restartTimer()
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
		self._restartTimer()

	##-- ShutdownPlugin hooks

	def on_shutdown(self):
		self._logger.info(u"Stopping OctoCheese")
		self._stirringOn = False
		self._restartTimer()


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
			stepperEnd=100
		)

	def on_settings_initialized(self):
		self._logger.debug(u"OctoCheese on_settings_initialized()")
		self._restartTimer()

	def on_settings_save(self, data):
		# make sure we don't get negative values
		for k in ('interval', 'stepperSpeed'):
			if data.get(k): data[k] = max(0, int(data[k]))
		if (not (data.get('stepper') == 'X' or data.get('stepper') == 'Y' or data.get('stepper') == 'Z' or data.get('stepper') == 'E')):
			data['stepper'] = 'X'

		self._logger.debug(u"OctoCheese on_settings_save(%r)" % (data,))

		octoprint.plugin.SettingsPlugin.on_settings_save(self, data)
		self._restartTimer()

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
