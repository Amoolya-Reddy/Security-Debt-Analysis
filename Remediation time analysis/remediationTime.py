import pandas as pd
import requests
import re
import matplotlib.pyplot as plt
from datetime import datetime
from openpyxl import load_workbook

# Function to extract CVE IDs
def extract_cve_ids(commit_msg):
    cve_pattern = r"CVE-\d{4}-\d{4,7}"
    return re.findall(cve_pattern, commit_msg)

def fetch_disclosure_date(cve_id, api_key):
    url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?cveId={cve_id}"
    headers = {"apiKey": api_key}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if 'vulnerabilities' in data and len(data['vulnerabilities'])>0:
                published_date = data['vulnerabilities'][0]['cve']['published']
                print(cve_id)
                print(published_date)
                dt = datetime.strptime(published_date, "%Y-%m-%dT%H:%M:%S.%f")
                # Adjust the date format string as per the actual format
                return dt.replace(tzinfo=None)
        elif response.status_code == 403:
            print(f"Access denied for {cve_id}. Check API key and rate limits.")
            return None
        else:
            print(f"Failed to fetch data for {cve_id}: HTTP {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request error for {cve_id}: {e}")
    except KeyError as e:
        print(f"Key error parsing data for {cve_id}: {e}")
    except ValueError as e:
        print(f"Value error parsing date for {cve_id}: {e}. Date received: ")
    return None


# API Key for NVD
api_key = "10bb829b-429b-42d8-9431-f6de9a13f8c9"

# Path to your Excel file
file_path = 'security_fixes.xlsx'

# Load the workbook and keep the formatting info
xls = pd.ExcelFile(file_path, engine='openpyxl')
sheet_names = xls.sheet_names

dfs = {sheet: pd.read_excel(xls, sheet_name=sheet, engine='openpyxl') for sheet in sheet_names}

# writer.book = book
# writer.sheets = dict((ws.title, ws) for ws in book.worksheets)
cve_disclosure_dates = {}
for sheet, df_commits in dfs.items():
    # Use pandas to read the current sheet    
    # Check if the sheet has rows (excluding header)
    if not df_commits.empty:
        df_commits['date'] = pd.to_datetime(df_commits['date'])
        

        # Iterate through each commit once
        for index, row in df_commits.iterrows():
            # Extract CVE IDs from the commit message
            cve_ids_in_commit = extract_cve_ids(row['msg'])
            
            for cve_id in cve_ids_in_commit:
                # Check if we've already fetched the disclosure date for this CVE ID
                if cve_id not in cve_disclosure_dates:
                    # Fetch disclosure date and store it in the dictionary
                    disclosure_date = fetch_disclosure_date(cve_id, api_key)
                    if disclosure_date:
                        cve_disclosure_dates[cve_id] = disclosure_date
                    else:
                        # If no date is found, continue to the next CVE ID
                        continue
                
                # Calculate remediation time for this commit and CVE ID
                disclosure_date = cve_disclosure_dates[cve_id]
                remediation_time = (row['date'] - disclosure_date).days
                df_commits.at[index, 'remediation_time_days'] = remediation_time
        dfs[sheet] = df_commits

# Write all DataFrames back to the Excel file
with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
    for sheet, df in dfs.items():
        df.to_excel(writer, sheet_name=sheet, index=False)