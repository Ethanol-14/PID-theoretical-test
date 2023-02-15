import turtle
import random

Lcurrent = 10
Rcurrent = 10

LcurrentOffset = 0.5
RcurrentOffset = 0
LcurrentError = 0
RcurrentError = 0
LcurrentErrorMax = 2
RcurrentErrorMax = 2

LaccelerationLag = 0.9
RaccelerationLag = 0.9
LdeccelerationLag = 0.3
RdeccelerationLag = 0.3

Lvelocity = 0
Rvelocity = 0

Lsensor = 0
Rsensor = 0
previousLsensor = Lsensor
previousRsensor = Rsensor

displacementError = 0
previousDisplacementError = 0

cumulativeError = 0
previousCumulativeError = 0
LsensorError = 0
RsensorError = 0
LsensorErrorMax = 1
RsensorErrorMax = 1

target = 600

time = 0

Kp = 0.4
Ki = 0.04
Kd = 0

turtle.speed(0)
turtle.hideturtle()

def graph(deltaT, preDeltaT, x1, prex1, offsetX, offsetY, color):
    turtle.up()
    turtle.pencolor(color)
    turtle.goto(preDeltaT+offsetX, prex1+offsetY);
    turtle.down()
    turtle.goto(deltaT+offsetX, x1+offsetY);
    turtle.up()

#Blue line is Lsensor, red line is Rsensor
#L shall be the master, R shall be the follower
turtle.tracer(1, 0)

graph(-400, 400, 0, 0, 0, 0, "black")
graph(-400, -400, -400, 400, 0, 0, "black")

while Lsensor < target or Rsensor < target:

    LcurrentError = random.randint(0, LsensorErrorMax)-(LsensorErrorMax/2)
    RcurrentError = random.randint(0, RsensorErrorMax)-(RsensorErrorMax/2)

    LsensorError = random.randint(0, LcurrentErrorMax)-(LcurrentErrorMax/2)
    RsensorError = random.randint(0, RcurrentErrorMax)-(RcurrentErrorMax/2)

    Rcurrent = Lcurrent + (displacementError * Kp) + (cumulativeError * Ki) + (Kd)

    if Lcurrent > Lvelocity:
        Lvelocity = ((Lvelocity-(Lcurrent+LcurrentError+LcurrentOffset))*LaccelerationLag)+(Lcurrent+LcurrentError+LcurrentOffset)
    else:
        Lvelocity = ((Lvelocity-(Lcurrent+LcurrentError+LcurrentOffset))*LdeccelerationLag)+(Lcurrent+LcurrentError+LcurrentOffset)
        
    if Rcurrent > Rvelocity:
        Rvelocity = ((Rvelocity-(Rcurrent+RcurrentError+RcurrentOffset))*RaccelerationLag)+(Rcurrent+RcurrentError+RcurrentOffset)
    else:
        Rvelocity = ((Rvelocity-(Rcurrent+RcurrentError+RcurrentOffset))*RdeccelerationLag)+(Rcurrent+RcurrentError+RcurrentOffset)

    print("\nLV: "+str(Lvelocity))
    print("RV: "+str(Rvelocity))
    
    Lsensor += Lvelocity + LsensorError
    Rsensor += Rvelocity + RsensorError
    
    displacementError = Lsensor - Rsensor
    cumulativeError += Lsensor - Rsensor
    
    if Lsensor >= target:
        Lsensor = target
    if Rsensor >= target:
        Rsensor = target

    #graph lines
    graph(time*10, (time-1)*10, Lsensor, previousLsensor, -400, -300, "blue")
    graph(time*10, (time-1)*10, Rsensor, previousRsensor, -400, -300, "red")
    
    graph(time*10, (time-1)*10, displacementError, previousDisplacementError, -400, 0, "green")
    graph(time*10, (time-1)*10, cumulativeError, previousCumulativeError, -400, 0, "purple")

    previousLsensor = Lsensor
    previousRsensor = Rsensor
    
    previousDisplacementError = displacementError
    previousCumulativeError = cumulativeError

    time += 1

turtle.update()
turtle.exitonclick()