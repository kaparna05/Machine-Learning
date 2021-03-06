# -*- coding: utf-8 -*-
"""Graduation_Academic_Prediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/11sPrMx_o232yBulHreYzH7ur6iSDfVh8
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings('ignore')

from sklearn.model_selection import train_test_split #function
from sklearn.linear_model import LinearRegression #class
from sklearn.metrics import mean_squared_error, r2_score #function

df = pd.read_csv('Admission_Predict.csv')

"""#Analysing Data Set"""

sns.heatmap(df.corr(),annot=True)

"""Observation: From the above heatmap we can observe that variables CGPA, TOEFL, GRE Score has high correlation with the dependent variable Chance of Admit. Below is an visualization of the same using scatter plot."""

#plt.figure(figsize=(10,10))
sns.scatterplot(x=df['CGPA'],y=df['Chance of Admit '],color='green')
sns.scatterplot(x=df['GRE Score'],y=df['Chance of Admit '],color='blue')
sns.scatterplot(x=df['TOEFL Score'],y=df['Chance of Admit '],color='orange')

df.describe()

"""Observation: The above table provides a summarised view of statistical details of all the columns"""

sns.scatterplot(data=df,x='GRE Score',y='TOEFL Score')

"""Observation: GRE Score and TOEFL Score shows us a high positive correlation, which brings us to a conclusion that a person who performs well in GRE also performs good in TOEFL."""

sns.scatterplot(data=df,x='GRE Score',y='CGPA')

"""Observation: GRE Score and CGPA shows us a high positive correlation, which brings us to a conclusion that a person who performs well in Academics also performs good in GRE.

The same holds true for TOEFL Score and CGPA.
"""

sns.barplot(x=df['Research'],y=df['Chance of Admit '])

sns.scatterplot(data=df,x='CGPA',y='GRE Score',hue='Research')

"""Observation: A student excelling in academics as well as entrance test tend to do research which increases their chance of admission

#Exploratory Data Analysis
"""

df.head()

#Removing Unwanted column
df.drop(df[['Serial No.']],axis=1,inplace=True)

df.head() #Column Serial No. has been removed

df.shape

"""Step1: Handling missing values / junk values"""

df.info()

"""Info: As all the no of rows are 500 and if the column contains any junk value then the data type of the column is object. Here in above data set all the columns are of int or float type. Hence we can conclude there is no missing values as well as junk data"""

df.isnull().sum()

"""Observation: As all the column shows 500 rows hence there is no missing values and also as none of the column type is object columns also does not consists junk value. We can also confirm the same by above .isnull() output

Step2 : Handling Outliers
"""

sns.boxplot(df['Chance of Admit '])

sns.boxplot(df['Chance of Admit '],whis=1.53)

"""Observation: We can observe from the above boxplot that there is not much of Outliers, increasing the whis by 0.03 makes the data set outlier free

Step3: Handling skewness
"""

from scipy.stats import skew

for col in df:
  try:
    print(col,"=",skew(df[col]))
    sns.distplot(df[col])
    plt.show()
  except:
    pass
  finally:
    print("**********************************************")

"""Observation: Skew value for all the columns range between -0.5 and 0.5. Hence we do not have any columns to reduce skewness

Step4: Handling Categorical Data
"""

df.head()

"""Observation: Analyzing dataset we can understand that there is no column with categorical value

#Modelling
"""

df.head()

sns.heatmap(df.corr(),annot=True)

"""Prediction considering only CGPA"""

x_train,x_test,y_train,y_test = train_test_split(df[['CGPA']],df['Chance of Admit '],test_size=0.3)

lr = LinearRegression()
lr.fit(x_train,y_train)

print(lr.intercept_)

print(lr.coef_)

y_hat = lr.predict(x_test)

mean_squared_error(y_test,y_hat)

r2_score(y_test,y_hat)

residuals = y_test - y_hat
sns.scatterplot(y_hat,residuals)
plt.show()

sns.distplot(residuals)
plt.show()

skew(residuals)

"""Observation: Score for the prediction using only CGPA is 0.77. Wherein wrt to the domain knowledge all other features are equally important for prediction

Prediction considering all the columns
"""

x_train,x_test,y_train,y_test = train_test_split(df.drop(['Chance of Admit '],axis=1),df['Chance of Admit '],test_size=0.3)

lr = LinearRegression()

lr.fit(x_train,y_train)

lr.intercept_

lr.coef_ #y = mx + c # y = m1x1 + m2x2 + .... + c

y_hat = lr.predict(x_test)

r2_score(y_test,y_hat)

residuals = y_test - y_hat
sns.scatterplot(y_hat,residuals)
plt.show()

sns.distplot(residuals)

skew(residuals)

