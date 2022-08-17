"""
SignalProcesseing for Exercises for ww19
"""
import collections
import random

real_val = 4
max_noi = 1
buffer = collections.deque(maxlen=12)
res = []
resErrs = []


def getNoisy(real_value,max_noise): # This function makes fake noise, and returns it.
    rv = real_value # Shorthands our input to a new internal variable
    mn = max_noise # Shorthands our input to a new internal variable

    noise_value = rv + random.randrange(-mn,mn+1) # Makes some noise by selecting a number in the range of negative to positive max_noise value.

    return(noise_value)


def getMean(value): # This function calculates an avg from a range of numbers, and returns the avg.
    lon = value # Shorthands our input to a new internal variable
    count = 0 # Instantiates a counter variable as an int
    totallon = 0.0 # Instantiate our Total list of numbers as an float

    for num in lon:
        count += 1 # Our counter
        totallon += num # Here we add the numbers together

    avg_num = totallon/count # Here we calulate or average

    return(avg_num)

for x in range(1,13): #First we fill up the buffer
    buffer.append( getNoisy(real_val,max_noi) ) # Here we feed our noise function with data and returns noise to the buffer list.

for x in range(1,21): #Then we append new values to the buffer and add each of the avg's to a new list, this way we get a Moving Average.
    buffer.append( getNoisy(real_val,max_noi) ) # Here we again feed our noise function with data and returns noise to the buffer list.
    res.append(getMean(buffer)) # Here we take the avg of our whole buffer and puts the value in the a new list, this is our Moving Average.

print("Res list:",res, "\n") #Prints the moving average values

"""
# Calculation of the errors

## Notes
> *The Exercise menstions using resErrs[0] = abs(res[0] - 4)*

Using resErrs[0] = abs(res[0] - 4) to get the avg of a list makes little sense, 
given that it is essencly a static number because it is being place in to the first position of the list each time, and not appended.

Not that appending alone makes sense either when the absolut number of res is allways the same, 
given it's the absolute of only the first number in the list.
"""

for x in res: # Here we messure the error values.
    resErrs.append(abs(x - 4)) # Here is what i came up with in order to get the result described in the exercise.

print("Avg ResError:",getMean(resErrs)) # Here we print out the avg error value.
