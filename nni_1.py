# -*- coding: utf-8 -*-
"""NNI-1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1nbo1EVVlptLmpFH3LOF03OCiJyRQJOlA

# **Neural Network Intelligence (NNI) without scaling**

**Introduction**

**As per the problem statement the target columns are NFL,NFH, so i have constructed two different model structure which are slightly different they are namely Dependent model construction/implementation &  Independent model construction/implementation, the difference between them is that dependent model structure/implementation ,would perform  training/prediction of   NFH  first based on other features (excluding nfl), once that is completed it would train NFL based on other features along with the values of NFH or in other words NFL model training would depend on NFH values along with that NFL predictions would be made based on predicted values of NFH as presented by the NFH model, and i term this model to be a pipeline model, whereas in the Independent model construction/implementation both NFH,NFL trainings would be performed seperately**


**Queries at this stage**

**1) Can we predict NFL using NFH predicted values in pipeline technique ?**

**A) Yes Sir we can ,but here i have strictly followed the order of the columns mentioned in the original dataset so as a result NFH column came first followed by NFL so hence used the same but if need be we could employ the viceversa also sir**

**Note:Predictions are made using test set, whereas training set is dedicated for model fitting sir**

**Important Note: KIndly run the code cells in order so as to obtain accurate results sir**

**Libraries**
"""

# Uninstall mkl for faster neural-network training time
!pip uninstall -y mkl
# Upgrade pip to ensure the latest package versions are available
!pip install -U pip
# Upgrade setuptools to be compatible with namespace packages
!pip install -U setuptools wheel
!pip install -U "mxnet<2.0.0"
# Install autogluon (Tutorial based on autogluon==0.1.0)
! pip install --upgrade nni
# Upgrade ipykernel (Necessary for Colab)
!pip install -U ipykernel

import pandas as pd # Library to process the dataframe
import numpy as np # Library to handle with numpy arrays
import warnings # Library that handles all the types of warnings during execution
import matplotlib.pyplot as plt# Library that handles ploting of  the graphs
warnings.filterwarnings("ignore") # Ignore all the warnings

"""### **Dataset Preprocessing**"""

def process(df):
  # input: unprocessed dataframe
  # output: processed dataframe
  df.reset_index(inplace=True)
  p=list(df.iloc[:,-1].values)
  #p.pop(0)
  df=df.drop(columns=['nfl_data']) # removing the header of dataframe
  df=df.rename(columns={"level_0":"Index","level_1":"Date(IST)","level_2":"NFO","level_3":"NFH","level_4":"NFL","level_5":"NFC","level_6":"FIIB","level_7":"FIIS","level_8":"FIIN","level_9":"DIIB","level_10":"DIIS","level_11":"DIIN","level_12":"August","level_13":"December","level_14":"CAD","level_15":"DAD","level_16":"DOD","level_17":"NDAD","level_18":"Currey","level_19":"Flow","level_20":"Shine"})
  df['Vega']=p
  df=df.drop(0)
  #print(df.columns)
  df=df.drop(columns=['Index'])
  df=df.dropna(how='any')
  df['NFO']=pd.to_numeric(df['NFO']).astype(float)
  df['NFH']=pd.to_numeric(df['NFH']).astype(float)
  df['NFL']=pd.to_numeric(df['NFL']).astype(float)
  df['NFC']=pd.to_numeric(df['NFC']).astype(float)
  df['FIIB']=pd.to_numeric(df['FIIB']).astype(float)
  df['FIIS']=pd.to_numeric(df['FIIS']).astype(float)
  df['FIIN']=pd.to_numeric(df['FIIN']).astype(float)
  df['DIIB']=pd.to_numeric(df['DIIB']).astype(float)
  df['DIIS']=pd.to_numeric(df['DIIS']).astype(float)
  df['August']=pd.to_numeric(df['August']).astype(float)
  df['December']=pd.to_numeric(df['December']).astype(float)
  df['CAD']=pd.to_numeric(df['CAD']).astype(float)
  df['DAD']=pd.to_numeric(df['DAD']).astype(float)
  df['DOD']=pd.to_numeric(df['DOD']).astype(float)
  df['NDAD']=pd.to_numeric(df['NDAD']).astype(float)
  df['Flow']=pd.to_numeric(df['Flow']).astype(float)
  df['Currey']=pd.to_numeric(df['Currey']).astype(float)
  df['Shine']=pd.to_numeric(df['Shine']).astype(float)
  df['Vega']=pd.to_numeric(df['Vega']).astype(float)
  df['nfh']=df['NFH']
  df['nfl']=df['NFL']
  df=df.drop(columns=['NFH','NFL'])
  
  return df

