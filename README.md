# Goals
Check de-anonymization risk of Tor Browser users, through:

- mouse-over from Tor browser to another non-Tor browser (and vice versa)
- switching browsers with hotkeys 


There are probably many similar ways the user 
can be deanonymized. Not all are examined here.

# Results
I tested it on my PC with Tor and another browser:
 - The match is **extremely accurate** when using **CTR TAB in Tor**.

![tor_to_tor](https://github.com/FermiParadox/torWindowSwitchDeanon/blob/master/tor_to_tor_CTR_TAB.png)

 - It is **very accurate in Tor-to-normal**, but less so 
due to speed. It can be further improved by projecting 
the mouse track on the border of the browser.

![tor_to_normal](https://github.com/FermiParadox/torWindowSwitchDeanon/blob/master/tor_to_normal2.png)

This has to be tested with real data (double-blind).   
Also, just to make sure, it has to be 
independently verified by other researchers.

### Tor has been notified and they will change the documentation
["Discourage more running a browser in parallel to Tor Browser"](https://gitlab.torproject.org/tpo/web/support/-/issues/280)


# Metrics analysed
The following are compared between users 
when they are within a specified time difference. 

Mouse movement close to entry and exit locations: 

- **angle**
- mouse **speed**
- mouse **acceleration**

Due to time granulation at 100ms speed and acceleration are 
useless unless they are calculated in a different way.
A way around this is deducing the elapsed time based on 
registered points. The storage of x-y values seems to be following 
the speed pattern of my mouse movements. 

However, delays due to other simultaneous 
browser events perhaps will affect it.

### Tor CTR TAB metrics
Only the location and the time-frame is used, 
since probably most users stop moving their mouse 
before switching tab.

## Exit and entry point distances on both browsers

Measuring the entry-exit distance between points in a browser 
and comparing it with other browsers results in the creation of
unique fingerprints. 

Firstly, a center of all matching points is created 
(for each browser). Then the matching users' centers 
are taken as a common point 
and the distance of each matching point is compared.


### Pixels are like chessboard boxes

Slow mouse movement results erroneously in exit/entry angles 
of 45.00000, 90.00000 or 0.00000 degrees. 
Or other "standard" values for slightly higher speeds.

That's because x,y are "quantized" and during 
slow speeds adjacent points are noted. 
Meaning we can't take just the last 2 points 
before browser exit to calculate the angle at 
slow speeds.

Much more accurate (yet computationally 
more demanding) methods are possible. 

## Increasing accuracy
To reduce false positives smaller thresholds 
can be used for all metrics. 

Also, the distance comparison of critical points 
(that is, suspected exit or entry points) can be calculated 
while taking into account speed and acceleration.

# Bug
It sometimes crashes 
(when specific mouse-tracks are stored in a browser tab session)
Simply restart the program and open new tabs.

I'll fix it in the future.

# Software limitations 

This is simply a proof of concept.   

I haven't taken into account all scenarios, e.g.: 
- user trying to deceive the server by manipulating data
- interrupted data transfer
- changing IP during session
- assignment of existing IP to new user
- accuracy (false positives and false negatives)


# Investigate later
- Can single-browser single-tab metrics be used to extract user patterns 
related to user's UI layout (file shortcuts on desktop, etc.)?
