# Defect Classification via Convolutional Neural Network

## Introduction

We aimed at automating the visual inspection process that identifies
wafer images falling into a certain defect class via Convolutional Neural Network. We attempted
different neural network architectures, parameters, optimization techniques, and image
augmentation techniques to find a better model to fit this classification task. The overall accuracy
is around 93% as shown in the CodaLab competition submissions. The best model so far
achieved 97% accuracy by using three convolutional layers followed by max pooling and
0.25 dropout and vertical flipping as the image augmentation technique. 

## Data Preprocessing

At first, we preprocessed the training images and the labels. We reshaped the training
data to 400x64x64x1. Since there are 6 different defect classes and we expected that the neural
network returned 6 scores for each of the class, for each classified image we would like to have
each class matching with one score and also know the ground truth class. Hence, we cannot just
convert the string labels into integers. Because of this, we used a method called One Hot
Encoding to represent categorical variables as binary vectors. To do this, we converted the string
labels into integers first. Then each integer value is represented as a binary vector that is all zero
values except the index of the integer marked with a 1.

Secondly, we split the training set and validation set with a 7:3 ratio. Initially, we used
8:2 but we considered that there would be only 80 validation images and the experiments with
7:3 showed better results than the ones with 8:2. Hence, we decided to use 7:3 splitting

## CNN Architecture

### Layer number:

Since the wafer image size is 64x64x1 and the training dataset size is 280, we cannot
construct a very deep neural network in order to avoid overfitting and vanishing gradients 
problems. Initially, we tried 4 convolutional layers and turned out that training accuracy kept
improving but the validation accuracy was not improving at all after a few epochs. We concluded
that the overfitting occurred and 4 convolutional layers were too deep for this dataset. Hence, we
decided to use 3 convolutional layers. After switching to 3 convolutional layers, the overfitting
issue was fixed.

Since we decided the basic architecture of the neural network, we started play around the
parameters in convolutional layers, dropout rate, epochs, batch size, image augmentation etc. 

### Filter Number:

At first, we tried the different numbers of filters for each convolutional layer. We started
with 4 filters for the first layer and times two for the next convolutional layer. The accuracy
turned out to be around 90%, which is reasonable. However, when we started with 32 filters for
the first convolutional layer and ended up with 128 filters for the last convolutional layer, the
overfitting occurred again. Hence, we decided to start with 16 for the first convolutional layer, 32
for the second one, and 64 for the last one.

### Kernel and Bias Initializer:

The decision to use ‘RandomNormal’ as the kernel and bias initializer was mostly based
on the experiments. We tried ‘glorot_uniform’, ‘zeros’, and ‘ones’. It seemed that with the
‘RandomNormal’ the neural network consistently generated more robust results.

### Activation function:

We used the rectified linear unit as the activation function at the beginning since the
activation function is computational efficient and good at overcoming slow weights updating
issues.

### Dropout rate, epoch, and batch size:

For these three parameters, the decision was mostly based the observations for the
training accuracy and validation accuracy.

The dropout layer is necessary because it can effectively prevent the overfitting issue for
this case. Since this is not a very deep network and the number of filters is not large, the dropout
rate after each convolutional computation should not be too large. Hence, we used a middle
number 0.25. However, considering the large number of parameters at the last layer, we used 0.5
as the dropout rate for the last layer.

Initially, we trained the neural network for 100 epochs. Since it was not very obvious to
notice that the validation accuracy stopped improving at a certain epoch, we decided to train 200
epochs. However, we noticed that after around 150th epoch the validation accuracy did not
improve that much but the validation accuracy was still improving a bit between 100th and 150th
epochs. Therefore, we decided to train the neural network for 150 epochs.
Since the training data size is 280 and the validation data size is 120, the batch size
should be around 10-20. With a few experiments, we noticed that the overall accuracy was
slightly higher when we used 10 images for a batch.

### Image Augmentation:

The available image augmentation techniques are the following: setting input mean to 0
over the dataset or each sample, random rotation, shearing, zooming, shifting, flipping, zca 
whitening etc. Considering the wafer image is grey-scale and the shape of each image is circle,
we thought the zca_whitening, rotation, standardization would not help training that much. This
was proved by the experiments with these techniques. Also, we experimented with shearing and
zooming. Experiments with shearing did produce slightly better results, which improved the
overall accuracy around 93%. However, experiments with zooming did not show that much
improvements. The best image augmentation technique we attempted so far was flipping. It
improved the overall accuracy to around 94%-95%. Hence, we used vertical flipping as the
image augmentation technique. Since the property of this dataset rules out many techniques

![Image Augmentation examples](https://github.com/ZhengqiY/Defect_Classifcation/blob/master/ImageAugmentationDefectClassification.PNG)

| Layer | Parameter (#filters, kernel size, stride, padding, activation, kernel initializer, bias initializer) |
| --- | --- |
| Block 1 | 16, 3x3, (1,1), same, relu, RandomNormal, RandomNormal, input shape (64,64,1) |
|         | Max pooling with pool size (2,2) |
|         | Dropout 0.25 |
| Block 2 | 32, 3x3, (1,1), same, relu, RandomNormal, RandomNormal |
|         | Max pooling with pool size (2,2) |
|         | Dropout 0.25 |
| Block 3 | 64, 3x3, (1,1), same, relu, RandomNormal, RandomNormal |
|         | Max pooling with pool size (2,2) |
|         | Dropout 0.25 |
| Block 4 | Flatten |
| Block 5 | Dense, 128, relu |
|         | Dropout 0.5 |
| Block 6 | FC, Softmax generating 6 classes results |

