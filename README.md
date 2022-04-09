
# Vadimaniac-Code
Repository for Vadimaniacs' Heresy's project code

I added the create_venv.sh we use for class along with an updated requirements.txt.
The requirements.txt adds the pyarrow library to a virtual environment. 
Pyarrow is used to open the parquet and feather files in the Argoverse2 download. 

The preprocess.py may be usable with many different types of models.

The mlp_model_1.py model is a very basic 2 layer mlp that predicts 5 of the features that were
chosen in the preprocess.py code. After the model trains, it outputs a prediction for the 
values of all the features in the next timestap. There is a prechosen timeseries 
that the prediction is based on that prints just ahead of the prediction.

There is a visualizatoin of the training loss per batch as well.

Switching the data input into the model to an '5-gram' layout greatly improved the 
testing loss. I corrected an error in the processing where the data was not being properly 
flattened. Now the model trains much faster and appears to be more accurate depending on the 
number of epochs.


The gru_model.py model has one GRU layer with two dense layers. There is a 
visualization for the batch loss on this one. The training loss decreases 
very smoothly before 1000 epochs. There may be overfitting though since the 
test loss is fairly high to start but stabalizes after 1000 epochs as well.

The model presents a prediction of the next timestep just as the mlp mpdel does.
There is a difference in the way the prediction is displayed though. It appears as though some
recent revisions of the keras LSTM and GRU models do not give the user the ability 
to set the input shape. They expect batch size, timestps (or window size), feature only. Therefore,
the output is three dimensional. If we keep the number of outputs from the GRU layer at 
the window size then the timestep that is predicted all have the same value. If you increase the 
number of outputs then each timestep predicted varies by a small margin. Keeping the output 
at window size does not appear to effect the prediction accuracy but I cannot say this is the 
correct way to do this. More research is needed. 
