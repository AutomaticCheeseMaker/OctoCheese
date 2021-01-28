; OctoCheese GCode for Halloumi Cheese described at https://www.youtube.com/watch?v=PPNQmV7roos&t=29s

M954 Add 8L of Milk;
M954 Put 2ml (1/2 tsp) Calcium Chloride diluted with milk in Dispencer
M954 Put 2ml (1/2 tsp) liquid rennet in Dispencer

; Put 8L milk in
M955 S1 CALCIUM_CHLORIDE; Put 2ml (1/2 tsp) Calcium Chloride in
M950 S1; Start stirring
M140 S32; Heat to 32C
M952 H32; Wait to milk hit 32C
M955 S1 RENNET; Put 2ml (1/2 tsp) liquid rennet in

M951 S60; Stir for a minute
M950 S0; Stop stirring
M951 S2400; Wait for 40 mins
M954 CUT the CURDS; Cut Curds

M951 S300; Wait for 5 mins
M950 S1; Start stirring

;Over 20 mins bring upto 40C
M140 S34; Heat to 34C
M951 S300; Wait for 5 mins
M140 S36; Heat to 36C
M951 S300; Wait for 5 mins
M140 S38; Heat to 38C
M951 S300; Wait for 5 mins
M140 S40; Heat to 40C
M951 S300; Wait for 5 mins

; Wait for curds to rest
M950 S0; Stop stirring
M951 S600; Wait for 10 mins

M140 S0; Turn off heat

; Drain & retain whey
M954 DRAIN & Retain Whey;

M954 Begin heating whey to boiling
M954 Press Cheese under 4L water/4kg then continue
M951 S600; Wait for 10 mins
M954 Turn over and press Cheese under 4L water/4kg then continue
M951 S1200; Wait for 20mins
M954 Cut curd mass into blocks
M954 Put blocks into whey until they float
M954 Take out and salt & mint
