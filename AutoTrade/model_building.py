from sklearn.linear_model import LinearRegression #mean square error사용하는방법
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split

test_data = pd.read_excel(r'C:\Users\jongh\OneDrive\바탕 화면\project\Stock_Project\Convert_M_Data\동국알앤에스_Fdata_Min.xlsx')

tmp = []
for i in range(len(test_data)):
  if i != (len(test_data) -1) :
    tmp += test_data['open'][i+1],
  else:
    tmp += test_data['open'][i],

test_data['Target'] = tmp
test_data.drop(index=len(test_data)-1,inplace=True)
test_data.reset_index(drop=True,inplace=True)
test_data.dropna(axis=0,inplace=True)
len(test_data)
test_data.drop(['Unnamed: 0', 'Unnamed: 0.1','compare'], axis=1, inplace=True)
test_data.drop(['day','time'], axis=1, inplace=True)

X = test_data.iloc[:,0:-1]
Y = test_data['Target']
print(X.shape,Y.shape)

X_train, X_test, y_train, y_test = \
train_test_split(X, Y, test_size = 0.2, random_state = 13)

lr_Dong = LinearRegression(fit_intercept=True, normalize=True, n_jobs = -1)
lr_Dong.fit(X_train, y_train)  
lr_Dong.score(X_test, y_test)

joblib.dump(lr_Dong,'testdata.pkl')
#test_model = joblib.load('testdata.pkl')