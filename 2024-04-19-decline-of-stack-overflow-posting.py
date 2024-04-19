import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, date

# Load the data from a CSV file, parsing 'date' column as dates and setting it as index
df = pd.read_csv('data/site_data/posts_2008-Sep-15_2024-Apr-18.csv', parse_dates=['date'],
                 usecols=['date', 'all posts'], index_col='date')

# Filter the data to include only entries from 2020 onwards
df_2020 = df.loc['2020':]

# Find the date with the most posts in the filtered data
max_2020 = pd.Timestamp(df_2020.idxmax().values[0]).date()

# Adjust df_2020 to show only data from the date with most posts onwards
df_2020 = df_2020.loc[max_2020:]

# Resample the data to 3-month periods and calculate the mean for each period
df_resampled = df_2020.resample('3ME').mean()

# Calculate the percent change for each period
df_percent_change = df_resampled.pct_change().mul(100)

# Set the index to be the date component only
df_percent_change.index = df_percent_change.index.date

# Calculate the cumulative percent change and convert it to percentage
df_cumulative_percent_change = df_percent_change.cumsum()

# Create a subplot with 3 rows
fig, (ax0, ax1, ax2, ax3) = plt.subplots(nrows=4, figsize=(12, 15), tight_layout=True)

# Plot the entire data on the first subplot
ax0.plot(df, label='')
ymin, ymax = ax0.get_ylim()
ax0.vlines(x=max_2020, ymin=ymin, ymax=df_2020.max(), label=f'{max_2020}\nCOVID Max', colors='k')

# Plot the filtered data on the second subplot
ax1.plot('date', 'all posts', data=df_2020.reset_index(), label='')

# Plot the cumulative percent change as a bar chart on the third subplot
ax2.bar(x='index', height='all posts', width=10, data=df_percent_change.reset_index(), label='')

# Add labels to the bars on the third subplot
ax2.bar_label(ax2.containers[0], padding=2, fmt='%.1f%%')

# Bar Plot the cumulative percent change as a line chart on the fourth subplot
ax3.bar(x='index', height='all posts', width=10, data=df_cumulative_percent_change.reset_index(), label='')

# Add labels to the bars on the fourth subplot
ax3.bar_label(ax3.containers[0], padding=2, fmt='%.1f%%')

# Define the date when ChatGPT went live
chatGPT_day = datetime.strptime('2022-11-30', '%Y-%m-%d')

# Add a vertical line on the third subplot at the date when ChatGPT went live
ax2.vlines(x=chatGPT_day, ymin=df_percent_change.loc[date(2022, 11, 30), 'all posts'],
           ymax=0, label='ChatGPT Live', colors='r')

# Add a vertical line on the fourth subplot at the date when ChatGPT went live
ax3.vlines(x=chatGPT_day, ymin=df_cumulative_percent_change.loc[date(2022, 11, 30), 'all posts'],
           ymax=0, label='ChatGPT Live', colors='r')

# Add a vertical line on the first and second subplots at the date when ChatGPT went live
for ax in [ax0, ax1]:
    ymin, _ = ax.get_ylim()
    ymax = df.loc[chatGPT_day, 'all posts']
    ax.vlines(x=chatGPT_day, ymin=ymin, ymax=ymax, label='ChatGPT Live', colors='r')
    # add a line for the date when GPT-3 went live
    ax.vlines(x=datetime.strptime('2020-06-11', '%Y-%m-%d'), ymin=ymin,
              ymax=df.loc['2020-06-11', 'all posts'], label='GPT-3 Live', colors='tab:orange')
    # add a line for the date of stack overflow's 2023-10-16 layoffs
    ax.vlines(x=datetime.strptime('2023-10-16', '%Y-%m-%d'), ymin=ymin,
              ymax=df.loc['2023-10-16', 'all posts'], label='28% of staff laid off', colors='tab:purple')
    ax.legend(frameon=False)

# Set margins for the first and second subplots
ax0.margins(x=0, y=0)
ax1.margins(y=0)
ax2.margins(y=0.1)
ax3.margins(y=0.1)

# Set limits for the x and y axes of the subplots
ax0.set_ylim(bottom=0)
ax0.set_xlim(left=df.index.min(), right=df.index.max())
ax1.set_xlim(left=df_2020.index.min(), right=df_2020.index.max())
ax2.set_xlim(left=df_2020.index.min(), right=df_2020.index.max())
ax3.set_xlim(left=df_2020.index.min(), right=df_2020.index.max())

# Set titles and y-labels for the subplots
ax0.set(title='Total Number of Posts Over Time', ylabel='Number of Posts')
ax1.set(title='Number of Posts Since Peak in 2020', ylabel='Number of Posts')
ax2.set(title='Percentage Change in Posts Every 3 Months', ylabel='% Change')
ax3.set(title='Cumulative Percentage Change in Posts Every 3 Months', ylabel='% Change')

# Add a suptitle to the figure
_ = fig.suptitle('Analysis of Stack Overflow Posting Trends', fontsize=16)

# Save the plot as a PNG file
plt.savefig('2024-04-19-decline-of-stack-overflow-posting.png')

# Display the plot
plt.show()
