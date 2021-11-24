# Goals
Check de-anonymization risk of Tor Browser users, through:

- mouse-over from one browser to the other
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

To my understanding, slow mouse movement 
results erroneously in exit/entry angles 
of 45.00000, 90.00000 or 0.00000 degrees. 

That's because x,y are "quantized" and during 
slow speeds adjacent points are noted. 
Meaning we can't take just the last 2 points 
before browser exit to calculate the angle at 
slow speeds.

Much more accurate (yet computationally 
expensive) methods are possible. 


# Software limitations 

I haven't taken into account all scenarios, e.g.: 
- user trying to deceive the server by manipulating data
- interrupted data transfer
- changing IP during session
- assignment of IP to new user