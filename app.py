import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from src.dashboard import Backend, draw_graph, clear_graph

backend = Backend(dmc_path="data/dmc.csv", ariadna_path="data/ariadna.csv")

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LITERA])

server = app.server

app.layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Label("Base DMC color:"),
                        dcc.Dropdown(
                            id="drop_dmc",
                            options=[
                                {"label": code, "value": code}
                                for code in backend.dmc_df.index
                            ],
                            placeholder="Select DMC color",
                            searchable=True,
                            clearable=False,
                            style={"marginBottom": "1.5em"},
                        ),
                        html.Label("Color comparing algorithm:"),
                        dcc.Dropdown(
                            id="drop_metric",
                            options=[
                                {"label": m, "value": m} for m in backend.metrics.keys()
                            ],
                            placeholder="Select algorithm",
                            searchable=False,
                            value=backend.default_metric,
                            clearable=False,
                            style={"marginBottom": "1.5em"},
                        ),
                        html.Label("Number of similar colors:"),
                        html.Div(
                            dcc.Slider(
                                id="slider_n",
                                min=1,
                                max=9,
                                step=1,
                                value=5,
                                marks={n: str(n) for n in range(1, 10, 2)},
                            ),
                            style={"marginBottom": "1.5em"},
                        ),
                        html.Div(
                            [
                                dbc.Button(
                                    "Clear",
                                    color="secondary",
                                    id="button_clear",
                                    outline=True,
                                    n_clicks=0,
                                    style={"marginRight": ".5em"},
                                ),
                                dbc.Button(
                                    "Find similar",
                                    color="primary",
                                    id="button_run",
                                    n_clicks=0,
                                ),
                            ],
                            style={"display": "flex", "justify-content": "right"},
                        ),
                    ],
                    width=3,
                ),
                dbc.Col(
                    html.Div(
                        [
                            dcc.Graph(
                                id="graph",
                                figure=clear_graph(),
                                config={"staticPlot": True},
                            )
                        ]
                    ),
                    width=9,
                ),
            ],
            style={"marginLeft": "1em", "marginTop": "1em"},
        )
    ]
)


# Draw graph with run button if color is chosen
@app.callback(
    Output("graph", "figure"),
    Input("button_run", "n_clicks"),
    State("drop_dmc", "value"),
    State("drop_metric", "value"),
    State("slider_n", "value"),
)
def find_similar_colors(clicks, dmc_choice, metric, n):
    if not clicks or not dmc_choice:
        return clear_graph()

    base_color = backend.dmc_to_hex(dmc_choice)
    result_codes, result_colors = backend.find_similar(dmc_choice, metric, n)

    fig = draw_graph(base_color, dmc_choice, result_colors, result_codes)

    return fig


# Clear graph and choices with clear button
@app.callback(
    Output("button_run", "n_clicks"),
    Output("drop_dmc", "value"),
    Input("button_clear", "n_clicks"),
)
def on_clear_button(_):
    return 0, None


if __name__ == "__main__":
    app.run_server(debug=True)