"""**Gathering and Processing the dataframe**"""

df=pd.read_csv('csv_nfl_data.csv')
df=process(df)
df

"""### **Model Construction/Implementation using NNI**


"""

import nni
import pickle
from sklearn.model_selection import train_test_split
import numpy as np
from sklearn.multioutput import MultiOutputRegressor
from sklearn.metrics import r2_score
from sklearn.ensemble import StackingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lars
from xgboost import XGBRegressor
from sklearn.linear_model import ARDRegression
from sklearn.neural_network import MLPRegressor

def run(X_train, X_test, y_train, y_test):
  models = list()# stack of models 
  models.append(('Ridge',Ridge()))
  models.append(('Lars',Lars()))
  models.append(('LR',LinearRegression()))
  models.append(('ARDR',ARDRegression()))
  models.append(('XGBC',XGBRegressor()))
  models.append(('MLPR',MLPRegressor(alpha=0.01, batch_size=300, epsilon=1e-08, hidden_layer_sizes=(300,), learning_rate='adaptive', max_iter=750)))
  meta =XGBRegressor()
  model = StackingRegressor(estimators=models,final_estimator=meta,cv=25)
  reg = MultiOutputRegressor(estimator=model)
  reg.estimator.final_estimator_ = reg.estimator.final_estimator
  reg.fit(X_train,y_train)
  filename = 'IM-NFH.h5'
  pickle.dump(reg, open(filename, 'wb'))
  print("Model saved succesfully!!!")
  loaded_model = pickle.load(open(filename, 'rb'))
  print("Loaded Model Sucessfully")
  predict_y = loaded_model.predict(X_test)
  score = r2_score(y_test, predict_y)
  print('Super Learner: %.3f' % (score * 100))
  nni.report_final_result(score)
  return predict_y

def run1(X_train, X_test, y_train, y_test):
  models = list()# stack of models 
  models.append(('Ridge',Ridge()))
  models.append(('Lars',Lars()))
  models.append(('LR',LinearRegression()))
  models.append(('ARDR',ARDRegression()))
  models.append(('XGBC',XGBRegressor()))
  models.append(('MLPR',MLPRegressor(alpha=0.01, batch_size=300, epsilon=1e-08, hidden_layer_sizes=(300,), learning_rate='adaptive', max_iter=750)))
  meta =XGBRegressor()
  model = StackingRegressor(estimators=models,final_estimator=meta,cv=25)
  reg = MultiOutputRegressor(estimator=model)
  reg.estimator.final_estimator_ = reg.estimator.final_estimator
  reg.fit(X_train,y_train)
  filename = 'IM-NFL.h5'
  pickle.dump(reg, open(filename, 'wb'))
  print("Model saved succesfully!!!")
  loaded_model = pickle.load(open(filename, 'rb'))
  print("Loaded Model Sucessfully")
  predict_y = loaded_model.predict(X_test)
  score = r2_score(y_test, predict_y)
  print('Super Learner: %.3f' % (score * 100))
  nni.report_final_result(score)
  return predict_y

