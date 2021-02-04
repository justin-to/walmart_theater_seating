Walmart Theater Seating Challenge

Language used: 
Python

This program takes seating reservations from a file by reading input line by line and outputs the seating arrangements 
associated with the respective reservation in another file, the full path to that file is printed to the terminal.

Installation:
Install python and modify the device's Path environment variables such that it points to the installed python package.

Usage:
python main.py [input]
Input needs to be the full path to the file.

Assumptions:
Customer safety, the buffer around reservations, is top priority so no compromising on that to fit more people.
Customer satisfaction quantified by having further seats from the screen as well as seating as many people possible (in 
the order they made the reservation).
All the reservations do not require a seat.
Buffer for seating for one row and three columns over is 
 __________
|sbbbbbbbss|
|sbbbtbbbss|
|sbbbbbbbss|
where 'b' represents the buffer, 't' is the taken seat, and 's' is an open seat.

Future Considerations:
Closer to the center of a row increases satisfaction, audio balance and non-warped viewing experience.
Best theater seats are in the center seats of rows 2/3 of the way back, so start from the center and work outwards.
Allow for splitting up of groups
|sbbbbbbbbs|
|sbbbggbbbs|
|sbbbggbbbs|
Buffer is smaller diagonally
 __________
|ssbbbbbsss|
|sbbbtbbbss|
|ssbbbbbsss|
Order of reservations does not matter, we could try and maximize satisfaction with larger groups getting good seats
to minimize buffering of good seats.
Find a clever way to generate buffers for each customer.