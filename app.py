import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output, State

from src.dashboard import Backend, clear_graph, draw_graph


backend = Backend(dmc_path="data/dmc.csv", ariadna_path="data/ariadna.csv")

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.LITERA],
    title="FlossVerter - Mouline Color Converter",
)
server = app.server

app.layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                dbc.Tabs(
                                    [
                                        html.Label("Input type:"),
                                        dbc.Tab(
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
                                            label="DMC code",
                                            tab_id="tab_dmc",
                                            active_tab_class_name="fw-bold",
                                        ),
                                        dbc.Tab(
                                            dbc.Input(
                                                id="input_rgb",
                                                placeholder="#rrggbb",
                                                type="text",
                                                pattern=r"#([A-Fa-f0-9]{6}",
                                                valid=False,
                                                maxLength=7,
                                                minLength=6,
                                                style={"marginBottom": "1.5em"},
                                            ),
                                            label="RGB",
                                            tab_id="tab_rgb",
                                            active_tab_class_name="fw-bold",
                                        ),
                                    ],
                                    id="tabs_input",
                                    active_tab="tab_dmc",
                                ),
                            ]
                        ),
                        html.Label("Color comparing algorithm:"),
                        dcc.Dropdown(
                            id="drop_metric",
                            options=[
                                {"label": m, "value": m} for m in backend.METRICS.keys()
                            ],
                            placeholder="Select algorithm",
                            searchable=False,
                            value=backend.DEFAULT_METRIC,
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


# Draw graph on button_run click if color is chosen
# Clear graph on button_run.clicks == 0 (modified by button_clear)
@app.callback(
    Output("graph", "figure"),
    Input("button_run", "n_clicks"),
    State("tabs_input", "active_tab"),
    State("drop_dmc", "value"),
    State("input_rgb", "value"),
    State("input_rgb", "valid"),
    State("drop_metric", "value"),
    State("slider_n", "value"),
    State("graph", "figure"),
)
def find_similar_colors(
    clicks,
    active_tab,
    dmc_input,
    rgb_input,
    rgb_input_valid,
    metric,
    n_colors,
    current_fig,
):
    # clearing
    if not clicks:
        return clear_graph()

    # pass
    if not (dmc_input or rgb_input) or rgb_input_valid:
        return current_fig

    if active_tab == "tab_dmc":
        base_color = backend.dmc_to_hex(dmc_input)
        base_label = dmc_input
    elif active_tab == "tab_rgb":
        base_color = rgb_input
        base_label = None
    else:
        raise NotImplementedError("Unsupported input tab chosen.")

    result_codes, result_colors = backend.find_similar(base_color, metric, n_colors)

    fig = draw_graph(base_color, base_label, result_colors, result_codes)

    return fig


# Clear drop_dmc when active tab changes or on button_clear click
@app.callback(
    Output("drop_dmc", "value"),
    Input("tabs_input", "active_tab"),
    Input("button_clear", "n_clicks"),
)
def clear_drop_dmc(*_):
    return None


# Clear input_rgb when active tab changes or on button_clear click
@app.callback(
    Output("input_rgb", "value"),
    Input("tabs_input", "active_tab"),
    Input("button_clear", "n_clicks"),
)
def clear_input_rgb(*_):
    return ""


# Clear graph on button_clear click
@app.callback(
    Output("button_run", "n_clicks"),
    Input("button_clear", "n_clicks"),
)
def on_clear_button(_):
    return 0


if __name__ == "__main__":
    app.run_server()
