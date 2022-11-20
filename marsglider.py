######################################################################
# This file copyright the Georgia Institute of Technology
#
# Permission is given to students to use or modify this file (only)
# to work on their assignments.
#
# You may NOT publish this file or make it available to others not in
# the course.
#
######################################################################

#These import statements give you access to library functions which you may
# (or may not?) want to use.
from math import *
from glider import *
import random
import numpy as np

    
# cite from https://gatech.instructure.com/courses/175052/pages/15-importance-weight-answer?module_item_id=1399456
def Gaussian(mu, sigma, x):
    
    # calculates the probability of x for 1-dim Gaussian with mean mu and var. sigma
    return exp(- ((mu - x) ** 2) / (sigma ** 2) / 2.0) / sqrt(2.0 * pi * (sigma ** 2))


def measurement_prob(particle_measurement,sense_noise, measurement):
    
    # calculates how likely a measurement should be
    
    prob = 1.0
    
    prob *= Gaussian(particle_measurement, sense_noise, measurement)
        
    return prob

#end cite code

#This is the function you will have to write for part A. 
#-The argument 'height' is a floating point number representing 
# the number of meters your glider is above the average surface based upon 
# atmospheric pressure. (You can think of this as hight above 'sea level'
# except that Mars does not have seas.) Note that this sensor may be
# slightly nosiy. 
# This number will go down over time as your glider slowly descends.
#
#-The argument 'radar' is a floating point number representing the
# number of meters your glider is above the specific point directly below
# your glider based off of a downward facing radar distance sensor. Note that
# this sensor has random Gaussian noise which is different for each read.

#-The argument 'mapFunc' is a function that takes two parameters (x,y)
# and returns the elevation above "sea level" for that location on the map
# of the area your glider is flying above.  Note that although this function
# accepts floating point numbers, the resolution of your map is 1 meter, so
# that passing in integer locations is reasonable.
#
#
#-The argument OTHER is initially None, but if you return an OTHER from
# this function call, it will be passed back to you the next time it is
# called, so that you can use it to keep track of important information
# over time.
#

def estimate_next_pos(height, radar, mapFunc, OTHER=None):

   particle = 10000
   """ initialization"""
   
   #check whether the particle list is available. If no create a new one
   if OTHER == None:  
       
       particle_list = []
       for n in range(particle):
           temp = glider(random.uniform(-250,250),random.uniform(-250,250),random.uniform(4950,5050),random.uniform(-pi,pi), mapFunc = mapFunc)
           particle_list.append(temp)
   else:
       particle_list = OTHER
    
       
   """weight function"""
   w = []  #weight_list
   p_len = len(particle_list)    

   
   for i in range(p_len):
       particle_mF =  mapFunc(particle_list[i].x,particle_list[i].y)  
       particle_radar = particle_list[i].z  - particle_mF             #particle_to_ground
       particle_list[i].z = height
       w.append(measurement_prob(particle_radar ,random.uniform(1,10), radar))

       
   """standize the weight"""
   s = sum(w)
   w = [k/s for k in w]
   p = max(w)
   max_ = w.index(p)

   """resample""" 
   # # cite from https://gatech.instructure.com/courses/175052/pages/16-resampling?module_item_id=1399458
   p3 = []
   index = int(random.random() * p_len)
   beta = 0.0
   if p_len == particle:
       drop_len = int(p_len * 0.04 * 0.5)
       
   else:
       drop_len = int(p_len * 0.5)
       
   
   for i in range(drop_len):
       beta += random.random() * 2.0 * p
       while beta > w[index]:
           beta -= w[index]
           index = (index + 1) % p_len
       p3.append(particle_list[index])
   particle_list = p3
   #end code
   
   """fuzzing""" 
   for j in range(int(drop_len)):
       
        move = random.random()* particle_list[j].speed
       
        x = particle_list[j].x + cos(particle_list[j].heading + random.uniform(-pi/16 , pi/16))*move
       
        y = particle_list[j].y + sin(particle_list[j].heading + random.uniform(-pi/16 , pi/16))*move
       
        p = glider(x,y,height,random.uniform(-pi/4, pi/4))
       
        particle_list.append(p)
        
   """move and estimate"""     
   sum_x = 0
   sum_y = 0
   optionalPointsToPlot = []
   for i in range(len(particle_list)):
       particle_list[i] = particle_list[i].glide()
       sum_x += particle_list[i].x
       sum_y += particle_list[i].y
       optionalPointsToPlot.append((particle_list[i].x, particle_list[i].y,particle_list[i].heading ))
       
   
   xy_estimate = (sum_x/2/drop_len, sum_y/2/drop_len)

   OTHER = particle_list
   # #example of how to find the actual elevation of a point of ground from the map:
   # actualElevation = mapFunc(5,4)

   # # You must return a tuple of (x,y) estimate, and OTHER (even if it is NONE)
   # # in this order for grading purposes.
   # #
   # xy_estimate = (0,0)  #Sample answer, (X,Y) as a tuple.

   # #TODO - remove this canned answer which makes this template code
   # #pass one test case once you start to write your solution.... 
   # xy_estimate = (391.4400701739478, 1449.5287170970244) 

   # # You may optionally also return a list of (x,y,h) points that you would like
   # # the PLOT_PARTICLES=True visualizer to plot for visualization purposes.
   # # If you include an optional third value, it will be plotted as the heading
   # # of your particle.

   # optionalPointsToPlot = [ (1,1), (2,2), (3,3) ]  #Sample (x,y) to plot 
   # optionalPointsToPlot = [ (1,1,0.5),   (2,2, 1.8), (3,3, 3.2) ] #(x,y,heading)
   
   return xy_estimate, OTHER, optionalPointsToPlot