def run2(X_train, X_test, y_train, y_test):
  models = list()# stack of models 
  models.append(('Ridge',Ridge()))
  models.append(('Lars',Lars()))
  models.append(('LR',LinearRegression()))
  models.append(('ARDR',ARDRegression()))
  models.append(('XGBC',XGBRegressor()))
  models.append(('MLPR',MLPRegressor(alpha=0.01, batch_size=300, epsilon=1e-08, hidden_layer_sizes=(300,), learning_rate='adaptive', max_iter=750)))
  meta =XGBRegressor()
  model = StackingRegressor(estimators=models,final_estimator=meta,cv=25)
  reg = MultiOutputRegressor(estimator=model)
  reg.estimator.final_estimator_ = reg.estimator.final_estimator
  reg.fit(X_train,y_train)
  filename = 'DM-NFH.h5'
  pickle.dump(reg, open(filename, 'wb'))
  print("Model saved succesfully!!!")
  loaded_model = pickle.load(open(filename, 'rb'))
  print("Loaded Model Sucessfully")
  predict_y = loaded_model.predict(X_test)
  score = r2_score(y_test, predict_y)
  print('Super Learner: %.3f' % (score * 100))
  nni.report_final_result(score)
  return predict_y

def run3(X_train, X_test, y_train, y_test):
  models = list()# stack of models 
  models.append(('Ridge',Ridge()))
  models.append(('Lars',Lars()))
  models.append(('LR',LinearRegression()))
  models.append(('ARDR',ARDRegression()))
  models.append(('XGBC',XGBRegressor()))
  models.append(('MLPR',MLPRegressor(alpha=0.01, batch_size=300, epsilon=1e-08, hidden_layer_sizes=(300,), learning_rate='adaptive', max_iter=750)))
  meta =XGBRegressor()
  model = StackingRegressor(estimators=models,final_estimator=meta,cv=25)
  reg = MultiOutputRegressor(estimator=model)
  reg.estimator.final_estimator_ = reg.estimator.final_estimator
  reg.fit(X_train,y_train)
  filename = 'DM-NFL.h5'
  pickle.dump(reg, open(filename, 'wb'))
  print("Model saved succesfully!!!")
  loaded_model = pickle.load(open(filename, 'rb'))
  print("Loaded Model Sucessfully")
  predict_y = loaded_model.predict(X_test)
  score = r2_score(y_test, predict_y)
  print('Super Learner: %.3f' % (score * 100))
  nni.report_final_result(score)
  return predict_y

#help(nni)

"""### **Independent construction/implementation**

**The only difference between the above pipelining technique(dependent algorithm structure) and the independent model structure is that in pipelining technique for NFL prediction i assume that NFL depends on NFH and based on which training/prediction but here both the training/predictions of NFL/NFH would be done differently**

### **NFH training/Prediction**

### **Splitting the dataset into the Training set and Test dataframes (70% :train and 30%: test)**

**Note: Shuffling of data is active sir when train/test split occurs ,so as a result every time we run the code different sets of values would be catgeorised as train and test set based on which training and prediction would occur sir**
"""

df1=df.copy()
df1=df1.drop(columns=['nfl'])
X=df1.iloc[:,:-1].values
y=df1.iloc[:,-1].values
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=99, test_size=0.3)

X_train=X_train[:,1:]
X_train

X_test

date=X_test[:,:1]
X_test=X_test[:,1:]
X_test

date=date.reshape(len(date),1)
date=date.flatten()

date

y_test=y_test.reshape(len(y_test),1)
y_train=y_train.reshape(len(y_train),1)

y_pred=run(X_train, X_test, y_train, y_test)

y_test=y_test.flatten()
y_test

y_pred=y_pred.reshape(len(y_pred),1)
y_pred=y_pred.flatten()
y_pred

def disp(y_test,y_pred):
  for i in range(len(y_test)):
    for j in range(len(y_test)):
      if i==j:
        print("The actual value of NFH is {0}, the predicted value of NFH for the same is {1}".format(y_test[i],y_pred[j]))
      else:
        continue

