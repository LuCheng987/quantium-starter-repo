import pandas as pd
import dash
from dash import dcc, html
import plotly.express as px

# 读取处理后的数据
df = pd.read_csv("output/cleaned_sales.csv")

# 确保日期是 datetime 类型并排序
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")

# 聚合每日销售额（所有地区总和）
sales_by_date = df.groupby("date")["sales"].sum().reset_index()

# 创建折线图
fig = px.line(
    sales_by_date,
    x="date",
    y="sales",
    title="Daily Sales of Pink Morsel",
    labels={"sales": "Total Sales ($)", "date": "Date"}
)

# 添加涨价日期（2021-01-15）参考线
fig.add_shape(
    type="line",
    x0="2021-01-15", x1="2021-01-15",
    y0=0, y1=sales_by_date["sales"].max(),
    line=dict(color="red", dash="dash"),
)

# 添加注释文字
fig.add_annotation(
    x="2021-01-15",
    y=sales_by_date["sales"].max(),
    text="Price Increase (2021-01-15)",
    showarrow=True,
    arrowhead=1,
    ax=0,
    ay=-40
)

# 创建 Dash 应用
app = dash.Dash(__name__)
app.title = "Soul Foods Sales Dashboard"

app.layout = html.Div(children=[
    html.H1("Soul Foods - Pink Morsel Sales Overview", style={'textAlign': 'center'}),
    dcc.Graph(id='sales-line-chart', figure=fig)
])

# 启动服务
if __name__ == '__main__':
    app.run(debug=True)

