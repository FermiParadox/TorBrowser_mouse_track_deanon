# Attack summary 

When a Tor user switches tabs 
(to another Tor tab or to his clearnet browser)
his sessions can be linked from the mouse entry-exit points. 

This attack has two variants:

### Attack 1: Tor Browser plus normal browser

![deanon_attack_1](https://user-images.githubusercontent.com/10809024/160258389-48e2d156-a7e6-46c8-8bc2-89920f118751.gif)

Users can have their Tor Browser activity linked to their non-Tor IP by:

- moving the mouse from Tor Browser to another non-Tor browser (and vice versa)
- switching said browsers with hotkeys 




### Attack 2: only Tor Browser, with multiple tabs opened
There's another vulnerability involving the use of only Tor Browser.

Tor Browser has separate exit nodes (and IPs) for each tab. 
However, switching tabs with hotkeys creates a unique pattern,
meaning all opened websites (despite being opened on separate tabs) 
can be attributed to the same user.

![deanon_attack_2](https://user-images.githubusercontent.com/10809024/160257165-07ee4ffe-9d57-4e4e-8558-2131c8573148.gif)


# Test results
I tested it on my PC:

 - It is **very accurate in Tor-to-normal**, but less so 
due to speed. It can be further improved by projecting 
the mouse track on the border of the browser.

![image](https://user-images.githubusercontent.com/10809024/147254027-6cbc6f85-d82b-4ed8-9834-6c5912920dfd.png)

 - The match is **extremely accurate** when using **CTR TAB in Tor** 
(that is, only one browser). Note that both fingerprints are drawn on top of each other (3rd graph), since they are completely identical. 

![image](https://user-images.githubusercontent.com/10809024/147253839-c1d2413f-2e31-4b3b-bd1b-fe2a75824812.png)



This has to be tested with data from users 
that don't know of the attack (to prevent mouse movement biases).   
Also, it has to be independently verified by other researchers,
although I doubt there's anything that makes the attack infeasible. 

### TorProject had been notified prior to release
Update to their documentation:    
["Discourage more running a browser in parallel to Tor Browser"](https://gitlab.torproject.org/tpo/web/support/-/issues/280)


# Preconditions
1. JavaScript must be enabled on both browsers.
2. Websites must collect mouse x,y,time data.
3. Websites must share that data with each other.

Big tech is *already sharing data* for anti-fraud purposes, etc. 
[GIFTCT](https://gifct.org/about/story/#june-26--2017---formation-of-gifct)
Whether it's x,y,time I don't know.

Also, Google Tag Manager (used by [~18 million websites](https://trends.builtwith.com/websitelist/Google-Tag-Manager))
or similar 3rd parties could be gathering such data (haven't confirmed it yet).
If such data is indeed gathered in one place,
then whoever has access to it can use this attack.

# Metrics analysed
The following metrics are compared between users 
when they are within a specified time difference. 

Mouse movement close to entry and exit locations: 

- **x, y**, **time**
- **angle**
- **speed**
- **acceleration**

Due to [time granulation in Tor at 100ms](https://gitlab.torproject.org/legacy/trac/-/issues/1517) 
speed and acceleration can't be calculated in a traditional way.
A way around this is deducing the elapsed time based on 
density of registered points. The storage of x-y values seems to be following 
the speed pattern of my mouse movements. 

However, delays due to other simultaneous 
browser events perhaps will affect it.

### TorBrowser CTR TAB metrics
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
To reduce false positives smaller 
thresholds can be used for all metrics. 

Also, the distance comparison of critical points 
(that is, suspected exit or entry points) can be calculated 
while taking into account speed and acceleration.

# How to run it
- Install dependencies:   
```pip install -r requirements.txt```

## Try it locally:
(using only a normal browser):

1. edit the config file to allow pair matching between non-Tor browsers:
   ```python 
   PAIR_MUST_INCLUDE_TOR = False
   ```
2. run in terminal: 
   ```bash
   gunicorn -w 4 -b 0.0.0.0:65000 app:app
   ```
3. Open http://0.0.0.0:65000/ on two windows (not maximized)
4. move mouse from one window into the other
5. or alt-tab and move it
6. ... until matches are plotted (automatically)

### TorBrowser plus clearnet browser:

> ⚠️ WARNING ⚠️     
This exposes your server to the outside-world.  
**No** guarantees it's suitable for production. 


1. port-forward port 65000 in your router (or any other unused port)
2. find your IP
3. visit `<your-IP>:65000` through TorBrowser
4. visit `<your-IP>:65000` through clearnet browser
5. move mouse from one browser into the other until fingerprints appear

When finished you should undo the forwarding. 

### TorBrowser

> ⚠️ WARNING ⚠️   
This exposes your server to the outside-world.  
**No** guarantees it's suitable for production. 

1. port-forward port 65000 in your router (or any other unused port)
2. find your IP
3. visit `<your-IP>:65000` through TorBrowser _only_
4. open `<your-IP>:65000` on a 2nd tab in TorBrowser
5. press <kbd>CTR TAB</kbd> to switch tabs, and move mouse
6. repeat until fingerprints appear

When finished you should undo the forwarding. 



# Bug - Crashes
It sometimes crashes 
(when specific mouse-tracks are stored in a browser tab session). 

Avoid ultra-fast mouse-speed; I think registering only 2 points in a browser 
due to fast mouse-speed causes it to permanently crash.

Workaround: 
1. close the tabs
2. restart the program 
3. open _new_ tabs.



# Software limitations 

This is simply a proof of concept.   

I haven't taken into account all scenarios, e.g.: 
- user moving one of the browsers
- user trying to deceive the server by manipulating data
- interrupted data transfer
- changing IP during session
- assignment of existing IP to new user
- accuracy (false positives and false negatives)

The above could make the attacks a bit harder.   
But a more sophisticated software would overcome them.

# Investigate later
- Can single-browser single-tab metrics be used to extract patterns 
related to a user's UI layout (location of shortcuts on desktop, etc.)?