disp(y_test,y_pred)

col=['Date','NFH(actual)','NFH(predicted)']
fg1=pd.DataFrame(columns = col)
fg1['Date']=date
fg1['NFH(actual)']=y_test
fg1['NFH(predicted)']=y_pred
fg1

fg1.to_csv('Independent model analysis: NFH')

plt.figure(figsize=(40,20))
plt.plot(date,y_test,label='NFH(actual)',color='green')
plt.plot(date,y_pred,label='NFH(predicted)',color='red')
plt.grid(True)
plt.title('Comparision  Plot (NFH(actual) vs NFH(predicted))')
plt.legend()
plt.xlabel('Date')
plt.ylabel('NFH')
plt.style.use('fivethirtyeight')
plt.show()

"""### **NFL training/Prediction**

**Predicting NFL Using Train dataset which has actual samples of NFH and Test dataset which has predicted values of NFH  replacing the actual values so as to accomplish the goal of preditcing both the target columns one after the other ,i would replace the actual values of NFH with the predicted values (y_pred) so as to make predictions for NFL based on the predicted values of NFH and hence i term this mode as pipeline model**

### **Splitting the dataset into the Training set and Test dataframes (70% :train and 30%: test)**

**Note: Shuffling of data is active sir when train/test split occurs ,so as a result every time we run the code different sets of values would be catgeorised as train and test set based on which training and prediction would occur sir**
"""

df2=df.copy()
df2=df2.drop(columns=['nfh'])
X=df2.iloc[:,:-1].values
y=df2.iloc[:,-1].values
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=99, test_size=0.3)

df2

X_train=X_train[:,1:]
X_train

date=X_test[:,:1]
X_test=X_test[:,1:]
X_test

date=date.reshape(len(date),1)
date=date.flatten()

date

y_test=y_test.reshape(len(y_test),1)
y_train=y_train.reshape(len(y_train),1)

y_pred1=run1(X_train, X_test, y_train, y_test)

y_test=y_test.flatten()
y_test

y_pred1=y_pred1.reshape(len(y_pred1),1)
y_pred1=y_pred1.flatten()
y_pred1

def disp1(y_test,y_pred):
  for i in range(len(y_test)):
    for j in range(len(y_test)):
      if i==j:
        print("The actual value of NFL is {0}, the predicted value of NFL for the same is {1}".format(y_test[i],y_pred[j]))
      else:
        continue

disp1(y_test,y_pred1)

col1=['Date','NFL(actual)','NFL(predicted)']
fg2=pd.DataFrame(columns = col1)
fg2['Date']=date
fg2['NFL(actual)']=y_test
fg2['NFL(predicted)']=y_pred1
fg2

fg2.to_csv('Independent model analysis: NFL')

plt.figure(figsize=(40,20))
plt.plot(date,y_test,label='NFL(actual)',color='blue')
plt.plot(date,y_pred1,label='NFL(predicted)',color='red')
plt.grid(True)
plt.title('Comparision  Plot (NFL(actual) vs NFL(predicted))')
plt.legend()
plt.xlabel('Date')
plt.ylabel('NFL Values')
plt.style.use('fivethirtyeight')
plt.show()

col=['NFH(actual)','NFL(actual)','NFH(predicted)','NFL(predicted)']
fg=pd.DataFrame(columns = col)
fg.iloc[:,0]=fg1['NFH(actual)']
fg.iloc[:,1]=fg2['NFL(actual)']
fg.iloc[:,2]=y_pred
fg.iloc[:,3]=y_pred1
fg['Amount of Deviation:NFH (actual vs prediction)']=abs(fg['NFH(actual)']-fg['NFH(predicted)']).astype(float)
fg['Amount of Deviation:NFL (actual vs prediction)']=abs(fg['NFL(actual)']-fg['NFL(predicted)']).astype(float)
display(fg)
fg.to_csv('Independent model Analysis.csv')

