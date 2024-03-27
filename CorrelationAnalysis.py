import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency
from matplotlib.backends.backend_pdf import PdfPages

# Load data
df = pd.read_csv('widsdatathon2024-university/fixed_gender.csv')  # Update this to your CSV file path

# Prepare PDF to save figures
pdf_path = 'widsdatathon2024-university/analysis_output.pdf'
pdf_pages = PdfPages(pdf_path)

# Pearson correlation for continuous variables
correlations = df[['population', 'density', 'treatment_pd']].corr()
fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(correlations, annot=True, ax=ax)
pdf_pages.savefig(fig)  # Save the figure into the PDF

# Scatter and regression plots for continuous variables
for column in ['population', 'density']:
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.scatterplot(data=df, x=column, y='treatment_pd', ax=ax)
    sns.regplot(data=df, x=column, y='treatment_pd', scatter=False, color='red', ax=ax)
    pdf_pages.savefig(fig)

# Analyze and visualize categorical variables
for column in ['region', 'division', 'patient_zip3']:
    contingency_table = pd.crosstab(df[column], df['treatment_pd'])
    chi2, p, dof, expected = chi2_contingency(contingency_table)
    print(f"Chi-Square Test for {column} and 'treatment_pd': p-value = {p}")
    
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.barplot(data=df, x=column, y='treatment_pd', estimator=len, ax=ax)
    plt.xticks(rotation=45)
    pdf_pages.savefig(fig)

pdf_pages.close()  # Close the PDF and save the file
