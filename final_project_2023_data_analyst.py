# -*- coding: utf-8 -*-
"""FINAL PROJECT 2023 - DATA ANALYST

## **Import Data and Libraries**

Dataset: World Happiness Report

The dataset contains ...

**Questions:**

- How has happiness evolved over time globally, and within specific
countries?
- Are there any trends in happiness scores within specific regions?
- What are the key differences between the top and bottom ranked countries in terms of happiness?
- Is there a correlation between government policies and happiness scores?
"""

# Preprocessing:
# 1. Consolidate columns from all dataframe through years
# - (rename, replace)
# - create a column to store information about year: df['year'] = 2019 
# 2. Country and region mismatch
# - take df2016 --> list_of_standard_countries 
# - standardize all other dataframes to have the same list of countries and regions. E.g. 2019 --> split column "country or region" to 2 separate columns 
# 3. concatenate all dataframes

# Table of content:
# 1. Overall: world map with score (latest - 2019) --> highest score regions / countries
# 2. Trend through time -- lineplot (X: years / y: happiness score / hue: country)
# 3. [External research] Predefined model for scoring --> correlation with Score (barplot): clarify the most/least important features 
# 4. Top/bottom 5 scored countries --> compare these countries in terms of other features --> common characteristics / best practices / outliers(such as freedom in top bottom ...)

##load data from drive to colab
from google.colab import drive
drive.mount('/content/drive')

import seaborn as sns #plotting
import matplotlib.pyplot as plt #plotting
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import numpy as np # linear algebra


##Load data directly from Drive: 2015-2019
df19 = pd.read_csv("https://drive.google.com/uc?id=1Bv5i3zpDRjv3FySpdyXgQCTKZSvSw9yc")
df18 = pd.read_csv("https://drive.google.com/uc?id=1SANykWoI4RY1zoRIhRkTJHmP1E72nHMV")
df17 = pd.read_csv("https://drive.google.com/uc?id=1h0VYTGI4ye9VLqXewNUAl0HXfBp-GaR2")
df16 = pd.read_csv("https://drive.google.com/uc?id=1zjuErGs--fJQefjgz8Qmxc6LZSJ3z1Dq")
df15 = pd.read_csv("https://drive.google.com/uc?id=1-UZ_DVWh47KvllwArbSMvI7z0Wt6a52J")

##Drop unnecessary columns in period of 2015-2017 to ensure consitency in column names for 5 years
df17.drop(columns=["Whisker.high", "Whisker.low"], inplace=True)
df16.drop(columns=["Lower Confidence Interval", "Upper Confidence Interval"], inplace=True)
df15.drop(columns=["Standard Error"], inplace=True)

##Rename column
df19 = df19.rename(columns={
    "Overall rank": "Rank",
    "Country or region": "Country",
    "Freedom to make life choices": "Freedom"})
df18 = df18.rename(columns={
    "Overall rank": "Rank",
    "Country or region": "Country",
    "Freedom to make life choices":"Freedom"})
df17 = df17.rename(columns={
    "Happiness.Rank":"Rank",
    "Happiness.Score":"Score",
    "Economy..GDP.per.Capita.": "GDP per capita",
    "Family": "Social support",
    "Health..Life.Expectancy.":"Healthy life expectancy",
    "Trust..Government.Corruption.":"Perceptions of corruption"})
df16 = df16.rename(columns={
    "Happiness Rank":"Rank",
    "Happiness Score":"Score",
    "Economy (GDP per Capita)": "GDP per capita",
    "Family": "Social support",
    "Health (Life Expectancy)":"Healthy life expectancy",
    "Trust (Government Corruption)":"Perceptions of corruption"})
df15= df15.rename(columns={
    "Happiness Rank":"Rank",
    "Happiness Score":"Score",
    "Economy (GDP per Capita)": "GDP per capita",
    "Family": "Social support",
    "Health (Life Expectancy)":"Healthy life expectancy",
    "Trust (Government Corruption)":"Perceptions of corruption"})

#Re-order columns: 2015-2017
standard_col_list = ["Rank",
                     "Country",
                     "Score",
                     "GDP per capita",
                     "Social support",
                     "Healthy life expectancy",
                     "Freedom",
                     "Generosity",
                     "Perceptions of corruption"]

df15, df16, df17 = df15[standard_col_list], df16[standard_col_list], df17[standard_col_list]


