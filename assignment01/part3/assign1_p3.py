#Assignment 1 - Question 3      Akshit Arora
#Implementing logistic regression using perceptron learning rule.
#Given the error, determine the setting (learningRate, batch/minibatch/online) with minimal sweeps.

#Additional notes:
#not a vectorized implementation!

from numpy import *
from math import *
import matplotlib.pyplot as plt
#from mpl_toolkits.mplot3d import Axes3D

#fig = plt.figure()
#ax = fig.add_subplot(111, projection='3d')

NUMITR = 1000
ERROR = arange(NUMITR, dtype=float)
W1 = arange(NUMITR, dtype=float)
W2 = arange(NUMITR, dtype=float)
B = arange(NUMITR, dtype=float)

def h_theta_x(w1,x1,w2,x2,b):
    var = (1 / (1 + e**(- w1*x1 - w2*x2 - b)))
    if var >= 0.5:
        return 1.0
    else:
        return 0.0

def h_theta_x1(w1,x1,w2,x2,b):
    return (1 / (1 + e**(- w1*x1 - w2*x2 - b)))

def cost(w1,x1,w2,x2,b,y):
    h = h_theta_x1(w1,x1,w2,x2,b)
    return (-y * log(h) - (1-y) * log(1-h))

def error(w1, w2, b, points):
    totalError = 0
    for i in range(0, len(points)):
        x1 = points[i, 0]
        x2 = points[i, 1]
        y = points[i, 3]
        #totalError += (y - (w1 * x1 + w2 * x2 + b)) ** 2
        totalError += cost(w1,x1,w2,x2,b,y)
    return totalError / float(len(points))

def step_gradient(b_current, w1_current, w2_current, points, learningRate):
    b_gradient = 0
    w1_gradient = 0
    w2_gradient = 0
    N = float(len(points))
    for i in range(0, len(points)):
        x1 = points[i, 0]
        x2 = points[i, 1]
        y = points[i, 3]
        b_gradient += -(1/N) * (y - ( h_theta_x(w1_current,x1,w2_current,x2,b_current) ))
        w1_gradient += -(1/N) * x1 * (y - ( h_theta_x(w1_current,x1,w2_current,x2,b_current) ))
        w2_gradient += -(1/N) * x2 * (y - ( h_theta_x(w1_current,x1,w2_current,x2,b_current) ))
    new_b = b_current - (learningRate * b_gradient)
    new_w1 = w1_current - (learningRate * w1_gradient)
    new_w2 = w2_current - (learningRate * w2_gradient)
    return [new_b, new_w1, new_w2]

def gradient_descent_runner(points, starting_w1, starting_w2, starting_b, learning_rate, num_iterations):
    b = starting_b
    w1 = starting_w1
    w2 = starting_w2
    for i in range(num_iterations):
        random.shuffle(points)
        [b, w1, w2] = step_gradient(b, w1, w2, array(points), learning_rate)
        ERROR[i] = error(w1,w2,b,points)
        W1[i] = w1
        W2[i] = w2
        B[i] = b
    #this is the part where we change in order to account for regular patterns in jittering!
    '''
    we know that regular patterns appear. We spot that first such pattern appears between 170 and 300! (before 170 it is all irregular pattern)
    We just need to look at the Error[170:300] and take the minimum error position (say, t). Then simply get B[t], W1[t] and W2[t] and that would be the answer.

    But, it looks like there is another dip (in the irregular pattern before 170) in the very beginning around x = 10. So, including index 5 to 300 to find the minimum.
    '''
    t = where(ERROR == ERROR[5:300].min())
    w1 = W1[t]
    w2 = W2[t]
    b = B[t]
    #that's it!

    return [w1, w2, b, t]

def run():

    #Step 1 - collect our data in the form of ndarray
    points = genfromtxt('assign1_data.txt')
    points = delete(points, (0), axis=0)

    #Step 2 - define our hyperparameters
    learning_rate = 0.0001
    #y = w1 * x1 + w2 * x2 + b
    initial_w1 = 0
    initial_w2 = 0
    initial_b = 0
    num_iterations = NUMITR

    #Step 3 - train our model
    print 'starting batch gradient descent at w1 = {0}, w2 = {1}, b = {2}, error = {3}'.format(initial_w1,initial_w2, initial_b,error(initial_w1, initial_w2, initial_b, points))
    print "Running..."
    [w1, w2, b, t] = gradient_descent_runner(points, initial_w1, initial_w2, initial_b, learning_rate, num_iterations)
    print "After {0} iterations w1 = {1}, w2 = {2}, b = {3}, error w.r.t. whole data set (for comparison) = {4}".format(num_iterations, w1, w2, b, error(w1, w2, b, points))
    plt.plot(ERROR) #working!
    plt.xlabel('Total number of epochs')
    plt.ylabel('Error')
    print "Total iterations (number of times gradient_step was executed):" + str(len(ERROR) * len(points))
    print "Total epochs:" + str(NUMITR)
    print "SAMPLED AT: " + str(t)
    plt.title('Batch Logistic Regression (learning rate:' + str(learning_rate) + ')')
    #ax.scatter(W1,W2,ERROR) #working!
    #not able to get error surface properly though.
    plt.show()

if __name__ == '__main__':
    run()
