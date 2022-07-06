import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


# Import data
df = pd.read_csv("medical_examination.csv")

# Add 'overweight' column
df['height'] = df['height'].div(100) 
df['overweight'] = df['weight'] / df['height']**2
df['overweight'].values[df['overweight'] <= 25] = 0
df['overweight'].values[df['overweight'] > 25] = 1

# Normalize data by making 0 always good and 1 always bad. If the value of 'cholesterol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.
df['cholesterol'].values[df['cholesterol'] <= 1] = 0
df['cholesterol'].values[df['cholesterol'] > 1] = 1
df['gluc'].values[df['gluc'] <= 1] = 0
df['gluc'].values[df['gluc'] > 1 ] = 1

# Draw Categorical Plot
def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    df_cat = pd.melt(df,id_vars=['cardio'],value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight'])


    # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the columns for the catplot to work correctly.
    df_cat = pd.DataFrame(df_cat.groupby(['cardio','variable','value'])['value'].count())
    df_cat.rename(columns={'value':'total'},inplace=True)
    df_cat.reset_index(inplace=True)

    # Draw the catplot with 'sns.catplot()'
    
    bar = sns.catplot(x='variable', y ='total', hue='value', col='cardio', kind='bar',data =df_cat)

    fig = bar.fig
    # Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig


# Draw Heat Map
def draw_heat_map():
    # Clean the data
    df_heat = df[(df['ap_lo'] <= df['ap_hi']) & (df['height'] >= df['height'].quantile(0.025)) & (df['height'] <= df['height'].quantile(0.975)) & (df['weight'] >= df['weight'].quantile(0.025)) & (df['weight'] <= df['weight'].quantile(0.975))]
     

    # Calculate the correlation matrix
    corr = df_heat.corr()

    # Generate a mask for the upper triangle
    mask = np.zeros_like(corr)
    mask[np.triu_indices_from(mask)] = True



    # Set up the matplotlib figure
    fig, ax = plt.subplots(figsize=(12, 12))

    # Draw the heatmap with 'sns.heatmap()'
    ax = sns.heatmap(corr,mask = mask, square = True,annot = True,center= 0 ,vmin = -0.1 , vmax= 0.25,fmt = '.1f')

    
    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig
