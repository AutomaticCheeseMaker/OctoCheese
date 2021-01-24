; OctoCheese GCode for Halloumi Cheese described at https://www.youtube.com/watch?v=PPNQmV7roos&t=29s

; Put 8L milk in
M955 S1 CALCIUM_CHLORIDE; Put 2ml (1/2 tsp) Calcium Chloride in
M953 Released Calcium Chloride;
M950 S1; Start stirring
M140 S32; Heat to 32C
M953 Waiting 32C;
M952 H32; Wait to milk hit 32C
M953 Released Rennet
M955 S1 RENNET; Put 2ml (1/2 tsp) liquid rennet in

M951 S60; Stir for a minute
M950 S0; Stop stirring
M953 Waiting for 40 mins;
M951 S2400; Wait for 40 mins
M954 CUT_CURDS; Cut Curds

M951 S300; Wait for 5 mins
M950 S1; Start stirring

;Over 20 mins bring upto 40C
M140 S34; Heat to 34C
M953 Heat to 34C;
M951 S300; Wait for 5 mins
M140 S36; Heat to 36C
M953 Heat to 36C;
M951 S300; Wait for 5 mins
M140 S38; Heat to 38C
M953 Heat to 38C;
M951 S300; Wait for 5 mins
M140 S40; Heat to 40C
M953 Heat to 40C;
M951 S300; Wait for 5 mins

; Wait for curds to rest
M950 S0; Stop stirring
M951 S600; Wait for 10 mins

; Drain & retain whey
M954 DRAIN;

; Press Cheese under 4L water/4kg for 10mins
; Turn over and press Cheese under 4L water/4kg for 20mins
; Cut curd mass into blocks
; Boil whey
; Put blocks into whey until they float
; Take out and salt & mint