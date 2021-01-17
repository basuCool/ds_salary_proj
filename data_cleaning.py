import pandas as pd

df_org = pd.read_csv('glassdoor_data.csv')

# salary parsing
# Remove row with no salary info
df =df_org[df_org['Salary Estimate']!='-1']
df.dropna(inplace=True)

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

#Remove useless column
df.drop('Unnamed: 0', inplace=True,axis=1)

# Job title and seniority renaming
def title_simplifier(title):
    if 'data scientist' in title.lower():
        return 'data scientist'
    elif 'data engineer' in title.lower():
        return 'data engineer'
    elif 'analyst' in title.lower():
        return 'analyst'
    elif 'machine learning' in title.lower():
        return 'mle'
    elif 'manager' in title.lower():
        return 'manager'
    elif 'director' in title.lower():
        return 'director'
    else:
        return 'na'

def seniority(title):
    if 'sr' in title.lower() or 'sr.' in title.lower() or'senior' in title.lower() or 'lead' in title.lower() or 'principal' in title.lower():
        return 'senior'
    elif 'junior' in title.lower() or 'jr.' in title.lower():
        return 'jr'
    else:
        return 'na'

df['job_simp'] = df['Job Title'].apply(title_simplifier)
df['job_seniority'] = df['Job Title'].apply(seniority)

#fix state Los Angeles
df['job_state'] = df['job_state'].apply(lambda x: ' CA' if 'los angeles' in x.lower() else x)
#df.to_csv('Salary_data_cleaned.csv', index=False)
# job desc length
df['desc_len'] = df['Job Description'].apply(lambda x: len(x))
# competitor count
df['competitors_count'] = df['Competitors'].apply(lambda x: 0 if '-1' in x else (1 + x.count(',')))

#resetting the index of df_new
df_all = df.reset_index(drop=True)

#Convert hourly wage to annual wage (hourly wage * 40 hrs per week * 52 week. 2080*hourly wage) 
for i in df_all.index:        
    if df_all['hourly'][i] == 1:
        df_all['average_salary'][i] = df_all['average_salary'][i]*2.08
        
#Remove \r\n from comp text
df_all['comp_text'] = df_all['comp_text'].apply(lambda x: x.rstrip())
#Save df to csv        
df_all.to_csv('Salary_data_cleaned_full.csv', index=False)

df2 = pd.read_csv('Salary_data_cleaned_full.csv')