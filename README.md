# Goals
Check de-anonymization risk of Tor Browser users, through:

- mouse-over from Tor browser to a clearnet browser (and vice versa)
- switching browsers with hotkeys (implementation pending)


There are probably many ways the user can be de-anonymized. 
Not all are examined here.

# Metrics analysed
The following are compared between users 
when they are within a specified time difference. 

## Mouse movement
At entry and exit locations: 

- angle
- mouse speed
- mouse acceleration



### Pixels are like chessboard boxes

I am assuming, slow mouse movement 
results erroneously in exit/entry angles 
of 45.00000, 90.00000 or 0.00000 degrees. 
Or other "standard" values.

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
Metrics are compared for time differences approaching 
the expected latency differences of clearnet/Tor. 

To reduce false positives smaller thresholds 
can be used for all metrics.

# Software limitations 

I haven't taken into account all scenarios, e.g.: 
- user trying to deceive the server by manipulating data
- interrupted data transfer
- changing IP during session
- assignment of existing IP to new user