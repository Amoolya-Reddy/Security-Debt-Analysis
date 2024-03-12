from pydriller import Repository
import pandas as pd

# Define repositories
repositories = [
    'https://github.com/ashtom/logging-log4j2'
]

# The path to the Excel file you want to create/update
excel_file_path = 'security_fixes-origin.xlsx'

# Initialize ExcelWriter with the desired Excel file path
with pd.ExcelWriter(excel_file_path, engine='openpyxl') as writer:
    # Analyze each repository
    for repo_url in repositories:
        print(f"Mining repo: {repo_url}")
        commits_data = []  # Reset the list for each repository
        for commit in Repository(repo_url).traverse_commits():
            if 'CVE-' in commit.msg:
                commit_data = {
                    'repo': repo_url,
                    'hash': commit.hash,
                    'msg': commit.msg,
                    'date': commit.author_date.replace(tzinfo=None),
                    'author': commit.author.name
                }
                commits_data.append(commit_data)
        
        # Convert to DataFrame
        df_commits = pd.DataFrame(commits_data)
        
        # Define a sheet name based on the repository, e.g., by using the repo's name
        sheet_name = repo_url.split('/')[-1][:31]  # Sheet names limited to 31 characters
        
        # Save this repository's data to a sheet in the Excel file
        df_commits.to_excel(writer, sheet_name=sheet_name, index=False)
