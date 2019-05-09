#!/usr/bin/env python
import math
#from particles import Robot
import particles as Robot
 
 
 
def main():
    print 'In main'
 
    bob = Robot.Robot()
    bob.set(30, 50, math.pi/2)
    print bob.to_string()
 
    bob = bob.move(-math.pi/2.0, 15)
 
    bobCents = bob.sense()
    print bobCents
 
    bob = bob.move(-math.pi/2.0, 10)
    bobCents = bob.sense()
    print bobCents
 
    bob.set_noise(5.0, 0.1, 5.0)#sigma value for moving forward, turning in place and sensor value respectively
    print 'noise set:'

    bob.set(30, 50, math.pi/2)
    bob = bob.move(-math.pi/2.0, 15)
    bobCents = bob.sense()
    print bobCents
    bob = bob.move(-math.pi/2.0, 10)
    bobCents = bob.sense()
    print bobCents

    main_robot = Robot.Robot()
    main_robot.set_noise(0.05, 0.05, 5.0)
    num_particles = 1000
    turns = [0.1, 0.0, 0.0, 0.3, 0.5]
    forwards = [5.0, 5.0, 2.5, 3.0, 5.0]
   
    partArr = []
    for n in range(num_particles):
       	bob= Robot.Robot()
        bob.set_noise(0.05, 0.05, 5.0)
        partArr.append(bob)
 
    for i in range(len(turns)):
 
        for particle in partArr:
            particle = particle.move(turns[i], forwards[i])
 
        weightArr = []
        for particle in partArr:
            weight = main_robot.measurement_prob(particle.sense())
            weightArr.append(weight)
 

        partArr = Robot.resample(partArr, weightArr)
 
        main_robot = partArr[ weightArr.index(max(weightArr)) ]
 
        print 'most likey particle: '+ main_robot.to_string()
        print 'average error in set: ' + str(Robot.eval_set(main_robot, partArr))
 
 
if __name__ == '__main__':
    main()
