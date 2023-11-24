import pandas as pd #handle data as a pandas data frame
import numpy as np #allows for multi dimensional arrays or input features to be processed
import tensorflow as tf 
from sklearn.preprocessing import LabelEncoder #LabelEncoder processes categorical data and transforms it into numerical data the model can use
from tensorflow.keras.models import Model #use the keras api to develop a multi-output model
from tensorflow.keras.layers import Dense, Input #helps construct model layers
from sklearn.model_selection import train_test_split #split training and testing data
import pickle #saves model for future use

df = pd.read_csv('C:\\Users\\Keerthana\\astrolux\\exploratory data analysis\\mosfet.csv')#Open data frame
df = df.drop(columns=["Lost"])

def y_output(data):
    y1 = np.array(data["LETth"])#value of y1 is the resulting linear energy transfer after radiation testing
    y2 = np.array(data["V/VDSS"])#value of y2 is the maximum voltage a MOSFET is capable of during and after radiation exposure
    return y1, y2

Y1, Y2 = y_output(df) 
Y = np.column_stack((Y1, Y2))#np.column_stack creates a 2D array with the values of y1 and y2

X = df.drop(["LETth", "V/VDSS"], axis=1) 

train_X, test_X, train_Y, test_Y = train_test_split(X, Y, test_size=0.2, random_state=1)
#training and testing is 80% and 20% of the data frame respectively;random_state controls how the data is shuffled during splitting

train_stats = X.describe().transpose() 
#.describe() will provide information on the mean and standard deviation of each input feature; .transpose() flips th rows and columns of the array

def z_score(x, stats): #z-score normalization shows how different a data point is from the mean value, which is shown through standard deviations
    return(x - stats['mean'])/stats['std']

norm_train_X = z_score(train_X, train_stats)#normalize training data
norm_test_X = z_score(test_X, train_stats)#normalize testing data

input_shape = (train_X.shape)#set value of input shape

def multi_out_model(input_shape):#a multi-output model allows for both the LETth and V/VDSS values to be predicted as a function of the input features
    input_layer = tf.keras.Input(shape=input_shape)#input features are fed into the model
    first_dense = tf.keras.layers.Dense(units='128', activation='relu')(input_layer)#first layer is to predict LETth value; 128 nodes are in the layer, with the activation function as ReLu
    y1_output = tf.keras.layers.Dense(units='1', name='let_output')(first_dense)#value of y1 is outputted 
    
    second_dense = tf.keras.layers.Dense(units='128', activation='relu')(first_dense)#second layer is to predict V/VDSS value; 128 nodes are in the layer, with the activation function as ReLu
    y2_output = tf.keras.layers.Dense(units='1', name='vds_output')(second_dense)#value of y2 is outputted
    
    model = tf.keras.models.Model(inputs=input_layer, outputs=[y1_output, y2_output])#final prediction is outputted as a 1D array; input features will be presented in the first, input layer
    
    return model

model = multi_out_model(input_shape=norm_train_X.shape[1:])#model uses normalized training data, where ndim does not include the first dimension
model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])#adam optimizer is used during tuning and optimization; model is evaluated through root mean squared error (RMSE)

history = model.fit(norm_train_X, train_Y,
                    epochs=100, batch_size=100, validation_data=(norm_test_X, test_Y))#model is trained with a batch size of 100, and 100 epochs for every batch size

loss, Y1_loss, Y2_loss, Y1_rmse, Y2_rmse = model.evaluate(x=norm_test_X, y=test_Y)

print()
print(f'loss: {loss}')
print(f'let_loss: {Y1_loss}')
print(f'vds_loss: {Y2_loss}')
print(f'let_rmse: {Y1_rmse}')
print(f'vds_rmse: {Y2_rmse}')

filename = 'finalized_model.sav'#save model for future use
pickle.dump(model, open(filename, 'wb'))#save model for future use