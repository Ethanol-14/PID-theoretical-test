import turtle
import random
import keyboard
import time

Lcurrent = 10
Rcurrent = 10

LcurrentOffset = 0.2
RcurrentOffset = 0
LcurrentError = 0
RcurrentError = 0
LcurrentErrorMax = 2
RcurrentErrorMax = 2

LaccelerationLag = 0.9
RaccelerationLag = 0.9
LdeccelerationLag = 0.5
RdeccelerationLag = 0.5

Lvelocity = 0
Rvelocity = 0

Lsensor = 0
Rsensor = 0
previousLsensor = 0
previousRsensor = 0

error = 0
previousError = 0

cumulativeError = 0
previousCumulativeError = 0
LsensorError = 0
RsensorError = 0
LsensorErrorMax = 0
RsensorErrorMax = 0

previousErrorDifference = 0;

target = 600

dTime = 0

Kp = 1
Ki = 0
Kd = 0.1

turtle.speed(0)
turtle.hideturtle()

def graph(deltaT, preDeltaT, x1, prex1, offsetX, offsetY, color):
    turtle.up()
    turtle.pencolor(color)
    turtle.goto(preDeltaT+offsetX, prex1+offsetY)
    turtle.down()
    turtle.goto(deltaT+offsetX, x1+offsetY)
    turtle.up()

#Blue line is Lsensor, red line is Rsensor
#L shall be the master, R shall be the follower
turtle.tracer(0, 0)

while True:
    turtle.clear()
    Lvelocity = 0
    Rvelocity = 0
    Lsensor = 0
    Rsensor = 0
    previousLsensor = 0
    previousRsensor = 0
    error = 0
    previousError = 0
    cumulativeError = 0
    previousCumulativeError = 0
    previousErrorDifference = 0
    dTime = 0

    graph(-400, 400, 0, 0, 0, 0, "black")
    graph(-400, -400, -400, 400, 0, 0, "black")

    while Lsensor < target or Rsensor < target:

        LcurrentError = random.randint(0, LsensorErrorMax)-(LsensorErrorMax/2)
        RcurrentError = random.randint(0, RsensorErrorMax)-(RsensorErrorMax/2)

        LsensorError = random.randint(0, LcurrentErrorMax)-(LcurrentErrorMax/2)
        RsensorError = random.randint(0, RcurrentErrorMax)-(RcurrentErrorMax/2)

        Rcurrent = Lcurrent + (error * Kp) + (cumulativeError * Ki) + (previousErrorDifference * Kd)

        if Lcurrent > Lvelocity:
            Lvelocity = ((Lvelocity-(Lcurrent+LcurrentError+LcurrentOffset))*LaccelerationLag)+(Lcurrent+LcurrentError+LcurrentOffset)
        else:
            Lvelocity = ((Lvelocity-(Lcurrent+LcurrentError+LcurrentOffset))*LdeccelerationLag)+(Lcurrent+LcurrentError+LcurrentOffset)
            
        if Rcurrent > Rvelocity:
            Rvelocity = ((Rvelocity-(Rcurrent+RcurrentError+RcurrentOffset))*RaccelerationLag)+(Rcurrent+RcurrentError+RcurrentOffset)
        else:
            Rvelocity = ((Rvelocity-(Rcurrent+RcurrentError+RcurrentOffset))*RdeccelerationLag)+(Rcurrent+RcurrentError+RcurrentOffset)

        previousError = error
        
        Lsensor += Lvelocity + LsensorError
        Rsensor += Rvelocity + RsensorError
        
        error = Lsensor - Rsensor
        cumulativeError += Lsensor - Rsensor
        
        if Lsensor >= target:
            Lsensor = target
        if Rsensor >= target:
            Rsensor = target

        #graph lines
        graph(dTime*10, (dTime-1)*10, Lsensor, previousLsensor, -400, -300, "blue")
        graph(dTime*10, (dTime-1)*10, Rsensor, previousRsensor, -400, -300, "red")
        
        graph(dTime*10, (dTime-1)*10, error*4, previousError*4, -400, 0, "green")
        graph(dTime*10, (dTime-1)*10, cumulativeError*4, previousCumulativeError*4, -400, 0, "purple")
        graph(dTime*10, (dTime-1)*10, (error - previousError)*4, previousErrorDifference*4, -400, 0, "orange")

        previousLsensor = Lsensor
        previousRsensor = Rsensor
        
        previousErrorDifference = (error - previousError)

        previousError = error
        previousCumulativeError = cumulativeError

        dTime += 1

    turtle.update()

    while not keyboard.is_pressed("a"):
        time.sleep(0.05)
    time.sleep(0.05)
    