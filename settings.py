#Path to the dataset you want to use to train and test the convolutional neural network
import time

databasePath = '/Users/alexis/Documents/GitHub/Dataset'

#Size of the reisized square images
size = 64
#Part of the dataset you want to test the model
offset_test = 0.1
#Part of the dataset to train the model, the other part to cross validation
offset_train_val = 0.7
#Number of iterations on your training dataset
nb_epoch = 100
#Total number of training examples present in a single batch.
batch_size = 256
#Gradient descent parameter, to calculate the gradient loss function more frequently or not
learning_rate = 0.001
#Strictness of classification : an image is attributed to a class if its score > x * (1/nb class)  (random classification score)
strictness_class = 1.3


nb_filter = 32
filter_size = 3
reseau = 1
