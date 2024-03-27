import pandas as pd

# Load data
df = pd.read_csv('widsdatathon2024-university/train.csv')


# Check for duplicate IDs
# duplicate_ids = df[df.duplicated('patient_id')]
# print("Duplicate IDs:\n", duplicate_ids)

# # Get unique values from the second column
# unique_values = df['patient_race'].unique()

# # Print unique values
# print(unique_values)

# # Count unique values including NaN
# value_counts = df['patient_race'].value_counts(dropna=False)

# # Print the counts
# print(value_counts)

# # Get unique values from the second column
# unique_values = df['payer_type'].unique()

# # Print unique values
# print(unique_values)

# # Count unique values including NaN
# value_counts = df['payer_type'].value_counts(dropna=False)

# # Print the counts
# print(value_counts)

# # Get unique values from the second column
# unique_values = df['payer_type'].unique()

# # Print unique values
# print(unique_values)

# # Count unique values including NaN
# value_counts = df['payer_type'].value_counts(dropna=False)

# # Print the counts
# print(value_counts)

# # Find state codes with more than 2 letters
# invalid_state_codes = df[df['patient_state'].notna() & df['patient_state'].astype(str).apply(lambda x: len(x) > 2)]

# # Print the rows with invalid state codes
# print(invalid_state_codes)

# # Count unique values including NaN
# value_counts = df['patient_state'].value_counts(dropna=False)

# # Print the counts
# print(value_counts)

# # Filter rows where 'patient_zip3' does not have exactly three digits
# invalid_zip_rows = df[df['patient_zip3'].notna() & ~df['patient_zip3'].astype(str).str.match(r'^\d{3}$')]


# # Print the rows with invalid ZIP codes
# print(invalid_zip_rows)

# # Check for null values in the ZIP code column
# null_zip_rows = df[df['patient_zip3'].isna()]

# # Print the rows with null ZIP codes
# print(null_zip_rows)

# Define a function to get the most common region, division, and patient_state and its count
def get_most_common_and_count(group):
    mode_df = group[['region', 'division', 'patient_state']].mode()
    if mode_df.empty:
        # Return a series with NaN values if mode cannot be computed
        return pd.Series({'patient_state': pd.NA, 'region': pd.NA, 'division': pd.NA, 'count': 0})
    else:
        # Compute the count of the mode in the original group
        count = group[(group['region'] == mode_df.iloc[0]['region']) & 
                      (group['division'] == mode_df.iloc[0]['division']) &
                      (group['patient_state'] == mode_df.iloc[0]['patient_state'])].shape[0]
        mode_df['count'] = count
        return mode_df.iloc[0]

# Group the data by 'patient_zip3', apply the function, and reset index to turn the group keys into a column
most_common_combination_with_count = df.groupby('patient_zip3').apply(get_most_common_and_count).reset_index()

# Save the resulting DataFrame to an Excel file
most_common_combination_with_count.to_excel('most_common_combination_with_count.xlsx', index=False)