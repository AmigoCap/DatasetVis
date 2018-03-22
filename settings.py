#Path to the dataset you want to use to train and test the convolutional neural network
databasePath = '../Dataset'
#Size of the resized square images
size = 32
#Part of the dataset you want to test the model
offset_test = 0.1
#Part of the dataset to train the model, the other part to cross validation
offset_train_val = 0.8
#Number of iterations on your training dataset
nb_epoch = 100
#Total number of training examples present in a single batch.
batch_size = 256
#Gradient descent parameter, to calculate the gradient loss function more frequently or not
learning_rate = 0.001
#Strictness of classification : an image is attributed to a class if its score > x * (1/nb class)  (random classification score)
strictness_class = 1.3
#The number of convolutional network
nb_filter = 32
#Size of filters
filter_size = 5
#Choose the network in the reseau.py script
reseau = 1