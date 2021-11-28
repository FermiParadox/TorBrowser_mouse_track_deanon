# Goals
Check de-anonymization risk of Tor Browser users, through:

- mouse-over from Tor browser to another non-Tor browser (and vice versa)
- switching browsers with hotkeys (implementation pending)


There are probably many similar ways the user 
can be deanonymized. Not all are examined here.

### Tor might be unaware of this attack...
 
[Official page:](https://support.torproject.org/tbb/tbb-17/)

> **Is it safe to run Tor Browser and another browser 
> at the same time?**

> If you run Tor Browser and another browser at the same time, 
> it won't affect Tor's performance or privacy properties. 
> However, be aware that your other browser is not keeping 
> your activity private, and you may forget 
> and accidentally use that non-private browser to do something 
> that you intended to do in Tor Browser.

### ...but they have taken measures to reduce time accuracy

[Bug 1517: Reduce precision of time for Javascript](https://gitweb.torproject.org/user/mikeperry/tor-browser.git/commit/?h=bug1517)
> This clamps Javascript's time precision to 100ms for most things, without
altering event delivery or responsiveness. It also clamps keyboard events
(such as keypress, keyup, keydown, etc) to 250ms resolution, to mitigate
keystroke fingerprinting.


# Metrics analysed
The following are compared between users 
when they are within a specified time difference. 

Mouse movement close to entry and exit locations: 

- **angle**
- mouse **speed**
- mouse **acceleration**

Due to time granulation at 100ms speed and acceleration might be
useless unless they are calculated in a different way.
A way around this might be deducing the elapsed time based on 
registered points. The storage of x-y values seems to be following 
the speed pattern of my mouse movements. Delays due to other simultaneous 
browser events perhaps can affect it.

## Exit and entry point distances on both browsers

Measuring the entry-exit distance between points in a browser 
and comparing it with other browsers would probably deanonymize 
the user.


### Pixels are like chessboard boxes

I am assuming, slow mouse movement 
results erroneously in exit/entry angles 
of 45.00000, 90.00000 or 0.00000 degrees. 
Or other "standard" values for slightly higher speeds.

That's because x,y are "quantized" and during 
slow speeds adjacent points are noted. 
Meaning we can't take just the last 2 points 
before browser exit to calculate the angle at 
slow speeds.

Much more accurate (yet computationally 
expensive) methods are possible. 

# Thresholds
Metrics will be compared for time differences approaching 
the expected latency differences of non-Tor/Tor. 
(note: latency might not be an issue; 
must check whether collected time-data is based on PC clock)

To reduce false positives smaller thresholds 
can be used for all metrics.

# Software limitations 

This is simply a proof of concept.   

I haven't taken into account all scenarios, e.g.: 
- user trying to deceive the server by manipulating data
- interrupted data transfer
- changing IP during session
- assignment of existing IP to new user


# Investigate later
- Can single browser metrics be used to extract user patterns 
related to user's UI layout (file shortcuts on desktop, etc.)?