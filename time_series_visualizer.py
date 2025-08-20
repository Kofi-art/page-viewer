import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv("fcc-forum-pageviews.csv")
df.set_index("date", inplace=True)
df.index = pd.to_datetime(df.index)

# Clean data
df = df[(df["value"] >= df["value"].quantile(0.025)) & 
        (df["value"] <= df["value"].quantile(0.975))]


def draw_line_plot():
    # Draw line plot
    df_line = df.copy()
    fig = plt.figure(figsize=(20, 8))
    plt.plot(df_line)
    plt.xlabel("Date")
    plt.ylabel("Page Views")
    plt.title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")




    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month_name()
    months_order = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    df_grouped = df_bar.groupby(['year', 'month'])['value'].mean().unstack()

    # Ensure months are in correct order
    df_grouped = df_grouped[['January', 'February', 'March', 'April', 'May', 'June',
                            'July', 'August', 'September', 'October', 'November', 'December']]

    # Plot
    fig = df_grouped.plot.bar(figsize=(20, 8)).figure
    plt.xlabel('Years')
    plt.ylabel('Average Page Views')
    plt.legend(title='Months')
    
    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]
    months_order = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
    ]
    df_box['month'] = pd.Categorical(
        df_box['month'],
        categories=months_order,
        ordered=True
    )
    # Draw box plots (using Seaborn)

    fig, axes = plt.subplots(1, 2, figsize=[20, 8])
    sns.boxplot(
        data=df_box,
        x="year",
        y="value",
        hue="year",
        legend=False,
        palette="Set1",
        flierprops=dict(marker='.', markerfacecolor="black"),
        ax=axes[0]
    )
    axes[0].set_title("Year-wise Box Plot (Trend)")
    axes[0].set_xlabel("Year")
    axes[0].set_ylabel("Page Views")



    sns.boxplot(
        data=df_box,
        x="month",
        y="value",
        hue="month",
        legend=False,
        palette="Set2",
        flierprops=dict(marker='.', markerfacecolor="black"),
        ax=axes[1]
    )
    axes[1].set_title("Month-wise Box Plot (Seasonality)")
    plt.xlabel("Month")
    plt.ylabel("Page Views")




    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
