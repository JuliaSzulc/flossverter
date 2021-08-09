import plotly.graph_objects as go


def clear_graph():
    fig = go.Figure(
        data={},
        layout=go.Layout(
            template = None,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis={'showgrid': False, 'showticklabels': False, 'zeroline':False},
            yaxis={'showgrid': False, 'showticklabels': False, 'zeroline':False},
        )
    )
    return fig


def draw_graph(base_color, compared_colors, base_label, compared_labels):
    n = len(compared_colors)

    fig = go.Figure(
        data=go.Heatmap(
            z=[list(range(n)), [n] * n],
            x=compared_labels,
            y=['Ariadna ', 'DMC {} '.format(base_label)],
            colorscale=compared_colors + [base_color],
            showscale=False,
            xgap=5,
            hovertemplate='xD'
        ),
        layout=go.Layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis={'showgrid': False, 'zeroline':False},
            yaxis={'showgrid': False, 'zeroline':False},
        ),
    )
    
    return fig
