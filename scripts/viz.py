"""Simple dash script to visualize the humidity readings."""

import argparse
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go


###########
# Constants
###########

# Max number of points to display in the graph
MAX_POINTS = 20

# Style of the humidity value
HUMIDITY_STYLE = {
    "fontFamily": "Arial",
    "fontSize": 54,
    }


# Stryle of the Main Div
MAIN_STYLE = {
    "paddingLeft": 300,
    "paddingRight": 300,
    }


###################
# Utility functions
###################

def convert_dates(t):
    """Convert the stored timestamps to a valid format.

    This is mainly because an observed difference in treatment of the
    timestamps in Windows (where this was developed) and in the Pi
    (where it runs).
    """
    try:
        o = t.apply(lambda x: x.strftime("%Y-%m-%d %H:%M:%S.%s"))
    except ValueError:
        o = t
    return o


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


def serve_layout():
    """Serve layout for app.

    This is what will be assigned to app.layout.
    """
    # First, read humidity data to be displayed
    frm = pd.read_hdf(args.store_location, key="readings")
    last_reading = frm.values[-1, 0]

    return html.Div(style=MAIN_STYLE, children=[
        html.H1(children=str(last_reading) + " %", style=HUMIDITY_STYLE),

        dcc.Graph(
            id='humidity',
            figure={
                'data': [
                    go.Scatter(
                        x=convert_dates(frm.timestamp[-MAX_POINTS:]),
                        y=frm.humidity[-MAX_POINTS:],
                        mode='lines+markers',
                        opacity=0.7,
                        marker={
                            'size': 15,
                            'line': {'width': 0.5, 'color': 'white'}
                        },
                        name='Readings'
                    )
                ],
                'layout': go.Layout(
                    xaxis={'title': 'Date/Time'},
                    yaxis={'title': 'Humidity (%)'},
                    margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                    legend={'x': 0, 'y': 1},
                    hovermode='closest'
                )
            }
        )
    ])


###################
# Dash Layout
###################

# Parse args
CMD_DESCRIPTION = "Visualize the sensor readings of a given file."
parser = argparse.ArgumentParser(description="CMD_DESCRIPTION")
parser.add_argument("store_location", help="HDF5 store with the readings")
args = parser.parse_args()

# Prepare Dash Layout
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Serve layout.
app.layout = serve_layout


###################
# Main function
###################

if __name__ == '__main__':
    app.run_server(debug=True, host="0.0.0.0")
