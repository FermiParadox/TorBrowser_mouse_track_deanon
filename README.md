# Goals
Check de-anonymization risk of Tor Browser users, through:

- mouse-over from Tor browser to a clearnet browser (and vice versa)
- switching browsers with hotkeys (implementation pending)


There are probably many similar ways the user 
can be deanonymized. Not all are examined here.

### Tor is unaware of the attack
 
[Official page:](https://support.torproject.org/tbb/tbb-17/)

> **Is it safe to run Tor Browser and another browser 
> at the same time?**

> If you run Tor Browser and another browser at the same time, 
> it won't affect Tor's performance or privacy properties. 
> However, be aware that your other browser is not keeping 
> your activity private, and you may forget 
> and accidentally use that non-private browser to do something 
> that you intended to do in Tor Browser.

# Metrics analysed
The following are compared between users 
when they are within a specified time difference. 

## Mouse movement
At entry and exit locations: 

- angle
- mouse speed
- mouse acceleration

## Exit and entry point distances on both browsers




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

# Other metrics to track
- entry points' distances compared to exit points'

# Thresholds
Metrics will be compared for time differences approaching 
the expected latency differences of clearnet/Tor. 
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