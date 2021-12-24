# Attack summary: Tor Browser plus another browser
Users can have their real IP "revealed" to websites opened in Tor Browser by:

- moving the mouse from Tor Browser to another non-Tor browser (and vice versa)
- switching said browsers with hotkeys 

# Attack summary: CTR-TAB in Tor Browser
Tor Browser has separate exit nodes (and IPs) for each tab. 
However, switching tabs with hotkeys creates a unique pattern,
meaning all opened websites (despite being opened on separate tabs) 
can be linked to the same user.

# Preconditions
1. JavaScript must be enabled on both browsers.
2. Websites must share mouse-movement data.

Many websites *already share data* for anti-fraud purposes.

Also, Google Tag Manager could be gathering such data 
and is being used by [~18 million websites](https://trends.builtwith.com/websitelist/Google-Tag-Manager).
If such data is indeed gathered in one place,
then whoever has access to it can use this attack.



# Test results
I tested it on my PC:
 - The match is **extremely accurate** when using **CTR TAB in Tor** 
(that is, only one browser).

![image](https://user-images.githubusercontent.com/10809024/147253839-c1d2413f-2e31-4b3b-bd1b-fe2a75824812.png)


 - It is **very accurate in Tor-to-normal**, but less so 
due to speed. It can be further improved by projecting 
the mouse track on the border of the browser.

![image](https://user-images.githubusercontent.com/10809024/147254027-6cbc6f85-d82b-4ed8-9834-6c5912920dfd.png)


This has to be tested with data from users 
that don't know of the attack (double-blind).   
Also, it has to be independently verified by other researchers,
although I doubt there's anything that makes the attack infeasible. 

### Tor has been notified and they will change the documentation
["Discourage more running a browser in parallel to Tor Browser"](https://gitlab.torproject.org/tpo/web/support/-/issues/280)


# Metrics analysed
The following metrics are compared between users 
when they are within a specified time difference. 

Mouse movement close to entry and exit locations: 

- **angle**
- mouse **speed**
- mouse **acceleration**

Due to [time granulation in Tor at 100ms](https://gitlab.torproject.org/legacy/trac/-/issues/1517) 
speed and acceleration can't be calculated in a traditional way.
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

Firstly, **a center of all matching points** is created 
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

So, more accurate methods are used. 

## Increasing accuracy
To reduce false positives smaller, 
thresholds can be used for all metrics. 

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
- Can single-browser single-tab metrics be used to extract patterns 
related to a user's UI layout (file shortcuts on desktop, etc.)?
