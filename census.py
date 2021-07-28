# Open Sublime text editor, create a new Python file, copy the following code in it and save it as 'census_app.py'.

# Import modules
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

@st.cache()
def load_data():
	# Load the Adult Income dataset into DataFrame.

	df = pd.read_csv('https://student-datasets-bucket.s3.ap-south-1.amazonaws.com/whitehat-ds-datasets/adult.csv', header=None)
	df.head()

	# Rename the column names in the DataFrame using the list given above. 

	# Create the list
	column_name =['age', 'workclass', 'fnlwgt', 'education', 'education-years', 'marital-status', 'occupation', 'relationship', 'race','gender','capital-gain', 'capital-loss', 'hours-per-week', 'native-country', 'income']

	# Rename the columns using 'rename()'
	for i in range(df.shape[1]):
	  df.rename(columns={i:column_name[i]},inplace=True)

	# Print the first five rows of the DataFrame
	df.head()

	# Replace the invalid values ' ?' with 'np.nan'.

	df['native-country'] = df['native-country'].replace(' ?',np.nan)
	df['workclass'] = df['workclass'].replace(' ?',np.nan)
	df['occupation'] = df['occupation'].replace(' ?',np.nan)

	# Delete the rows with invalid values and the column not required 

	# Delete the rows with the 'dropna()' function
	df.dropna(inplace=True)

	# Delete the column with the 'drop()' function
	df.drop(columns='fnlwgt',axis=1,inplace=True)

	return df

census_df = load_data()
st.set_option('deprecation.showPyplotGlobalUse', False)
# Write the code to design the web app
# Add title on the main page and in the sidebar.
st.title('Census data Visualization app')
st.sidebar.title('Census data Visulization app')
# Using the 'if' statement, display raw data on the click of the checkbox.
if st.sidebar.checkbox('Show Raw data:'):
  st.subheader('census data set')
  st.dataframe(census_df)

# Add a multiselect widget to allow the user to select multiple visualisations.
# Add a subheader in the sidebar with the label "Visualisation Selector"
st.sidebar.subheader("Visualisation Selector")

# Add a multiselect in the sidebar with label 'Select the Charts/Plots:'
# Store the current value of this widget in a variable 'plot_list'.
plot_list=st.sidebar.multiselect('Select the chart/plot:',('pie plot','box plot','count plot'))

# Display pie plot using matplotlib module and 'st.pyplot()'
if 'pie plot' in plot_list:
  st.subheader('Distribution Records for different income groups')
  c=st.sidebar.multiselect('Select the column for pie chart',('income','gender'))
  for i in c:
    p_data=census_df[i].value_counts()
    plt.title(f'pie chart {i}')
    plt.figure(figsize=(10,5))
    plt.pie(p_data,labels=p_data.index,autopct='%1.2f%%',startangle = 30,)
    st.pyplot()
if 'box plot' in plot_list:
	st.subheader('Box plot for hours per week')
	c=st.sidebar.multiselect('Select the column for box plot',('income','gender'))
	for i in c:
		plt.title(f'box plot {i}')
		plt.figure(figsize=(10,5))
		sns.boxplot(x=census_df[ 'hours-per-week'],y=census_df[i])
		st.pyplot() 
if 'count plot' in plot_list:
	st.subheader('count plot')
	plt.figure(figsize=(15,4))
	sns.countplot(x='workclass',hue='income',data=census_df)
	st.pyplot()
