# Package imports
import os
import sys
import matplotlib.pyplot as plt
import numpy as np
import sklearn
import sklearn.datasets
import sklearn.linear_model
import matplotlib

# number of hidden units
nn_hdim = int(sys.argv[1])

# dat set size
dsize = int(sys.argv[2])

# iteration count
it_count = int(sys.argv[3])

# learning rate
epsilon = float(sys.argv[4])


# validation
use_validation_data = True

# Generate a dataset
#noise_level = 0.20
noise_level = 0.01
vlo = 100
vup = vlo + dsize / 5
vsize = vup - vlo
print "trainig data size %d" %(vsize)
np.random.seed(0)
XC, yc = sklearn.datasets.make_moons(dsize, noise=noise_level)

print "complete data set generated"
def print_array(X,y):
	for row in X:
		print(row)
	for row in y:
		print(row)
		

# Generate a validation dataset
#np.random.seed(0)
#XV, yv = sklearn.datasets.make_moons(40, noise=0.20)
#print "validation data set generated"

XV = XC[vlo:vup:1]
yv = yc[vlo:vup:1]
print "validation data generated"
#print_array(XV, yv)

X = np.delete(XC, np.s_[vlo:vup:1], 0)
y = np.delete(yc, np.s_[vlo:vup:1], 0)
print "training data generated"
#print_array(X, y)

	
# Parameters
num_examples = len(X) # training set size
nn_input_dim = 2 # input layer dimensionality
nn_output_dim = 2 # output layer dimensionality

# Gradient descent parameters (I picked these by hand)
#epsilon = 0.01 # learning rate for gradient descent
reg_lambda = 0.01 # regularization strength 

		
# Helper function to evaluate the total loss on the dataset
def calculate_loss(X,y,model):
    W1, b1, W2, b2 = model['W1'], model['b1'], model['W2'], model['b2']
    size = len(X)
    
    # Forward propagation to calculate our predictions
    z1 = X.dot(W1) + b1
    a1 = np.tanh(z1)
    z2 = a1.dot(W2) + b2
    exp_scores = np.exp(z2)
    probs = exp_scores / np.sum(exp_scores, axis=1, keepdims=True)
    
    # Calculating the loss
    corect_logprobs = -np.log(probs[range(size), y])
    data_loss = np.sum(corect_logprobs)
    
    # Add regulatization term to loss (optional)
    data_loss += reg_lambda/2 * (np.sum(np.square(W1)) + np.sum(np.square(W2)))
    return 1./size * data_loss
    
    
# Helper function to predict an output (0 or 1)
def predict(model, x):
    W1, b1, W2, b2 = model['W1'], model['b1'], model['W2'], model['b2']
    
    # Forward propagation
    z1 = x.dot(W1) + b1
    a1 = np.tanh(z1)
    z2 = a1.dot(W2) + b2
    exp_scores = np.exp(z2)
    probs = exp_scores / np.sum(exp_scores, axis=1, keepdims=True)
    return np.argmax(probs, axis=1)

# This function learns parameters for the neural network and returns the model.
# - nn_hdim: Number of nodes in the hidden layer
# - num_passes: Number of passes through the training data for gradient descent
# - print_loss: If True, print the loss every 1000 iterations
def build_model(nn_hdim, num_passes=10000, validation_interval=50):    
    # Initialize the parameters to random values. We need to learn these.
	np.random.seed(0)
	W1 = np.random.randn(nn_input_dim, nn_hdim) / np.sqrt(nn_input_dim)
	b1 = np.zeros((1, nn_hdim))
	W2 = np.random.randn(nn_hdim, nn_output_dim) / np.sqrt(nn_hdim)
	b2 = np.zeros((1, nn_output_dim))

    # This is what we return at the end
	model = {}
    
    # Gradient descent. For each batch...
	loss = -1.0
	for i in xrange(0, num_passes):
		#print "pass %d" %(i)
		
		# Forward propagation
		z1 = X.dot(W1) + b1
		a1 = np.tanh(z1)
		z2 = a1.dot(W2) + b2
		exp_scores = np.exp(z2)
		probs = exp_scores / np.sum(exp_scores, axis=1, keepdims=True)

        # Back propagation
		delta3 = probs
		delta3[range(num_examples), y] -= 1
		dW2 = (a1.T).dot(delta3)
		db2 = np.sum(delta3, axis=0, keepdims=True)
		delta2 = delta3.dot(W2.T) * (1 - np.power(a1, 2))
		dW1 = np.dot(X.T, delta2)
		db1 = np.sum(delta2, axis=0)

        # Add regularization terms (b1 and b2 don't have regularization terms)
		dW2 += reg_lambda * W2
		dW1 += reg_lambda * W1

        # Gradient descent parameter update
		W1 += -epsilon * dW1
		b1 += -epsilon * db1
		W2 += -epsilon * dW2
		b2 += -epsilon * db2
        
        # Assign new parameters to the model
		model = { 'W1': W1, 'b1': b1, 'W2': W2, 'b2': b2}
        
        # This is expensive because it uses the whole dataset, so we don't want to do it too often.
		if i % validation_interval == 0:
			if use_validation_data:
				cur_loss = calculate_loss(XV,yv,model)
			else:
				cur_loss = calculate_loss(X,y,model)
				
			print "Loss after iteration %i: %.8f" %(i, cur_loss)
			loss = cur_loss
    
		
	return model
    
# Build a model with a 3-dimensional hidden layer
model = build_model(nn_hdim, num_passes=it_count, validation_interval=1)

print "hidden layer"
for row in model['W1']:
	print(row)

print "hidden layer bias"
for row in model['b1']:
	print(row)

print "output layer"
for row in model['W2']:
	print(row)

print "output layer bias"
for row in model['b2']:
	print(row)
    
    