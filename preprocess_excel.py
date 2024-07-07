import pandas as pd

# Load the Excel file
df = pd.read_excel('data/files/BIAN v12 asset(SD).xlsx', sheet_name='Service Domain')
print(df.columns)

# Select the desired columns
select_columns = df[['Service Domain', 'Business Area', 'Business Domain',
       'functionalPattern', 'assetType', 'genericArtefactType', 'Examples Of Use', 'Role Definition']]

print(select_columns)

select_columns.to_csv('data/files/BIAN v12 asset(SD).csv', encoding='utf8', index=False)