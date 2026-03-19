from dash import Dash, dcc, html, Input, Output
import pandas as pd
import plotly.express as px

# Load data (use relative path for GitHub)
data = pd.read_csv(r"C:\ALL PROJECTS\Data analyst\walmart sales\WalmartSalesData.csv (1).csv")
data['Date'] = pd.to_datetime(data['Date'])

app = Dash(__name__)

# Theme styles
light_theme = {
    'background': "#041015",
    'text': '#2c3e50',
    'card': 'white'
}

dark_theme = {
    'background': '#1e1e1e',
    'text': 'white',
    'card': "#145595"
}

# Layout
app.layout = html.Div([

    html.H1("📊 Sales Dashboard", id='title',
            style={'textAlign': 'center'}),

    # 🌗 Theme Toggle
    dcc.RadioItems(
        id='theme_toggle',
        options=[
            {'label': 'Light', 'value': 'light'},
            {'label': 'Dark', 'value': 'dark'}
        ],
        value='light',
        inline=True,
        style={'textAlign': 'center'}
    ),

    # 🎛️ Sidebar + Main Layout
    html.Div([

        # Sidebar
        html.Div([

            html.H3("Filters"),

            dcc.Dropdown(
                id='branch_filter',
                options=[{'label': b, 'value': b} for b in data['Branch'].unique()],
                value=data['Branch'].unique()[0],
                clearable=False
            ),

            dcc.Dropdown(
                id='product_filter',
                options=[{'label': p, 'value': p} for p in data['Product line'].unique()],
                multi=True,
                placeholder="Select Product"
            )

        ], style={
            'width': '20%',
            'padding': '20px'
        }),

        # Main Content
        html.Div([

            # KPI Cards
            html.Div(id='kpi_cards', style={
                'display': 'flex',
                'justifyContent': 'space-around',
                'margin': '20px'
            }),

            # Charts
            dcc.Graph(id='bar_chart'),
            dcc.Graph(id='pie_chart'),
            dcc.Graph(id='line_chart')

        ], style={'width': '80%'})

    ], style={'display': 'flex'})

], id='main_container')


# Callback
@app.callback(
    [Output('bar_chart', 'figure'),
     Output('pie_chart', 'figure'),
     Output('line_chart', 'figure'),
     Output('kpi_cards', 'children'),
     Output('main_container', 'style'),
     Output('title', 'style')],
    [Input('branch_filter', 'value'),
     Input('product_filter', 'value'),
     Input('theme_toggle', 'value')]
)
def update_dashboard(branch, product, theme):

    df = data[data['Branch'] == branch]

    if product:
        df = df[df['Product line'].isin(product)]

    # Theme selection
    theme_style = light_theme if theme == 'light' else dark_theme

    # KPI calculations
    total_sales = df['Total'].sum()
    avg_rating = df['Rating'].mean()
    total_transactions = len(df)

    # KPI Cards
    kpi = [
        html.Div([
            html.H4("💰 Total Sales"),
            html.P(f"{total_sales:.2f}")
        ], style={
            'background': theme_style['card'],
            'padding': '15px',
            'borderRadius': '10px'
        }),

        html.Div([
            html.H4("⭐ Avg Rating"),
            html.P(f"{avg_rating:.2f}")
        ], style={
            'background': theme_style['card'],
            'padding': '15px',
            'borderRadius': '10px'
        }),

        html.Div([
            html.H4("🧾 Transactions"),
            html.P(f"{total_transactions}")
        ], style={
            'background': theme_style['card'],
            'padding': '15px',
            'borderRadius': '10px'
        })
    ]

    # Charts
    bar_fig = px.bar(
        df, x='Product line', y='Total',
        color='Product line',
        title='Sales by Product',
        template='plotly_dark' if theme == 'dark' else 'plotly_white'
    )

    pie_fig = px.pie(
        df, names='Payment', values='Total',
        title='Payment Distribution',
        template='plotly_dark' if theme == 'dark' else 'plotly_white'
    )

    daily = df.groupby('Date')['Total'].sum().reset_index()

    line_fig = px.line(
        daily, x='Date', y='Total',
        title='Sales Trend',
        markers=True,
        template='plotly_dark' if theme == 'dark' else 'plotly_white'
    )

    return bar_fig, pie_fig, line_fig, kpi, {
        'backgroundColor': theme_style['background'],
        'color': theme_style['text'],
        'padding': '20px'
    }, {
        'textAlign': 'center',
        'color': theme_style['text']
    }


# Run App
app.run(debug=True)