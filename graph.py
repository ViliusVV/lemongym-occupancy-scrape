import datetime
import random
import matplotlib.pyplot as plt
import plotly.express as px

FILE = "occupancies.csv"

if __name__ == "__main__":
    # read file
    with open(FILE, "r", encoding="utf-8") as file:
        lines = file.readlines()

    # parse lines (group by name)
    data = {}
    for line in lines:
        time, name, occupancy = line.strip().split(";")
        if name not in data:
            data[name] = []
        date = datetime.datetime.fromisoformat(time).astimezone()
        data[name].append((date, int(occupancy)))

    # plotly
    fig = px.line(title="Occupancies")
    for name, values in data.items():
        times, occupancies = zip(*values)
        fig.add_scatter(x=times, y=occupancies, name=name, mode="lines", line_shape='spline')

    fig.update_xaxes(title_text="Time")
    fig.show()
