import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import scipy.stats as stats

pd.options.display.float_format = '{:,.2f}'.format

# Create locators for ticks on the time axis
years = mdates.YearLocator()
months = mdates.MonthLocator()
years_fmt = mdates.DateFormatter('%Y')

# Register date converters to avoid warning messages
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()

# Read the Data
df_yearly = pd.read_csv('annual_deaths_by_clinic.csv')
# parse_dates avoids DateTime conversion later
df_monthly = pd.read_csv('monthly_deaths.csv',
                         parse_dates=['date'])
# Preliminary Data Exploration

print("What is the shape of df_yearly and df_monthly? How many rows and columns?")
print(df_yearly.shape)
print(df_yearly)
print(df_monthly.shape)
print("What are the column names?")
print(df_yearly.columns)
print(df_monthly.columns)
print("Which years are included in the dataset?")
print(df_yearly['year'].unique())
print("Are there any NaN values or duplicates?")
print(df_yearly.info())
print(df_monthly.info())
print(f'Any yearly NaN values? {df_monthly.isna().values.any()}')
print(f'Any monthly NaN values? {df_yearly.isna().values.any()}')
print(f'Any yearly duplicates? {df_yearly.duplicated().values.any()}')
print(f'Any monthly duplicates? {df_monthly.duplicated().values.any()}')
print("What were the average number of births that took place per month?")
print(df_monthly.groupby('date')['births'].mean())
print("What were the average number of deaths that took place per month?")
print(df_monthly.groupby('date')['deaths'].mean())

# Descriptive Statistics
print(df_monthly.describe())
print(df_yearly.describe())

# Percentage of Women Dying in Childbirth
print("The percentage of women giving birth who died throughout the 1840s at the hospital."
      "In comparison, the United States recorded 18.6 maternal deaths per 100,000 or 0.018% in 2023")
prob = df_yearly.deaths.sum() / df_yearly.births.sum() * 100
print(f'Chances of dying in the 1840s in Vienna: {prob:.3}%')

# Visualise the Total Number of Births and Deaths over Time

plt.figure(figsize=(10, 6), dpi=200)
plt.title('Total Number of Monthly Births and Deaths', fontsize=18)
plt.yticks(fontsize=14)
plt.xticks(fontsize=14, rotation=45)

ax1 = plt.gca()
ax2 = ax1.twinx()

ax1.set_ylabel('Births', color='skyblue', fontsize=18)
ax2.set_ylabel('Deaths', color='crimson', fontsize=18)

# Add locators for tick marks
ax1.set_xlim([df_monthly.date.min(), df_monthly.date.max()])
ax1.xaxis.set_major_locator(years)
ax1.xaxis.set_major_formatter(years_fmt)
ax1.xaxis.set_minor_locator(months)

ax1.grid(color='grey', linestyle='--')

ax1.plot(df_monthly.date,
         df_monthly.births,
         color='skyblue',
         linewidth=3)

ax2.plot(df_monthly.date,
         df_monthly.deaths,
         color='crimson',
         linewidth=2,
         linestyle='--')
# TODO: Descomentar todos los .show;
# plt.show()


# The Yearly Data Split by Clinic

line = px.line(df_yearly,
               x='year',
               y='births',
               color='clinic',
               title='Total Yearly Births by Clinic')

# line.show()

line2 = px.line(df_yearly,
                x='year',
                y='deaths',
                color='clinic',
                title='Total Yearly Deaths by Clinic')

# line2.show()

# Calculate the Proportion of Deaths at Each Clinic
df_yearly['pct_deaths'] = df_yearly.deaths / df_yearly.births
clinic_1 = df_yearly[df_yearly.clinic == 'clinic 1']
avg_c1 = clinic_1.deaths.sum() / clinic_1.births.sum() * 100
print(f'Average death rate in clinic 1 is {avg_c1:.3}%.')

clinic_2 = df_yearly[df_yearly.clinic == 'clinic 2']
avg_c2 = clinic_2.deaths.sum() / clinic_2.births.sum() * 100
print(f'Average death rate in clinic 2 is {avg_c2:.3}%.')

# Plotting the Proportion of Yearly Deaths by Clinic
line = px.line(df_yearly,
               x='year',
               y='pct_deaths',
               color='clinic',
               title='Proportion of Yearly Deaths by Clinic')

# line.show()


"""The Effect of Handwashing
Dr Semmelweis made handwashing obligatory in the summer of 1947. 
In fact, he ordered people to wash their hands with clorine (instead of water)."""

# Date when handwashing was made mandatory
handwashing_start = pd.to_datetime('1847-06-01')

# Add a column called "pct_deaths" to df_monthly that has the percentage of deaths per birth for each row.
df_monthly['pct_deaths'] = df_monthly.deaths/df_monthly.births
# Create two subsets from the df_monthly data: before and after Dr Semmelweis ordered washing hand.
before_washing = df_monthly[df_monthly.date < handwashing_start]
after_washing = df_monthly[df_monthly.date >= handwashing_start]
# Calculate the average death rate prior to June 1947.
bw_rate = before_washing.deaths.sum() / before_washing.births.sum() * 100
print(f'Average death rate before 1847 was {bw_rate:.4}%')

# Calculate the average death rate after June 1947.
aw_rate = after_washing.deaths.sum() / after_washing.births.sum() * 100

print(f'Average death rate AFTER 1847 was {aw_rate:.3}%')

# Calculate a Rolling Average of the Death Rate
roll_df = before_washing.set_index('date')
roll_df = roll_df.rolling(window=6).mean()
print(roll_df)


# Highlighting Subsections of a Line Chart

plt.figure(figsize=(14,8), dpi=200)
plt.title('Percentage of Monthly Deaths over Time', fontsize=18)
plt.yticks(fontsize=14)
plt.xticks(fontsize=14, rotation=45)

plt.ylabel('Percentage of Deaths', color='crimson', fontsize=18)

ax = plt.gca()
ax.xaxis.set_major_locator(years)
ax.xaxis.set_major_formatter(years_fmt)
ax.xaxis.set_minor_locator(months)
ax.set_xlim([df_monthly.date.min(), df_monthly.date.max()])

plt.grid(color='grey', linestyle='--')

ma_line, = plt.plot(roll_df.index,
                    roll_df.pct_deaths,
                    color='crimson',
                    linewidth=3,
                    linestyle='--',
                    label='6m Moving Average')
bw_line, = plt.plot(before_washing.date,
                    before_washing.pct_deaths,
                    color='black',
                    linewidth=1,
                    linestyle='--',
                    label='Before Handwashing')
aw_line, = plt.plot(after_washing.date,
                    after_washing.pct_deaths,
                    color='skyblue',
                    linewidth=3,
                    marker='o',
                    label='After Handwashing')

plt.legend(handles=[ma_line, bw_line, aw_line],
           fontsize=18)

# plt.show()

# Statistics - Calculate the Difference in the Average Monthly Death Rate

# What was the average percentage of monthly deaths before handwashing?
avg_prob_before = before_washing.pct_deaths.mean() * 100
print(f'Chance of death during childbirth before handwashing: {avg_prob_before:.3}%.')
# What was the average percentage of monthly deaths after handwashing was made obligatory?
avg_prob_after = after_washing.pct_deaths.mean() * 100
print(f'Chance of death during childbirth AFTER handwashing: {avg_prob_after:.3}%.')
# By how much did handwashing reduce the average chance of dying in childbirth in percentage terms?
mean_diff = avg_prob_before - avg_prob_after
print(f'Handwashing reduced the monthly proportion of deaths by {mean_diff:.3}%!')
# How many times lower are the chances of dying after handwashing compared to before?
times = avg_prob_before / avg_prob_after
print(f'This is a {times:.2}x improvement!')

# Use Box Plots to Show How the Death Rate Changed Before and After Handwashing
df_monthly['washing_hand'] = np.where(df_monthly.date < handwashing_start, "No", "Yes")

box = px.box(df_monthly,
             x='washing_hand',
             y='pct_deaths',
             color='washing_hand',
             title='How Have the Stats Changed with Handwashing?')
box.update_layout(xaxis_title="Washing Hands?",
                  yaxis_title='Percentage of Monthly Deaths')

# box.show()

# Use Histograms to Visualise the Monthly Distribution of Outcomes

hist = px.histogram(df_monthly,
                    x='pct_deaths',
                    color='washing_hand',
                    nbins=30,
                    opacity=0.4,
                    barmode='overlay',
                    histnorm='percent',
                    marginal='box')
hist.update_layout(xaxis_title='Proportion of Monthly Deaths',
                   yaxis_title='Count',)

# hist.show()

# Use a Kernel Density Estimate (KDE) to visualise a smooth distribution

plt.figure(dpi=200)
plt.figure(dpi=200)
sns.kdeplot(before_washing.pct_deaths,
            fill=True,
            clip=(0,1))
sns.kdeplot(after_washing.pct_deaths,
            fill=True,
            clip=(0,1))
plt.title('Est. Distribution of Monthly Death Rate Before and After Handwashing')
plt.xlim(0, 0.40)
# plt.show()

# Use a T-Test to Show Statistical Significance

t_stat,p_value = stats.ttest_ind(a=before_washing.pct_deaths,
                                 b=after_washing.pct_deaths)
print(f'p-palue is {p_value:.10f}')
print(f't-statstic is {t_stat:.4}')