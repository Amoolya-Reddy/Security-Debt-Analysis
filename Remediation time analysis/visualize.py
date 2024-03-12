import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('security_fixes_cve.csv')

# Ensure 'date' is converted to datetime
df['date'] = pd.to_datetime(df['date'])

# Set 'date' as the index of the DataFrame
df.set_index('date', inplace=True)

# Verify the index is a DatetimeIndex
print(df.index)
# Resample by month and count commits
monthly_commits = df.resample('M')['value'].size()

# Plotting
plt.figure(figsize=(12, 6))
monthly_commits.plot(kind='line', marker='o', color='tomato')
plt.title('Frequency of Security-Related Updates Over Time')
plt.xlabel('Month/Year')
plt.ylabel('Number of Security-Related Commits')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
