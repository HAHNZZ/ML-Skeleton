import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler

# Load the data
csv_file_path = 'C:/Users/hansg/Downloads/dummy_data.csv'  # Update this with the path to your CSV file.
df = pd.read_csv(csv_file_path)

# Select features and target variable
X_scaled = df.drop('treatment_pd', axis=1)  # This drops the target column from the features.
y = df['treatment_pd']  # This is the target variable.

# Preprocessing: Handle categorical variables if necessary and scale the data
# Assuming that your categorical variables are already binary encoded based on your CSV header.
# It might be necessary to scale the data if the range of your features varies widely.
#scaler = StandardScaler()
#X_scaled = scaler.fit_transform(X)

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Initialize the Linear Regression model
lin_reg = LinearRegression()

# Fit the model to the training data
lin_reg.fit(X_train, y_train)

# Predict on the test data
y_pred = lin_reg.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f'Mean Squared Error: {mse:.2f}')
print(f'R^2 Score: {r2:.2f}')
