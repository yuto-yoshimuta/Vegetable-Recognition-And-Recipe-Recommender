# Import necessary libraries from TensorFlow and Keras
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import ReduceLROnPlateau, EarlyStopping, ModelCheckpoint
from tensorflow.keras.layers import Dense, Flatten, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import Model

# Define paths for training and testing images
train_dir = "../AI/train_imgs/train"
test_dir = "../AI/train_imgs/test"

# Arrange image data generators for training 
train_datagen = ImageDataGenerator( 
    rotation_range=90,          # randomly rotated 0~90 degrees
    width_shift_range=0.2,      #randomly shifted horizontally by up to 20% 
    height_shift_range=0.2,     #vertical shifting
    brightness_range=[0., 0.5], #chaging brightness 0~0.5
    shear_range=0.2,            #shear transformations(max0.2)
    zoom_range=0.2,             #randamly zooming up to 20%
    channel_shift_range=0.2,    #color channels of the image
    fill_mode='nearest',        #adjust a nearest pixel
    horizontal_flip=True,       #flipped horizontally
    vertical_flip=True,         #flipped vertically
    rescale=1./255,             #each pixel is divided by 255
)
    

# Create generators for training datasets
train_generator = train_datagen.flow_from_directory( 
    train_dir,                  #specify the train directory 
    target_size=(221, 221),     #specify the image size
    color_mode="rgb",           #specify the color mode
    batch_size=32,              #specify the batch size
    class_mode='categorical',   #specify the class(categorical:2d)
    shuffle=True                #shuffling 
)

# Arrange image data generators for testing by using keras
valid_datagen = ImageDataGenerator(rescale=1./255)

# Create generators for training datasets
valid_generator = valid_datagen.flow_from_directory(
    test_dir,                  #specify the test directory 
    target_size=(221, 221),     #specify the image size
    color_mode="rgb",           #specify the color mode
    batch_size=32,              #specify the batch size
    class_mode='categorical',   #specify the class(categorical:2d)
    shuffle=True                #shuffling 
)

# Load DenseNet121 model with pre-trained weights
base_model = keras.applications.densenet.DenseNet121(
    include_top=False,          #not using final fully-connected layers to use our images
    weights='imagenet',         #load weights that already trained on the ImageNet dataset
    input_shape=(221, 221, 3)   #specify the shape of the input data(221x221/RGB)
)

# Define callbacks for model training
LR_function = ReduceLROnPlateau(  #reduce the learning rate
    monitor='val_accuracy',       #monitoring the validation accuracy
    patience=3,                   #reduce learning rate if no improvement in specified the number of epoch if 
    verbose=1,                    #showing massage
    factor=0.5,                   #a number or quantity when learning rate decreases
    min_lr=0.000001               #set the lower bound on the learning rate
)

adam = Adam(learning_rate=0.0001) #Adam optimizer
estop = EarlyStopping(
    monitor='loss', #show how many losses has occur
    patience=6      #eary stop when it doesnt improve after running 6 epoch
    ) 

scp = ModelCheckpoint(
    'model_20.h5',                  #the name of model file name
    monitor="val_accuracy",         #moniter the verification accuracy value
    verbose=0,                      #not showing massage
    save_best_only=True,            #only save the best model
    save_weights_only=False,        #save whole model
    mode="auto",                    #choose the best mode with automatic mode
    save_freq="epoch"               #save every epoch
)

# Build the classification head on top of the base model
x = base_model.output                           #output of the model(without its top layer)
x = Flatten()(x)                                #multi-dimensional(base model) to 1D 
x = Dense(2048, activation='relu')(x)           #Add neural network layer with 2048 neurons(relu;allow learn more complex patterns)
x = Dense(1024, activation='relu')(x)           #Add neural network layer with 1024 neurons
x = Dropout(0.5)(x)                             #Apply dropout to the network(prevent overfitting)
predictions = Dense(20, activation='softmax')(x)#20 neurons(softmax:multi-class classification)
model = Model(base_model.input, predictions)    #Create final model(linking predictions layer)

#configure the model for training
model.compile(
    optimizer=adam,                     #specify the optimization algorithm to use
    loss='categorical_crossentropy',    #measure how far off the predictions are from the actual labels
    metrics=['accuracy']                #fraction of images correctly classified
)

# Set the number of validation steps
validation_steps = len(valid_generator)

# Train the model on the training dataset
history = model.fit(
    train_generator,                    #bring training data batchs from train_generator
    epochs=100,                         #number of epochs
    callbacks=[LR_function, estop, scp],#1checking decreasing/2early stop/3save model
    validation_data=valid_generator,    #testing
    validation_steps=validation_steps,  #checking trained 20 classes or not after finish runnning 1 epoch
    workers=10                          #decide processes to run in parallel 
)

# Save the trained model
model.save('model_20.h5')