"""## **Dependent model construction/implementation**

**For NFH model fitting/prediction we shall remove actual NFL values as depcited in the order of the columns in the actual dataset**

###**NFH training/prediction**

### **Splitting the dataset into the Training set and Test dataframes (70% :train and 30%: test)**

**Note: Shuffling of data is active sir when train/test split occurs ,so as a result every time we run the code different sets of values would be catgeorised as train and test set based on which training and prediction would occur sir**
"""

df1=df.copy()
df1=df1.drop(columns=['nfl'])
X=df1.iloc[:,:-1].values
y=df1.iloc[:,-1].values
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=99, test_size=0.3)

df1

X_train=X_train[:,1:]
X_train

X_test

date=X_test[:,:1]
X_test=X_test[:,1:]
X_test

date=date.reshape(len(date),1)
date=date.flatten()

date

y_test=y_test.reshape(len(y_test),1)
y_train=y_train.reshape(len(y_train),1)

y_pred1=run2(X_train, X_test, y_train, y_test)

len(X_train)

len(y_train)

len(X_test)

len(y_test)

y_test=y_test.reshape(len(y_test),1)
y_test=y_test.flatten()
y_test

y_pred=y_pred.reshape(len(y_pred),1)
y_pred=y_pred.flatten()
y_pred

disp(y_test,y_pred)

col=['Date','NFH(actual)','NFH(predicted)']
fg3=pd.DataFrame(columns = col)
fg3['Date']=date
fg3['NFH(actual)']=y_test
fg3['NFH(predicted)']=y_pred
fg3

fg3.to_csv('Dependent model analysis: NFH')

plt.figure(figsize=(40,20))
plt.plot(date,y_test,label='NFH(actual)',color='green')
plt.plot(date,y_pred,label='NFH(predicted)',color='red')
plt.grid(True)
plt.title('Comparision  Plot (NFH(actual) vs NFH(predicted))')
plt.legend()
plt.xlabel('Date')
plt.ylabel('NFH')
plt.style.use('fivethirtyeight')
plt.show()

"""### **NFL training/prediction**

### **Splitting the dataset into the Training set and Test dataframes (70% :train and 30%: test)**

**Note: Shuffling of data is active sir when train/test split occurs ,so as a result every time we run the code different sets of values would be catgeorised as train and test set based on which training and prediction would occur sir**
"""

df2=df.copy()
X=df2.iloc[:,:-1].values
y=df2.iloc[:,-1].values
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=99, test_size=0.3)

df2

X_train=X_train[:,1:]
X_train

date=X_test[:,:1]
X_test=X_test[:,1:]
X_test

date=date.reshape(len(date),1)
date=date.flatten()

date

y_test=y_test.reshape(len(y_test),1)
y_train=y_train.reshape(len(y_train),1)

y_pred1=run3(X_train, X_test, y_train, y_test)

y_test=y_test.flatten()
y_test

y_pred1=y_pred1.reshape(len(y_pred1),1)
y_pred1=y_pred1.flatten()
y_pred1

disp1(y_test,y_pred1)

col1=['Date','NFL(actual)','NFL(predicted)']
fg4=pd.DataFrame(columns = col1)
fg4['Date']=date
fg4['NFL(actual)']=y_test
fg4['NFL(predicted)']=y_pred1
fg4

fg4.to_csv('Independent model analysis: NFL')

plt.figure(figsize=(40,20))
plt.plot(date,y_test,label='NFL(actual)',color='blue')
plt.plot(date,y_pred1,label='NFL(predicted)',color='red')
plt.grid(True)
plt.title('Comparision  Plot (NFL(actual) vs NFL(predicted))')
plt.legend()
plt.xlabel('Date')
plt.ylabel('NFL Values')
plt.style.use('fivethirtyeight')
plt.show()

