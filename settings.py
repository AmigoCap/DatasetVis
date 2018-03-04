#Path to the dataset you want to use to train and test the convolutional neural network
databasePath = '../Dataset'
#Size of the reisized square images
size = 64
#Part of the dataset you want to test the model
offset_test = 0.1
#Part of the dataset to train the model, the other part to cross validation
offset_train_val = 0.7
#Number of iterations on your training dataset
nb_epoch = 80
#Total number of training examples present in a single batch.
batch_size = 32
#Gradient descent parameter, to calculate the gradient loss function more frequently or not
learning_rate = 0.001
