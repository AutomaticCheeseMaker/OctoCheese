; OctoCheese GCode for Edam Cheese described at https://www.youtube.com/watch?v=7yMmovpXyW8

2 tbsp Cheese Salt

;M954 Add 10L of Milk;
;M954 Put 1 tsp Calcium Chloride diluted with milk in Dispencer;
;M954 Put 1/2 tsp liquid rennet in Dispencer;
;M954 Put 1/8 tsp Mesophilic Culture in Dispencer;
M954 Begin Cheese Making!;

M950 S1; Start stirring
M140 S31; Heat to 31C
M952 H31; Wait to milk hit 31C

M950 S0; Stop stirring
M955 S1 CULTURE;
M951 S60; Wait for a minute
M950 S1; Start stirring
M951 S60; Wait for a minute
M950 S0; Stop stirring

M951 S1800; Wait for 30 minute
M955 S1 CALCIUM_CHLORIDE;
M955 S1 RENNET;

M950 S1; Start stirring
M951 S60; Stir for a minute
M950 S0; Stop stirring

M951 S2400; Wait for 40 mins
M954 Cut the curd into 1.25cm (1/2 inch) cubes;

M950 S1; Start stirring

M953 Boil about 5L of water and let cool;

; Over 30 mins bring up to 33C
M140 S31; Heat to 31C
M951 S600; Wait for 10 mins
M140 S32; Heat to 32C
M951 S600; Wait for 10 mins
M140 S33; Heat to 33C
M951 S600; Wait for 10 mins

; Wait for curds to rest
M950 S0; Stop stirring
M951 S300; Wait for 5 mins

M140 S0; Turn off heat
M954 Laddle out whey until hit top of curds. Reserve this whey. Top pot back up with preboiled water;

M950 S1; Start stirring

; Heat to 37C over 30m
M140 S31; Heat to 31C
M951 S300; Wait for 5 mins
M140 S33; Heat to 33C
M951 S300; Wait for 5 mins
M140 S34; Heat to 34C
M951 S300; Wait for 5 mins
M140 S35; Heat to 35C
M951 S300; Wait for 5 mins
M140 S36; Heat to 36C
M951 S300; Wait for 5 mins
M140 S37; Heat to 37C
M951 S300; Wait for 5 mins

M950 S0; Stop stirring

; Drain & retain whey
M954 DRAIN & Bin Whey (Keeping laddled whey instead);

M954 Press Cheese under 12kg;
M953 Begin heating whey to 50C;
M951 S1800; Wait for 30 mins
M954 Loosen cheesecloth and transfer cheese+cloth to hot whey
M951 S600; Wait for 10 mins
M954 Flip and rewrap cheese
M951 S600; Wait for 10 mins


M954 Press Cheese under 22.5kg for 6 hours
M954 Flip and rewrap cheese
M954 Press Cheese under 22.5kg for 7 hours

M954 Leave in Brine for 12h, flipping half way

M954 Air dry for 2-3 days then wax. Age for 2 months.
