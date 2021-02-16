import plotly.graph_objs as go
from datetime import datetime
from datetime import timedelta


def create_figure(df):
    '''
    func create and return a plotly figure from a OHLC dataframe
    :param df:
    :return:
    '''
    # add hover text
    hover_text = []
    for i in range(len(df['Open'])):
        hover_text.append('Open: ' + str(round(df['Open'][i]))
                          + '<br>High: ' + str(round(df['High'][i]))
                          + '<br>Low: ' + str(round(df['Low'][i]))
                          + '<br>Close: ' + str(round(df['Close'][i]))
                          )

    trace = go.Candlestick(
        x=df['Date'],
        open=df['Open'].astype(float),
        high=df['High'].astype(float),
        low=df['Low'].astype(float),
        close=df['Close'].astype(float),
        text=hover_text,
        hoverinfo='text'
    )
    # export to a html file
    # plot([trace], filename="btc-2020.html")

    # show in browser
    fig = go.Figure(
        data=[trace]
    )
    return fig


def show_candlestick_patterns(fig, df, filter_fn):
    for index, row in df.iterrows():
        if filter_fn(row):
            date_obj = datetime.strptime(row['Date'], '%Y-%m-%d')
            day_0 = (date_obj - timedelta(days=0.5)).strftime('%Y-%m-%d %H:%M:%S')
            day_1 = (date_obj + timedelta(days=0.5)).strftime('%Y-%m-%d %H:%M:%S')
            # add a rectangle
            fig.add_shape(
                type="rect",
                x0=day_0,
                y0=row['Low'] - 300,
                x1=day_1,
                y1=row['High'] + 300,
                line=dict(
                    color="RoyalBlue"
                ),
            )

            # Create scatter trace of text labels
            fig.add_trace(go.Scatter(
                x=[day_0],
                y=[row['Low'] - 550],
                text=['Doji'],
                mode="text",
            ))

            # fig.add_annotation(
            #     x=day_0,
            #     y=row['Low'] - 550,
            #     xref="x",
            #     yref="y",
            #     xanchor='left',
            #     text="dict Text",
            #     showarrow=True,
            #     arrowhead=7,
            #     ax=0,
            #     ay=-40
            # )
    fig.show()
