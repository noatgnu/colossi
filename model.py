from keras.models import load_model
import numpy as np

def prediction_with_model(X):
    #Sample Data - Replace with inputed metrics
    # X = np.zeros((1, 8))
    # load model
    model = load_model('model.h5')
    #Predict with model
    raw_prediction = model.predict(X)
    #Convert prediction to 0 or 1 - 0 is bad, 1 is good
    prediction =np.argmax(raw_prediction, axis = 1)
    return prediction[0]