##Add column year
df19.insert(0, 'Year', 2019)
df18.insert(0, 'Year', 2018)
df17.insert(0, 'Year', 2017)
df16.insert(0, 'Year', 2016)
df15.insert(0, 'Year', 2015)

#Concacenate
df=pd.concat([df19, df18, df17, df16, df15])

#Reset row indexes
df = df.reset_index(drop=True)

#Check null
df.isnull().sum() # There is 1 null value in Perceptions of corruption column
mean_value = df["Perceptions of corruption"].mean()
df["Perceptions of corruption"].fillna(mean_value, inplace=True) #Replace by mean value

## **Exploratory Data Analysis**

#**Overall: world map with score (latest - 2019) --> highest score regions / countries**
"""

#1. Where do happiest people live?
#Using Tableau to show the world map: Happiness score around the world. Required csv file for Tableau is exported from Colab
df.to_excel("df.xlsx", index=False) #index=False, the row index is not included in the exported file

#Check the location of exported file
import os
file_name = "df.xlsx"
file_path = os.path.abspath(file_name)
print("Location:")
print(file_path)

#Using Tableau to show rank of top & bottom 10
df19.to_excel("df19.xlsx", index=False)

from google.colab import drive
drive.mount('/content/drive')

#2. Trend: How has happiness evolved over time globally and within specific countries?
# DEFINITION: top / bottom based on average 5 years --> slide
#top_countries = df.groupby("Country")["Score"].mean().sort_values()# --> country | score
#sns.lineplot(data=df[df["Country"].isin(top_countries)], x="Year", y="Score", hue="Country")


#2 DEFINITION: top / bottom based on average 5 years --> slide
#Top_countries are countries having the highest happiness scores and the annual happiness score from 2015 to 2019  should be also in top list
#Similarly, Bottom_countries are countries having the lowest happiness scores and the annual happiness score from 2015 to 2019 should be also in bottom list


#Set up the theme
sns.set_theme(style="ticks", palette="colorblind")

#Visualize
plt.figure(figsize=(15,5))
plt.subplot(121)
#Creating line chart to choose top 5 countries in list of top 10 countries
top10_countries = df.groupby(["Country"])["Score"].mean().sort_values(ascending=False).head(10).reset_index()
top10_countries = top10_countries["Country"].tolist()
sns.lineplot(data=df[df["Country"].isin(top10_countries)], x="Year", y="Score", hue="Country")
#Adjust labels on x axis & customize the plot
plt.xticks(ticks=list(range(2015, 2020)),fontsize=10)
plt.yticks(fontsize=10)
plt.xlabel("Year", fontsize=10)
plt.ylabel("Happiness Score", fontsize=10)
plt.title("Top 10 Happiest Countries", fontsize=12)
#Adjust position of legend
plt.legend(title="Country", loc="upper right", fontsize=8, title_fontsize=10)

plt.subplot(122)
#Creating line chart to choose bottom 5 countries in list of 10 countries having the lowest happiness score
bottom10_countries = df.groupby(["Country"])["Score"].mean().sort_values().head(10).reset_index()
bottom10_countries = bottom10_countries["Country"].tolist()
sns.lineplot(data=df[df["Country"].isin(bottom10_countries)], x="Year", y="Score", hue="Country")
#Adjust labels on x axis & customize the plot
plt.xticks(ticks=list(range(2015, 2020)),fontsize=10)
plt.yticks(fontsize=10)
plt.xlabel("Year", fontsize=10)
plt.ylabel("Happiness Score", fontsize=10)
plt.title("Bottom 10 Happiest Countries", fontsize=12)
#Adjust position of legend
plt.legend(title="Country", loc="upper right",fontsize=8, title_fontsize=10)

plt.suptitle("Trend of Happiness Score (2015-2019)", fontsize=14)
plt.show()

#From above charts, we can select top 5 and bottom 5 countries for further analysis.
top_countries=["Denmark","Norway","Finland","Switzerland","Iceland"]
bottom_countries=["Burundi","Central African Republic", "Syria", "Rwanda", "Tanzania"]

#Set up the theme
sns.set_theme(style="ticks", palette="colorblind")

#Visualize
plt.figure(figsize=(15,5))

plt.subplot(121)
sns.lineplot(data=df[df["Country"].isin(top_countries)], x="Year", y="Score", hue="Country")
#Adjust labels on x axis&customize the plot
plt.xticks(ticks=list(range(2015, 2020)),fontsize=10)
plt.yticks(fontsize=10)
plt.xlabel("Year", fontsize=10)
plt.ylabel(" Happiness Score", fontsize=10)
#Adjust position of legend
plt.title("Top 5 Happiest Countries", fontsize=12)
plt.legend(title="Country", loc="lower right",fontsize=8, title_fontsize=10)

plt.subplot(122)
sns.lineplot(data=df[df["Country"].isin(bottom_countries)], x="Year", y="Score", hue="Country")
#Adjust labels on x axis
list(range(2015, 2020, 1))
plt.xticks(ticks=list(range(2015, 2020)),fontsize=10)
plt.yticks(fontsize=10)
plt.xlabel("Year", fontsize=10)
plt.ylabel("Happiness Score", fontsize=10)
plt.title("Bottom 5 Happiest Countries", fontsize=12)
#Adjust position of legend
plt.legend(title="Country", loc="lower right",fontsize=8, title_fontsize=10)

plt.suptitle("Trend of Happiness Score (2015-2019)", fontsize=14)
plt.show()

#3. Factors affect our happiness in general
feature_list = ["Score","GDP per capita", "Social support", "Healthy life expectancy", "Freedom", "Generosity","Perceptions of corruption"]
# Create correlation matrix
corr_matrix = df[feature_list].corr()

# Plot heatmap of correlations
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', linewidths=2, fmt=" .2f")
plt.title("Correlation heatmap of happiness features", fontsize=14)
plt.show()

from numpy.ma import left_shift
plt.figure(figsize=(15, 5))

plt.subplot(141)
sns.regplot(x="GDP per capita", y="Score",data = df, line_kws={"color":"black"})
sns.scatterplot(data=df, x="GDP per capita", y="Score", hue="Country", legend=False)
plt.xlabel("GDP per capita", fontsize=10)
plt.ylabel("Happiness Score", fontsize=10)

plt.subplot(142)
sns.regplot(x="Healthy life expectancy", y="Score",data = df, line_kws={"color":"black"})
sns.scatterplot(data=df, x="Healthy life expectancy", y="Score", hue="Country", legend=False)
plt.xlabel("Healthy life expectancy", fontsize=10)
plt.ylabel("Happiness Score", fontsize=10)

plt.subplot(143)
sns.regplot(x="Social support", y="Score",data = df, line_kws={"color":"black"})
sns.scatterplot(data=df, x="Social support", y="Score",hue="Country", legend=False)
plt.xlabel("Social support", fontsize=10)
plt.ylabel("Happiness Score", fontsize=10)

plt.subplot(144)
sns.regplot(x="Freedom", y="Score",data = df, line_kws={"color":"black"})
sns.scatterplot(data=df, x="Freedom", y="Score", hue="Country", legend=False)
plt.xlabel("Freedom", fontsize=10)
plt.ylabel('Happiness Score', fontsize=10)

plt.suptitle('Correlation between GDP per capita, Social support, Healthy life expectancy, Freedom and Happiness Score (by Country)', fontsize=14)
plt.show()

#Correlation between GDP and Healthy to conclude: richer countries have higher average level of happiness
from numpy.ma import left_shift
plt.figure(figsize=(20, 5))

plt.subplot(143)
sns.regplot(x="GDP per capita", y="Healthy life expectancy",data = df, line_kws={"color":"black"})
sns.scatterplot(data=df, x="GDP per capita", y="Healthy life expectancy", hue="Country", legend=False)
plt.xlabel("GDP per capita", fontsize=10)
plt.ylabel("Healthy life expectancy", fontsize=10)
plt.title("Correlation between GDP per capital and Healthy life expectancy")

#4. Top/bottom 5 scored countries --> compare these countries in terms of other features --> common characteristics / best practices / outliers(such as freedom in top bottom ...)

# Filter the data for the top & bottom countries only
top_filtered_data = df[df["Country"].isin(top_countries)]
bottom_filtered_data = df[df["Country"].isin(bottom_countries)]

#Calculate correlations between "Score" and other features in top & bottom 5 lists
feature_list = ["GDP per capita", "Social support", "Healthy life expectancy", "Freedom", "Generosity","Perceptions of corruption"]
top_countries_correlations = top_filtered_data[feature_list].corrwith(top_filtered_data["Score"]) # Pandas.Series
bottom_countries_correlations = bottom_filtered_data[feature_list].corrwith(bottom_filtered_data["Score"]) # Pandas.Series

#Set up the theme
sns.set_theme(style="ticks", palette="deep")

#Visualize
plt.figure(figsize=(15,5))

plt.subplot(121)
# Plot the correlations using a barplot for Top countries
top_countries_correlations.plot(kind='bar')
plt.ylabel("Correlation coefficient")
plt.title("Top 5 countries")
plt.xticks(rotation=45)

plt.subplot(122)
# Plot the correlations using a barplot for bottom countries
bottom_countries_correlations.plot(kind='bar')
plt.ylabel("Correlation coefficient")
plt.title('Bottom 5 countries')
plt.xticks(rotation=45)

plt.suptitle("Correlations between Happiness Score and other features", fontsize=14)
plt.tight_layout()  # Adjust spacing between subplots
plt.show()

top_filtered_data = df[df["Country"].isin(top_countries)]
bottom_filtered_data = df[df["Country"].isin(bottom_countries)]

#Calculate correlations between "Score" and other features in top & bottom 5 lists
feature_list = ["GDP per capita", "Social support", "Healthy life expectancy", "Freedom", "Generosity","Perceptions of corruption"]
top_countries_correlations = top_filtered_data[feature_list].corrwith(top_filtered_data["Score"]) # Pandas.Series
bottom_countries_correlations = bottom_filtered_data[feature_list].corrwith(bottom_filtered_data["Score"]) # Pandas.Series

#Set up the theme
sns.set_theme(style="ticks", palette="deep")

#Visualize
plt.figure(figsize=(20,8))

plt.subplot(121)
# Plot the correlations using a barplot for Top countries
ax_top = sns.barplot(x=top_countries_correlations.index, y=top_countries_correlations.values.flatten())
plt.ylabel("Correlation coefficient")
plt.title("Top 5 countries")
plt.xticks(rotation=45)
for i in ax_top.containers:
  ax_top.bar_label(i, fmt="%.2f")

plt.subplot(122)
# Plot the correlations using a barplot for bottom countries
#bottom_countries_correlations.plot(kind='bar')
ax_bottom = sns.barplot(x=bottom_countries_correlations.index, y=bottom_countries_correlations.values.flatten())
plt.ylabel("Correlation coefficient")
plt.title('Bottom 5 countries')
plt.xticks(rotation=45)
for j in ax_bottom.containers:
  ax_bottom.bar_label(j, fmt="%.2f")

plt.suptitle("Correlations between Happiness Score and other features", fontsize=14)
plt.tight_layout()  # Adjust spacing between subplots
plt.show()

#Show correlation for each year
years = df['Year'].unique()
top_countries=["Denmark","Norway","Finland","Switzerland","Iceland"]
bottom_countries=["Burundi","Central African Republic", "Syria", "Rwanda", "Tanzania"]
feature_list = ["GDP per capita", "Social support", "Healthy life expectancy", "Freedom", "Generosity","Perceptions of corruption"]
# Visualize correlations for each year
for year in years:
    # Filter the data for the specific year and top/bottom countries
    year_data = df[df['Year'] == year]
    top_filtered_data = year_data[year_data['Country'].isin(top_countries)]
    bottom_filtered_data = year_data[year_data['Country'].isin(bottom_countries)]

    # Calculate correlations between "Score" and other features for top/bottom countries
    top_countries_correlations = top_filtered_data[feature_list].corrwith(top_filtered_data['Score'])
    bottom_countries_correlations = bottom_filtered_data[feature_list].corrwith(bottom_filtered_data['Score'])

    # Visualize correlations using bar plots
    plt.figure(figsize=(15, 5))

    plt.subplot(121)
    top_countries_correlations.plot(kind='bar')
    plt.ylabel("Correlation coefficient")
    plt.title(f"Top 5 countries - {year}")
    plt.xticks(rotation=45)

    plt.subplot(122)
    bottom_countries_correlations.plot(kind='bar')
    plt.ylabel("Correlation coefficient")
    plt.title(f"Bottom 5 countries - {year}")
    plt.xticks(rotation=45)

    plt.suptitle(f"Correlations between Happiness Score and other features - {year}", fontsize=14)
    plt.tight_layout()
    plt.show()
