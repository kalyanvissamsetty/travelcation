import matplotlib.pyplot as plt
import base64
from io import BytesIO
import numpy as np
import pandas as pd

def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer,format='png')
    buffer.seek(0)
    image_png=buffer.getvalue()
    graph=base64.b64encode(image_png)
    graph=graph.decode('utf-8')
    buffer.close()
    return graph

def get_plot(x,y):
    plt.switch_backend('AGG')
    plt.figure(figsize=(7, 5))
    plt.title('The Average Price To Each City')
    plt.plot(x,y,color='black', linestyle='dashed', linewidth = 3,
         marker='o', markerfacecolor='red', markersize=12)
    plt.xticks(rotation=45)
    plt.xlabel('Cities')
    plt.ylabel('Average price')
    plt.tight_layout()
    graph=get_graph()
    return graph


def get_plot1(x,y):
    plt.switch_backend('AGG')
    plt.figure(figsize=(7, 5))
    plt.title('Price Comparision for each hotel')
    plt.bar(x, y,width=0.4, color=['red', 'green','red','green','red'])
    plt.xticks(rotation=80)
    plt.xlabel('Hotels')
    plt.ylabel('price')
    plt.tight_layout()
    graph = get_graph()
    return graph

def get_plot2(x):
    plt.switch_backend('AGG')
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.hist(x, bins=1)
    plt.xlabel('Hotels')
    plt.ylabel('Star rating')
    plt.title('Star rating of all hotels')
    plt.tight_layout()
    graph = get_graph()
    return graph