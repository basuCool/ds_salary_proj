import pandas as pd

df = pd.read_csv('glassdoor_data.csv')

# salary parsing
# Remove row with no salary info
df =df[df['Salary Estimate']!='-1']
df = df.dropna()

df['hourly'] = df['Salary Estimate'].apply(lambda x: 1 if 'per hour' in x.lower() else 0)
df['employer_provided'] = df['Salary Estimate'].apply(lambda x: 1 if 'employer provided salary:' in x.lower() else 0)

salary = df['Salary Estimate'].apply(lambda x: x.split('(')[0])
salary_minus_kd = salary.apply(lambda x: x.replace('K', '').replace('$',''))

salary_minus_kd_min_hr = salary_minus_kd.apply(lambda x: x.lower().replace('employer provided salary:', '').replace('per hour',''))

df['min_salary'] = salary_minus_kd_min_hr.apply(lambda x: int(x.split('-')[0]))
df['max_salary'] = salary_minus_kd_min_hr.apply(lambda x: int(x.split('-')[1]))
df['average_salary'] = (df.min_salary + df.max_salary)/2

# company name
df['comp_text'] = df['Company Name']

for i in df['Unnamed: 0']:        
    if df['Rating'][i]<0:
        df['comp_text'][i] = df['Company Name'][i]
    else:
        df['comp_text'][i] = df['Company Name'][i][:-3]

# state field
df['job_state'] = df['Location'].apply(lambda x: x.split(',')[1])
df.job_state.value_counts()
df['same_state'] = df.apply(lambda x: 1 if x.Location == x.Headquarters else 0, axis=1)
# age of the company
df['age_comp'] = df.Founded.apply(lambda x: x if x<0 else 2021-x)
# parsing of skill sets from job description.
#python
df['python'] = df['Job Description'].apply(lambda x: 1 if 'python' in x.lower() else 0)
#r studio
df['R_studio'] = df['Job Description'].apply(lambda x: 1 if 'r-studio' in x.lower() else 0)
#Spark
df['Spark'] = df['Job Description'].apply(lambda x: 1 if 'spark' in x.lower() else 0)
#aws
df['aws'] = df['Job Description'].apply(lambda x: 1 if 'aws' in x.lower() else 0)
#excel
df['excel'] = df['Job Description'].apply(lambda x: 1 if 'excel' in x.lower() else 0)

df_new = df.drop('Unnamed: 0', axis=1)

df_new.to_csv('Salary_data_cleaned.csv', index=False)

df2 = pd.read_csv('Salary_data_cleaned.csv')