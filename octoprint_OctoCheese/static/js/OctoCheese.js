$(function() {
    function OctoCheeseViewModel(parameters) {
        var self = this;
        var msgTitle = "OctoCheese";
        var msgType = "error";
        var autoClose = false;

        self.controlViewModel = parameters[0];
        self.settingsViewModel = parameters[1];

        self.getAdditionalControls = function() {
    				var buttons = [
    					{
                name: "OctoCheese - General",
                type: "section",
                layout: "horizontal",
                children: [
      						{
                    type: "javascript",
                    javascript: "OctoPrint.control.sendGcode(\"M950 S1\");",
                    name: "Stirrer On"
                  },
                  {
                    type: "javascript",
                    javascript: "OctoPrint.control.sendGcode(\"M950 S0\");",
                    name: "Stirrer Off"
                  },
                  {
                    type: "javascript",
                    javascript: "OctoPrint.control.sendGcode(\"M140 S0\");",
                    name: "Heater Off"
                  },
                  {
                    type: "javascript",
                    javascript: "OctoPrint.control.sendGcode(\"M951\");",
                    name: "Cancel Time Pause"
                  },
                  {
                    type: "javascript",
                    javascript: "OctoPrint.control.sendGcode(\"M952\");",
                    name: "Cancel Heat Pause"
                  },
                  {
                    type: "javascript",
                    javascript: "OctoPrint.control.sendGcode(\"M954\");",
                    name: "Cancel User Pause"
                  }
    					  ]
              },
              {
                name: "OctoCheese - Dispensers",
                type: "section",
                layout: "horizontal",
                children: [
                  {
                    type: "javascript",
                    javascript: "OctoPrint.control.sendGcode(\"M955 S0 RENNET\");",
                    name: "Close Rennet Dispenser"
                  },
                  {
                    type: "javascript",
                    javascript: "OctoPrint.control.sendGcode(\"M955 S1 RENNET\");",
                    name: "Open Rennet Dispenser"
                  },
                  {
                    type: "javascript",
                    javascript: "OctoPrint.control.sendGcode(\"M955 S0 CALCIUM_CHLORIDE\");",
                    name: "Close Calcium Chloride Dispenser"
                  },
                  {
                    type: "javascript",
                    javascript: "OctoPrint.control.sendGcode(\"M955 S1 CALCIUM_CHLORIDE\");",
                    name: "Open Calcium Chloride Dispenser"
                  },
                  {
                    type: "javascript",
                    javascript: "OctoPrint.control.sendGcode(\"M955 S0 ANNATTO\");",
                    name: "Close Annatto Dispenser"
                  },
                  {
                    type: "javascript",
                    javascript: "OctoPrint.control.sendGcode(\"M955 S1 ANNATTO\");",
                    name: "Open Annatto Dispenser"
                  },
                  {
                    type: "javascript",
                    javascript: "OctoPrint.control.sendGcode(\"M955 S0 CULTURE\");",
                    name: "Close Culture Dispenser"
                  },
                  {
                    type: "javascript",
                    javascript: "OctoPrint.control.sendGcode(\"M955 S1 CULTURE\");",
                    name: "Open Culture Dispenser"
                  }
    					  ]
              }
    				];
    			return buttons;
    		};

        self.onDataUpdaterPluginMessage = function(plugin, data) {
            if (plugin != "OctoCheese") {
                return;
            }

            if (data.type == "popup") {
                new PNotify({
                    text: data.msg,
                    title: msgTitle,
                    type: msgType,
                    hide: autoClose
                });
            }
        }
    }

    ADDITIONAL_VIEWMODELS.push([
        OctoCheeseViewModel,

        // This is a list of dependencies to inject into the plugin, the order which you request
        // here is the order in which the dependencies will be injected into your view model upon
        // instantiation via the parameters argument
        [],

        // Finally, this is the list of selectors for all elements we want this view model to be bound to.
        []
    ]);
});
