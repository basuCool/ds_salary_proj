import pandas as pd
import glassdoorScraper as gs

df = pd.read_csv('dataset.csv', engine='python', encoding='utf-8', error_bad_lines=False)
