from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image  # Import Image here
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from reportlab.platypus import PageBreak

# Load your dataset
df = pd.read_csv('widsdatathon2024-university/fixed_gender.csv')

# Define your continuous and categorical columns
continuous_columns = ['population', 'density']
categorical_columns = ['region', 'division', 'patient_zip3']

# Function to generate statistics for continuous variables
def generate_continuous_stats(df, columns):
    stats = df[columns].describe().T
    stats['% missing'] = 100 * (1 - df[columns].count() / len(df))
    stats['cardinality'] = df[columns].nunique()
    return stats

# Function to generate statistics for categorical variables
def generate_categorical_stats(df, columns):
    stats = pd.DataFrame(index=columns, columns=['count', '% missing', 'cardinality', 'mode', 'mode freq', 'mode %', '2nd mode', '2nd mode freq', '2nd mode %'])
    for column in columns:
        stats.at[column, 'count'] = df[column].count()
        stats.at[column, '% missing'] = 100 * (1 - df[column].count() / len(df))
        stats.at[column, 'cardinality'] = df[column].nunique()
        top2 = df[column].value_counts().nlargest(2)
        stats.at[column, 'mode'] = top2.index[0]
        stats.at[column, 'mode freq'] = top2.iloc[0]
        stats.at[column, 'mode %'] = 100 * top2.iloc[0] / len(df)
        if len(top2) > 1:
            stats.at[column, '2nd mode'] = top2.index[1]
            stats.at[column, '2nd mode freq'] = top2.iloc[1]
            stats.at[column, '2nd mode %'] = 100 * top2.iloc[1] / len(df)
        else:
            stats.at[column, '2nd mode'] = 'N/A'
            stats.at[column, '2nd mode freq'] = 'N/A'
            stats.at[column, '2nd mode %'] = 'N/A'
    return stats

# Generate and display the statistics
continuous_stats = generate_continuous_stats(df, continuous_columns)
categorical_stats = generate_categorical_stats(df, categorical_columns)

print("Continuous Variables Stats:")
print(continuous_stats)
print("\nCategorical Variables Stats:")
print(categorical_stats)

# Visualization
# Histograms for continuous variables
for column in continuous_columns:
    plt.figure(figsize=(10, 6))
    sns.histplot(df[column].dropna(), kde=True, bins=30)
    plt.title(f'Histogram of {column}')
    plt.xlabel(column)
    plt.ylabel('Frequency')

# Count plots for categorical variables
for column in categorical_columns:
    plt.figure(figsize=(10, 6))
    sns.countplot(y=column, data=df, order = df[column].value_counts().index)
    plt.title(f'Count Plot of {column}')
    plt.xlabel('Frequency')
    plt.ylabel(column)

# Function to save a figure
def save_fig(plt, fig_id, tight_layout=True, fig_extension="png", resolution=300):
    path = os.path.join(fig_id + "." + fig_extension)
    print("Saving figure", fig_id)
    if tight_layout:
        plt.tight_layout()
    plt.savefig(path, format=fig_extension, dpi=resolution)

# Function to create the PDF with tables
def create_pdf_with_tables(df, continuous_columns, categorical_columns, pdf_path):
    doc = SimpleDocTemplate(pdf_path, pagesize=letter)
    story = []

    # Generate tables for continuous variables
    continuous_stats = generate_continuous_stats(df, continuous_columns)
    continuous_data = [['Category', 'Statistic', 'Value']]
    for column in continuous_columns:
            continuous_stats = generate_continuous_stats(df, [column])
            for stat in continuous_stats.columns:
                continuous_data.append([column, stat, continuous_stats.at[column, stat]])
    continuous_table = Table(continuous_data)
    continuous_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('BOX', (0, 0), (-1, -1), 2, colors.black),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    story.append(continuous_table)
    story.append(PageBreak())
    
    # Generate tables for categorical variables
    categorical_stats = generate_continuous_stats(df, categorical_columns)
    categorical_data = [['Category', 'Statistic', 'Value']]
    for column in categorical_columns:
        categorical_stats = generate_categorical_stats(df, [column])
        for stat in categorical_stats.columns:
            categorical_data.append([column, stat, categorical_stats.at[column, stat]])

    categorical_table = Table(categorical_data)
    categorical_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('BOX', (0, 0), (-1, -1), 2, colors.black),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    story.append(categorical_table)
    
    story.append(PageBreak())
    
    created_files = []


    # Generate visualizations for continuous variables and add to the story
    for column in continuous_columns:
        fig = plt.figure(figsize=(6, 4))
        sns.histplot(df[column].dropna(), kde=True, bins=30)
        plt.title(f'Histogram of {column}')
        plt.xlabel(column)
        plt.ylabel('Frequency')
        plt.tight_layout()
        hist_filename = f'{column}_hist.png'
        plt.savefig(hist_filename)
        plt.close(fig)
        story.append(Image(hist_filename))
        created_files.append(hist_filename)

    # Generate visualizations for categorical variables and add to the story
    for column in categorical_columns:
        fig = plt.figure(figsize=(6, 4))
        sns.countplot(y=column, data=df, order=df[column].value_counts().index)
        plt.title(f'Count Plot of {column}')
        plt.xlabel('Frequency')
        plt.ylabel(column)
        plt.tight_layout()
        count_filename = f'{column}_count.png'
        plt.savefig(count_filename)
        plt.close(fig)
        story.append(Image(count_filename))
        created_files.append(count_filename)

    # Build the PDF with all the elements
    doc.build(story)
    
    # Now delete all the created image files
    for filename in created_files:
        os.remove(filename)

# Set the path to your CSV file and the output PDF file
csv_file_path = 'widsdatathon2024-university/fixed_gender.csv'
pdf_file_path = 'widsdatathon2024-university/data_quality_report_with_tables.pdf'

# Load the dataset
df = pd.read_csv(csv_file_path)

# Specify your continuous and categorical columns
continuous_columns = ['population', 'density']
categorical_columns = ['region', 'division', 'patient_zip3']

# Create the PDF with tables
print("creating pdf")
create_pdf_with_tables(df, continuous_columns, categorical_columns, pdf_file_path)