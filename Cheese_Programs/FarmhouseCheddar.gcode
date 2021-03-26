; OctoCheese GCode for FarmhouseCheddar Cheese described at https://www.youtube.com/watch?v=IsmW_XRXCGg

;M954 Add 8L of Milk;
;M954 Put 1 tsp Calcium Chloride diluted with milk in Dispencer;
;M954 Put 1 tsp liquid rennet in Dispencer;
;M954 Put 1/8 tsp Mesophilic Culture in Dispencer;
M954 Begin Cheese Making!;

M955 S1 CALCIUM_CHLORIDE;
M950 S1; Start stirring
M140 S32; Heat to 32C
M952 H32; Wait to milk hit 32C
M955 S1 CULTURE;
M951 S60; Stir for a minute
M950 S0; Stop stirring

M955 S1 RENNET;
M951 S60; Stir for a minute
M950 S0; Stop stirring

M951 S2700; Wait for 45 mins
M954 Cut the curd into 1.25cm (1/2 inch) cubes;

M950 S1; Start stirring

; Over 30 mins bring up to 38C
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
M140 S38; Heat to 38C
M951 S600; Wait for 10 mins

; Wait for curds to rest
M950 S0; Stop stirring
M951 S600; Wait for 10 mins

M140 S0; Turn off heat

; Drain & retain whey
M954 DRAIN & Retain Whey;

M954 Tie the corners of the cheesecloth into a knot and hang the bag over a bowl. Drain for 1 hour.
M951 S3600; Wait for 60 mins

M954 Gently mill into walnut sized pieces. Mill in 2 tbsp salt.
M954 Press Cheese under 5kg then continue
M951 S600; Wait for 10 mins
M954 Flip and rewrap cheese. Press Cheese under 10kg then continue
M951 S600; Wait for 10 mins
M954 Flip and rewrap cheese. Press Cheese under 25kg for 12 hours

M954 Follow remaining instructions for drying/aging