col=['NFH(actual)','NFL(actual)','NFH(predicted)','NFL(predicted)']
fg1=pd.DataFrame(columns = col)
fg1.iloc[:,0]=fg3['NFH(actual)']
fg1.iloc[:,1]=fg4['NFL(actual)']
fg1.iloc[:,2]=y_pred
fg1.iloc[:,3]=y_pred1
fg1['Amount of Deviation:NFH (actual vs prediction)']=abs(fg1['NFH(actual)']-fg1['NFH(predicted)']).astype(float)
fg1['Amount of Deviation:NFL (actual vs prediction)']=abs(fg1['NFL(actual)']-fg1['NFL(predicted)']).astype(float)
fg1.to_csv('Dependent model Analysis.csv')
display(fg1)

"""### **Comparative Analysis between Dependent and Independent model algorithms**"""

d=pd.read_csv('Dependent model Analysis.csv')
id=pd.read_csv('Independent model Analysis.csv')

"""**Graphical Analysis of NFH values**"""

plt.figure(figsize=(40,20))
plt.plot(date,d['NFH(actual)'],label='NFH(actual)')
plt.plot(date,d['NFH(predicted)'],label='predicted values of NFH : dependent model analysis')
plt.plot(date,id['NFH(predicted)'],label='predicted values of NFH : independent model analysis')
plt.grid(True)
plt.title('Comparative Analysis between Dependent and Independent model algorithms:NFH')
plt.legend()
plt.xlabel('Date')
plt.ylabel('NFH Values')
plt.style.use('fivethirtyeight')
plt.show()

"""**Amount of Deviation between the actual values and the predicted values for both the models based on NFH**"""

plt.figure(figsize=(40,20))
plt.plot(date,d['Amount of Deviation:NFH (actual vs prediction)'],label='predicted values of NFH : dependent model analysis')
plt.plot(date,id['Amount of Deviation:NFH (actual vs prediction)'],label='predicted values of NFH : independent model analysis')
plt.grid(True)
plt.title('Comparative Analysis between Dependent and Independent model algorithms:NFH Deviation')
plt.legend()
plt.xlabel('Date')
plt.ylabel('NFH Deviation Values')
plt.style.use('fivethirtyeight')
plt.show()

"""**Graphical Analysis of NFL values**"""

plt.figure(figsize=(40,20))
plt.plot(date,d['NFL(actual)'],label='NFL(actual)')
plt.plot(date,d['NFL(predicted)'],label='predicted values of NFL : dependent model analysis')
plt.plot(date,id['NFL(predicted)'],label='predicted values of NFL : independent model analysis')
plt.grid(True)
plt.title('Comparative Analysis between Dependent and Independent model algorithms:NFL')
plt.legend()
plt.xlabel('Date')
plt.ylabel('NFL Values')
plt.style.use('fivethirtyeight')
plt.show()

"""**Amount of Deviation between the actual values and the predicted values for both the models based on NFL**"""

plt.figure(figsize=(40,20))
plt.plot(date,d['Amount of Deviation:NFL (actual vs prediction)'],label='predicted values of NFL : dependent model analysis')
plt.plot(date,id['Amount of Deviation:NFL (actual vs prediction)'],label='predicted values of NFL : independent model analysis')
plt.grid(True)
plt.title('Comparative Analysis between Dependent and Independent model algorithms:NFL Deviation')
plt.legend()
plt.xlabel('Date')
plt.ylabel('NFL Deviation Values')
plt.style.use('fivethirtyeight')
plt.show()

"""**Based on the above comparative anaylsis graphs sir , one can choose the best model structure/implementation required to train/predict the same**

## **Conclusion**

**I would like to point out that there would be a rare possibility that both the Dependent model analysis.csv, indpendent model analysis.csv would be the same,but due to the fact these models operate using different logic hence the probability of dependent model analysis.csv and independent model analysis.csv would not be the same(i.e there would be a slight difference of values between them), i have enclosed a copy of the datasets for supporting the same sir.**



**Thank you**
"""