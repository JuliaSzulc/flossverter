"""
Functions used for displaying colors swatches.
"""
from typing import Optional

import plotly.graph_objects as go


def clear_graph() -> go.Figure:
    """
    Removes current swatch by replacing it with a background-colored graph.

    Returns:
        go.Figure: Plotly graph figure instance.
    """
    fig = go.Figure(
        data={},
        layout=go.Layout(
            template=None,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis={"showgrid": False, "showticklabels": False, "zeroline": False},
            yaxis={"showgrid": False, "showticklabels": False, "zeroline": False},
        ),
    )
    return fig


def draw_graph(
    base_color: str,
    base_label: Optional[str],
    compared_colors: list[str],
    compared_labels: list[str],
) -> go.Figure:
    """
    Creates a swatch of given colors next to the base color with their mouline codes.

    Args:
        base_color (str): Base hexadecimal color.
        base_label (Optional[str]): Base mouline identifier if the algorithm input was
            DMC code.
        compared_colors (list[str]): Hexadecimal codes of compared colors.
        compared_labels (str): Mouline identifiers of compared colors.

    Returns:
        go.Figure: Plotly graph figure instance.
    """
    n = len(compared_colors)

    base_label = f"DMC {base_label} " if base_label else f"{base_color} "

    fig = go.Figure(
        data=go.Heatmap(
            z=[list(range(n)), [n] * n],
            x=compared_labels,
            y=["Ariadna ", base_label],
            colorscale=compared_colors + [base_color],
            showscale=False,
            xgap=5,
        ),
        layout=go.Layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis={"showgrid": False, "zeroline": False},
            yaxis={"showgrid": False, "zeroline": False},
        ),
    )

    return fig
