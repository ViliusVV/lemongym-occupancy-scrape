import datetime
import random

import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

FILE = "occupancies.csv"

if __name__ == "__main__":
    # read file
    with open(FILE, "r", encoding="utf-8") as file:
        lines = file.readlines()

    # parse lines (group by name)
    data = {}
    for line in lines:
        time, name, occupancy = line.strip().split(";")
        if name != "Banginis": continue
        if name not in data:
            data[name] = []
        date = datetime.datetime.fromisoformat(time).astimezone()
        # fix 100% occupancy
        if occupancy == "100":
            occupancy = 0
        data[name].append((date, int(occupancy)))

    bangd = data["Banginis"]
    weekends = np.where(np.array([date.weekday() >= 5 for date, _ in bangd]),100,0)
    dates = [date for date, _ in bangd]
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(
        x=dates, y=weekends,
        fill='tonexty', fillcolor='rgba(99, 110, 250, 0.2)',
        line_shape='hv', line_color='rgba(0,0,0,0)',
        showlegend=False
        ),
        row=1, col=1, secondary_y=True
    )
    # Smoothed derivative
    bangd_derivative = np.gradient([occupancy for _, occupancy in bangd], np.array([d.timestamp() for d in dates]))
    # normalize
    bangd_derivative = bangd_derivative * 1000
    # smooth
    bangd_derivative = np.convolve(bangd_derivative, np.ones(100)/100, mode='same')

    fig.update_layout(yaxis1_range=[-5, 80], yaxis2_range=[-0, 0.1], yaxis2_showgrid=False, yaxis2_tickfont_color='rgba(0,0,0,0)')


    # plotly
    # fig = px.line(title="Occupancies")
    for name, values in data.items():
        times, occupancies = zip(*values)
        fig.add_scatter(x=times, y=occupancies, name=name, mode="lines", line_shape='spline')


    fig.add_scatter(x=dates, y=bangd_derivative, name="der", mode="lines", marker=dict(size=2))

    # fig.update_xaxes(showgrid=False)  # , gridwidth=1, gridcolor='rgba(0,0,255,0.1)')

    fig.update_xaxes(title_text="Time")
    fig.show()
