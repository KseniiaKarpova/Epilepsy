import plotly.graph_objects as go
import pandas as pd
import os
import csv
from plotly.subplots import make_subplots


outdir = os.path.abspath('tests/987_tW')


#df = pd.read_csv('tests/950_tW/spikeE.csv', sep=',')
x = []
y = []
with open('tests/987_tW/spikeE.csv', newline='') as File:
    reader = csv.reader(File)

    for row in reader:
        try:
            for i in row[4:]:
                x.append(round(float(i),1))
                y.append(int(float(row[2])))
        except Exception:
            print(Exception)
#print(len(y))
#print(len(x))
fig = make_subplots(1,2)
fig.add_trace(go.Histogram2d(
        x=x,
        y=y,
        xbins=dict(start=0, end=30, size=0.1),
        #autobiny=False,
        ybins=dict(start=-850, end=1300, size=10),
        coloraxis = "coloraxis",),1,1)


#outdir = os.path.abspath('tests/989_50n_tW')


#df = pd.read_csv('tests/950_tW/spikeE.csv', sep=',')
x = []
y = []
with open('tests/992_tW/spikeE.csv', newline='') as File:
    reader = csv.reader(File)

    for row in reader:
        try:
            for i in row[4:]:
                x.append(round(float(i),1))
                y.append(int(float(row[2])))
        except Exception:
            print(Exception)
fig.add_trace(go.Histogram2d(
        x=x,
        y=y,
        xbins=dict(start=0, end=30, size=0.1),
        #autobiny=False,
        coloraxis = "coloraxis",
        ybins=dict(start=-850, end=1300, size=10),
        bingroup = 1,),1,2)

#fig.show()
fig.write_html(os.path.join(outdir,'spike_0_gaba.html'))