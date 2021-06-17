import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import os
outdir = os.path.abspath('tests/947_tW')
fig = go.Figure()
df = pd.read_csv('tests/947_tW/extr_all.csv')
df=df.fillna(0)
Time = df['t'].unique()
data =  [[] for i in range(14)]
def dist(x2,y2,z2,z1, x1=100,y1=100):
    r=np.sqrt((10**(-6*2)) * ((x1-x2)**2+(y1-y2)**2+(z1-z2)**2))
    return r

THLM=[]
for step in Time:
    filter_t = df['t'] == step
    x=df.loc[filter_t]['x'].values.tolist()
    # print(x)
    y=df.loc[filter_t]['y'].values.tolist()
    z=df.loc[filter_t]['z'].values.tolist()
    v=df.loc[filter_t]['v'].fillna(0).values.tolist()
    id = df.loc[filter_t]['id']
    v_dist = [[] for i in range(14)]
    lenn=14
    lenV=len(v)
    thlm =[]
    for i in range(len(v)):
        if z[i] > 1000:
            thlm.append(v[i] / dist(x[i], y[i], z[i], 1150))
    for list in range(lenn):
        for i in range(lenV):
            if 850 >= z[i] >= -850:

                v_dist[list].append(v[i] /dist(x[i],y[i],z[i],-850+(list*114)))
    for i in range(lenn):
        data[i].append(sum(v_dist[i]))
    THLM.append(sum(thlm))


#print(data[0])
subplot_titles=["L2-3","L2-3","L2-3","L4", "L4","L4","L5","L5","L5","L5","L5","L6", "L6","L6"]
fig = make_subplots(rows=15, cols=1)
for i in range(14):
    fig.add_trace(go.Scatter(x=Time, y=data[i],  name=subplot_titles[i]), row=i+1, col=1)
fig.add_trace(go.Scatter(x=Time, y=THLM,  name="thlm"), row=15, col=1)
fig.update_xaxes(matches='x')
fig.update_yaxes(matches='y')

fig.update_layout(height=1000)
fig.update_xaxes(showticklabels=False)
fig.update_xaxes(showticklabels=True, row=15, col=1)
#fig.show()
fig.write_html(os.path.join(outdir,'main(extracellular).html'))




