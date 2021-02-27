import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import cross_val_score

df = pd.read_csv('Salary_data_cleaned_full.csv')

#choose relevent params
df_model = df[['average_salary','Rating','Size','Type of ownership', 'Industry', 'Sector', 'Revenue','competitors_count',
               'hourly', 'employer_provided','job_state', 'same_state', 'age_comp',
               'python', 'Spark', 'aws', 'excel', 'job_simp','job_seniority', 'desc_len',]]
#convert cat var to dummy vars
df_dum = pd.get_dummies(df_model)

#train test split
# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
X = df_dum.drop('average_salary', axis=1)
y = df_dum.average_salary.values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

#OLS regression
import statsmodels.api as sm
x_sm = X = sm.add_constant(X)
model = sm.OLS(y, x_sm)
model.fit().summary()

#Linear regression
from sklearn.linear_model import LinearRegression, Lasso, Ridge
reg = LinearRegression()
reg.fit(X_train,y_train)
np.mean(cross_val_score(reg, X_train, y_train, scoring='neg_mean_absolute_error'))

# ridge regression
rdg_reg = Ridge(0.5)
np.mean(cross_val_score(rdg_reg, X_train, y_train, scoring='neg_mean_absolute_error'))

# lasso regression
lss_reg = Lasso(alpha=0.2)
lss_reg.fit(X_train,y_train)
np.mean(cross_val_score(lss_reg, X_train, y_train, scoring='neg_mean_absolute_error'))

alpha = []
error = []
for i in range(1, 100):
    alpha.append(i/100)
    lml = Lasso(alpha=(i/100))
    error.append(np.mean(cross_val_score(lml, X_train, y_train, scoring='neg_mean_absolute_error')))
    
plt.plot(alpha, error)

err = tuple(zip(alpha, error))

df_err = pd.DataFrame(err, columns=['alpha', 'error'])
df_err[df_err.error == max(df_err.error)]    

# Random forest 
from sklearn.ensemble import RandomForestRegressor
r_reg = RandomForestRegressor()
np.mean(cross_val_score(reg, X_train, y_train, scoring='neg_mean_absolute_error'))

#Grid Search CV
from sklearn.model_selection import GridSearchCV
params = {'n_estimators': range(10, 300, 10), 'max_features':('auto', 'sqrt', 'log2'), 'criterion':('mse', 'mae')}

gs = GridSearchCV(r_reg, params, scoring='neg_mean_absolute_error')

gs.fit(X_train, y_train)

gs.best_score_
gs.best_estimator_

#test ensembles
tpred_reg = reg.predict(X_test)
tpred_lss_reg = lss_reg.predict(X_test)
tpred_r_reg = gs.best_estimator_.predict(X_test)

from sklearn.metrics import mean_absolute_error

mean_absolute_error(y_test, tpred_reg)

mean_absolute_error(y_test, tpred_lss_reg)

mean_absolute_error(y_test, tpred_r_reg)











