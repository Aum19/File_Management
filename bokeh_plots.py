# Bokeh Libraries
from bokeh.io import output_file
from bokeh.plotting import figure, show
from bokeh.models import ColumnarDataSource
from bokeh.models.widgets import Tabs, Panel
from bokeh.models import HoverTool
from bokeh.events import Tap
from math import pi
from bokeh.charts import Bar
#from bokeh.transform import cumsum
#from bokeh.palettes import Category20c
import statistics
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def format_count_bar(df, metadata_dict=dict()):
    x = df['Format'].value_counts().to_dict()
    format_pie_panel = bar_plot(x,metadata_dict)
    
    return format_pie_panel

#Scatter File age vs size
def create_scatter_graph(df, metadata_dict=dict()):
    #Creation vs Size
    # The figure will be rendered in a static HTML file
    output_file('output_file_test.html', 
                title=metadata_dict.get('file_title','Bokeh Figure'))
    # Set up a generic figure() object
    cds_df = df
    age_scatter_fig = figure(title=metadata_dict.get('fig_title','Plot'),
             plot_height=500, plot_width=800,
             x_axis_label='Creation_Age_Days',
             y_axis_label='Size_MB',
             x_range=(0, df['Creation_Age_Days'].max()*1.3), 
             y_range=(0, df['Size_MB'].max()*1.3),
             toolbar_location='right')

    median_x = df['Creation_Age_Days'].median()
    median_y = df['Size_MB'].median()
    mean_x = df['Creation_Age_Days'].mean()
    mean_y = df['Size_MB'].mean()
    age_scatter_fig.line([median_x,median_x],[0,median_y], line_width=2, color='green')
    age_scatter_fig.line([0,median_x],[median_y,median_y], line_width=2, color='green')
    age_scatter_fig.line([mean_x,mean_x],[0,mean_y], line_width=2)
    age_scatter_fig.line([0,mean_x],[mean_y,mean_y], line_width=2)

    age_scatter_fig.circle(x='Creation_Age_Days', y='Size_MB', source=cds_df,color='green', size=10, alpha=0.5)

    # Format the tooltip
    tooltips = [
                ('File','@File_name'),
                ('Path', '@Path'),
                ('Format', '@Format'),
                ('Age','@Creation_Age_Days'+' Days old'),
                ('Size','@Size_MB'+' MB'),
            ]

    # Configure a renderer to be used upon hover
    hover_glyph = age_scatter_fig.circle(x='Creation_Age_Days', y='Size_MB', source=cds_df,color='green',
                            size=15, alpha=0,
                            hover_fill_color='black', hover_alpha=0.5)

    # Add the HoverTool to the figure
    age_scatter_fig.add_tools(HoverTool(tooltips=tooltips, renderers=[hover_glyph]))

    Age_scatter_panel = Panel(child=age_scatter_fig, title='Files Age -vs- size')
    
    return Age_scatter_panel

#Bar Format vs total size
def bar_plot(data_dict, meta_data=dict()):
    data = {meta_data.get('X_label'):list(data_dict.keys()),
        meta_data.get('Y_label'): list(data_dict.values())}
    size_format_fig = Bar(data,
        values=str(meta_data.get('Y_label')), 
        label=str(meta_data.get('X_label')),
        title=meta_data.get('plot_title'), 
        legend='top_right',
        color=meta_data.get('color'),
        plot_height=500, 
        plot_width=800)
    Size_format_panel = Panel(child=size_format_fig, title=meta_data.get('panel_title'))
    return Size_format_panel

def get_panels(df, data_dict, metadata_dict=dict()):
    p1 = create_scatter_graph(df, metadata_dict=dict())
    p2 = bar_plot(data_dict, {'X_label': 'Format',\
        'Y_label': 'Total Size',
        'plot_title': 'Format by Size',
        'color': 'red',
        'panel_title': 'Format by size'})
    p3 = format_count_bar(df, {'X_label': 'Format',\
        'Y_label': 'Number of files',
        'plot_title': 'Format by Count',
        'color': 'green',
        'panel_title': 'Format by Count'})    # Assign the panels to Tabs

    tabs = Tabs(tabs=[p1, p2, p3])

    # Show the tabbed layout
    show(tabs)


