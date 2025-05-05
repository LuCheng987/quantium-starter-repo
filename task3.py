import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.express as px

# 读取数据
df = pd.read_csv("output/cleaned_sales.csv")
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")

# 地区选项（英文内部用，界面可展示中文）
regions = ['All', 'North', 'East', 'South', 'West']
region_display = {
    'All': '全部',
    'North': '北部',
    'East': '东部',
    'South': '南部',
    'West': '西部'
}

# 创建应用
app = dash.Dash(__name__)
app.title = "Soul Foods - 区域销售分析"

app.layout = html.Div(style={'fontFamily': 'Arial, sans-serif', 'padding': '20px'}, children=[
    html.H1("Pink Morsel 销售趋势分析", style={'textAlign': 'center', 'color': '#2a3f5f'}),

    html.Div([
        html.Label("选择地区：", style={'fontSize': '18px', 'marginRight': '10px'}),
        dcc.RadioItems(
            id='region-selector',
            options=[{'label': region_display[r], 'value': r} for r in regions],
            value='All',
            labelStyle={'display': 'inline-block', 'margin-right': '20px', 'fontSize': '16px'}
        )
    ], style={'textAlign': 'center', 'marginBottom': '30px'}),

    dcc.Graph(id='sales-chart', style={'border': '1px solid #ddd', 'padding': '10px'})
])

@app.callback(
    Output('sales-chart', 'figure'),
    Input('region-selector', 'value')
)
def update_chart(selected_region):
    if selected_region == 'All':
        filtered = df.groupby("date")["sales"].sum().reset_index()
        title = "每日总销售额（全部地区）"
    else:
        filtered = df[df["region"].str.lower() == selected_region.lower()]
        filtered = filtered.groupby("date")["sales"].sum().reset_index()
        title = f"{region_display[selected_region]}地区每日销售额"

    fig = px.line(
        filtered,
        x="date",
        y="sales",
        title=title,
        labels={"sales": "销售额 ($)", "date": "日期"}
    )

    fig.add_shape(
        type="line",
        x0="2021-01-15", x1="2021-01-15",
        y0=0, y1=filtered["sales"].max(),
        line=dict(color="red", dash="dash")
    )

    fig.add_annotation(
        x="2021-01-15",
        y=filtered["sales"].max(),
        text="涨价日 (2021-01-15)",
        showarrow=True,
        arrowhead=1,
        ax=0,
        ay=-40
    )

    fig.update_layout(transition_duration=500)
    return fig

if __name__ == '__main__':
    app.run(debug=True)
