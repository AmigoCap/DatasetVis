from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.conv import conv_2d, max_pool_2d, avg_pool_2d
from tflearn.layers.estimator import regression
from tflearn.data_preprocessing import ImagePreprocessing
from tflearn.data_augmentation import ImageAugmentation
import tflearn
import settings
import loadData as ld

def getReseau():
    size = settings.size
    nb_filter = settings.nb_filter
    filter_size = settings.filter_size

    # Make sure the data is normalized
    img_prep = ImagePreprocessing()
    img_prep.add_featurewise_zero_center()
    img_prep.add_featurewise_stdnorm()

    # Create extra synthetic training data by flipping, rotating and blurring the
    # images on our data set.
    img_aug = ImageAugmentation()
    img_aug.add_random_flip_leftright()
    img_aug.add_random_rotation(max_angle=25.)
    img_aug.add_random_blur(sigma_max=3.)

    # Define our network architecture:

    # Input is a 32x32 image with 3 color channels (red, green and blue)
    network = input_data(shape=[None, size, size, 3],
                         data_preprocessing=img_prep,
                         data_augmentation=img_aug)

    reseau = settings.reseau

    if reseau == 1:
        # Step 1: Convolution
        network = conv_2d(network, nb_filter, filter_size, activation='relu')

        # Step 2: Max pooling
        network = max_pool_2d(network, 2)

        # Step 3: Convolution again
        network = conv_2d(network, nb_filter * 4, filter_size, activation='relu')

        # Step 4: Convolution yet again
        network = conv_2d(network, nb_filter * 4, filter_size, activation='relu')

        # Step 5: Max pooling again
        network = max_pool_2d(network, 2)

        # Step 6: Fully-connected 512 node neural network
        network = fully_connected(network, nb_filter * 16, activation='relu')

        # Step 7: Dropout - throw away some data randomly during training to prevent over-fitting
        network = dropout(network, 0.5)


    elif reseau == 2:
        network = conv_2d(network, 32, 3, activation='relu')
        network = conv_2d(network, 32, 3, activation='relu')
        network = max_pool_2d(network, 2)
        network = conv_2d(network, 32, 3, activation='relu')
        network = conv_2d(network, 32, 3, activation='relu')
        network = max_pool_2d(network, 2)
        network = fully_connected(network, 512, activation='relu')
        network = fully_connected(network, 512, activation='relu')

    elif reseau == 3:
        network = conv_2d(network, 32, 3, activation='relu')
        network = avg_pool_2d(network, 2)
        network = conv_2d(network, 32, 3, activation='relu')
        network = avg_pool_2d(network, 2)
        network = conv_2d(network, 32, 3, activation='relu')
        network = avg_pool_2d(network, 2)
        network = fully_connected(network, 512, activation='relu')
        network = fully_connected(network, 512, activation='relu')
        network = dropout(network, 0.5)

    elif reseau == 4:
        network = conv_2d(network, 32, 3, activation='relu')
        network = conv_2d(network, 32, 3, activation='relu')
        network = conv_2d(network, 32, 5, padding='valid', activation='relu')
        network = conv_2d(network, 32, 3, activation='relu')
        network = conv_2d(network, 32, 3, activation='relu')
        network = conv_2d(network, 32, 5, padding='valid', activation='relu')
        network = fully_connected(network, 512, activation='relu')
        network = dropout(network, 0.5)

    elif reseau == 5:
        network = conv_2d(network, 64, 3, activation='relu')
        network = conv_2d(network, 64, 3, activation='relu')
        network = avg_pool_2d(network, 2)
        network = conv_2d(network, 32, 3, activation='relu')
        network = conv_2d(network, 32, 3, activation='relu')
        network = max_pool_2d(network, 2)
        network = fully_connected(network, 512, activation='relu')
        network = fully_connected(network, 512, activation='relu')

    # Step 8: Fully-connected neural network with three outputs (0=isn't a bird, 1=is a bird) to make the final prediction
    network = fully_connected(network, ld.getLabelsNumber(), activation='softmax')

    # Tell tflearn how we want to train the network
    network = regression(network, optimizer='adam',
                         loss='categorical_crossentropy',
                         learning_rate=settings.learning_rate)

    # Wrap the network in a model object
    # model = tflearn.DNN(network, tensorboard_verbose=0, checkpoint_path='dataviz-classifier.tfl.ckpt')
    model = tflearn.DNN(network,
                        tensorboard_verbose=0)  # , checkpoint_path='data-classifier/dataviz-classifier.tfl.ckpt')

    return model