# This is the function you will have to write for part B. The goal in part B
# is to navigate your glider towards (0,0) on the map steering # the glider 
# using its rudder. Note that the Z height is unimportant.

#
# The input parameters are exactly the same as for part A.

def next_angle(height, radar, mapFunc, OTHER=None):

   #How far to turn this timestep, limited to +/-  pi/8, zero means no turn. 
   particle = 10000
   """ initialization"""
   if OTHER == None:
       
       particle_list = []
       for n in range(particle):
           temp = glider(random.uniform(-250,250),random.uniform(-250,250),random.uniform(4950,5050),random.uniform(-pi,pi))
           particle_list.append(temp)
   else:
       particle_list = OTHER


   """weight function"""         
   w = []
   p_len = len(particle_list)    

   
   for i in range(p_len):
       particle_mF =  mapFunc(particle_list[i].x,particle_list[i].y)
       particle_radar = particle_list[i].z - particle_mF
       particle_list[i].z = height
       w.append(measurement_prob(particle_radar ,random.uniform(1,10), radar))

       

   """standize the weight"""
   s = sum(w)
   w = [k/s for k in w]
   p = max(w)
   max_ = w.index(p)

   """resample"""
   # # cite from https://gatech.instructure.com/courses/175052/pages/16-resampling?module_item_id=1399458
   p3 = []
   index = int(random.random() * p_len)
   beta = 0.0
   if p_len == particle:
       drop_len = int(p_len * 0.2 * 0.5)  # for the first time drop 80% of hte particles
       
   else:
       drop_len = int(p_len * 0.5)    # drop half of the particles, will be made up later after fuzzing
       

   for i in range(drop_len):
       beta += random.random() * 2.0 * p     #resample
       while beta > w[index]:
           beta -= w[index]
           index = (index + 1) % p_len
       p3.append(particle_list[index])
   particle_list = p3
   #end code

   """fuzzing"""
   
   # duplicate the particle list with one random step move
   for j in range(int(drop_len)):
       
        move = random.random()* particle_list[j].speed
       
        x = particle_list[j].x + cos(particle_list[j].heading + random.uniform(-pi/4 , pi/4))*move
       
        y = particle_list[j].y + sin(particle_list[j].heading + random.uniform(-pi/4 , pi/4))*move
       
        p = glider(x,y,height,random.uniform(-pi/4, pi/4))
       
        particle_list.append(p)
        
   """move the particles and estimate the location"""
   sum_x = 0
   sum_y = 0
   optionalPointsToPlot = []
   steering_angle_s = 0
   for i in range(len(particle_list)):
       angle_or = np.arctan2(particle_list[i].y,particle_list[i].x)
       angle_heading = particle_list[i].heading
       steering_angle_p = angle_heading%pi - angle_or , pi/8
       steering_angle_s += steering_angle_p
       steering_angle= steering_angle_s / len(particle_list)

       particle_list[i] = particle_list[i].glide(steering_angle)
     
       optionalPointsToPlot.append((particle_list[i].x, particle_list[i].y))
       


   
   # You may optionally also return a list of (x,y)  or (x,y,h) points that 
   # you would like the PLOT_PARTICLES=True visualizer to plot.
   #
   #optionalPointsToPlot = [ (1,1), (20,20), (150,150) ]  # Sample plot points 
   #return steering_angle, OTHER, optionalPointsToPlot
   OTHER = particle_list
   return steering_angle, OTHER,optionalPointsToPlot

def who_am_i():
    # Please specify your GT login ID in the whoami variable (ex: jsmith123).
    whoami = 'sli809'
    return whoami