"""**Observation**: Score has slightly increased after considering all the features for prediction. 
Assumptions of Linear Regression:
1. Dependent and Independent variable must have correlation
    > explanation- Multiple independent variables within the dataset has higher correlation with the dependent variable, CGPA being the highest with 0.88 - **PASS**

2. There must be little or no variance among residuals
    > explanation- Observing the above scatterplot we can observe that the graph is not homo-skedestical - **FAIL**
3. There should be no multi-colleniarity
    > explanation- Variables GRE Score, TOEFL Score, CGPA are highly correlated to each other. - **FAIL**
4. Residuals must be normally distributed
    > explanation- Observing the above distplot and the skewness value of the residuals, the bell curve is slightly skewed which can be accepted. - **FAIL**

Prediction using selected features
"""

df.info()

x = df[['CGPA','University Rating','SOP','LOR ','Research']]
y = df['Chance of Admit ']

x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.3)

lr = LinearRegression()
lr.fit(x_train,y_train)

print(lr.intercept_)
print(lr.coef_)

y_hat = lr.predict(x_test)

r2_score(y_test,y_hat)

lr.score(x_test,y_test)

residuals = y_test - y_hat
sns.scatterplot(y_hat,residuals)
plt.show()

sns.distplot(residuals)

skew(residuals)

"""**Observation**: Score has slightly increased after considering all the features for prediction. 
Assumptions of Linear Regression:
1. Dependent and Independent variable must have correlation
    > explanation- Multiple independent variables within the dataset has higher correlation with the dependent variable, CGPA being the highest with 0.88 - **PASS**

2. There must be little or no variance among residuals
    > explanation- Observing the above scatterplot we can observe that the graph is not homo-skedestical - **FAIL**
3. There should be no multi-colleniarity
    > explanation- Variables GRE Score, TOEFL Score, CGPA are highly correlated to each other, hence the above prediction is considered excluding GRE Score, TOEFL Score. - **PASS**
4. Residuals must be normally distributed
    > explanation- Observing the above distplot and the skewness value of the residuals, the bell curve is slightly skewed which can be accepted. - **PASS** **(DOUBT)**

Prediction using Polynomial Regression
"""

from sklearn.preprocessing import PolynomialFeatures

x = df[['CGPA','University Rating','SOP','LOR ','Research']]
y = df['Chance of Admit ']

pf = PolynomialFeatures(2)
x_degree_2 = pf.fit_transform(x)

x_train, x_test, y_train, y_test = train_test_split(x_degree_2,y,test_size=0.3)
lr = LinearRegression()
lr.fit(x_train,y_train)
y_train_hat = lr.predict(x_train)
print("Bias = ",r2_score(y_train,y_train_hat))
y_test_hat = lr.predict(x_test)
print("Variance = ",r2_score(y_test,y_test_hat))

residuals = y_test - y_test_hat
sns.scatterplot(y_test_hat,residuals)
plt.show()

sns.distplot(residuals)

skew(residuals)

"""**Observation**: Score has slightly increased after considering all the features for prediction. 
Assumptions of Linear Regression:
1. Dependent and Independent variable must have correlation
    > explanation- Multiple independent variables within the dataset has higher correlation with the dependent variable, CGPA being the highest with 0.88 - **PASS**

2. There must be little or no variance among residuals
    > explanation- Observing the above scatterplot we can observe that the graph is not homo-skedestical - **FAIL**
3. There should be no multi-colleniarity
    > explanation- Variables GRE Score, TOEFL Score, CGPA are highly correlated to each other. - **PASS**
4. Residuals must be normally distributed
    > explanation- Observing the above distplot and the skewness value of the residuals, the bell curve is slightly skewed which can be accepted. - **PASS**

Polynomial Regression with Degree 4
"""

from sklearn.preprocessing import PolynomialFeatures

x = df[['CGPA','University Rating','SOP','LOR ','Research']]
y = df['Chance of Admit ']

pf = PolynomialFeatures(4)
x_degree_4= pf.fit_transform(x)

x_train, x_test, y_train, y_test = train_test_split(x_degree_4,y,test_size=0.3)
lr = LinearRegression()
lr.fit(x_train,y_train)
y_train_hat = lr.predict(x_train)
print("Bias = ",r2_score(y_train,y_train_hat))
y_test_hat = lr.predict(x_test)
print("Variance = ",r2_score(y_test,y_test_hat))

residuals = y_test - y_test_hat
sns.scatterplot(y_test_hat,residuals)
plt.show()

sns.distplot(residuals)

skew(residuals)

"""Observation: Increasing the power to 3 doesn't make much difference, henceforth increasing the power to 4 arises a situation of overfitting which can be understood by the Bias and Variance Score.

**We can conclude that the polynomial regression with degree 2 gives us a good model**
"""