import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import numpy as np
from scipy.integrate import odeint

# Define the Lotka-Volterra equations
def lotka_volterra(state, t, alpha, beta, gamma, delta):
    x, y = state
    dxdt = alpha * x - beta * x * y
    dydt = -gamma * y + delta * x * y
    return [dxdt, dydt]

# Solve the system and return the trajectory
def solve_lotka_volterra(initial_conditions, alpha, beta, gamma, delta):
    t = np.linspace(0, 100, 1000)
    solution = odeint(lotka_volterra, initial_conditions, t, args=(alpha, beta, gamma, delta))
    return solution[:, 0], solution[:, 1]  # prey, predators

# Initialize Dash app
app = dash.Dash(__name__)

# Default initial conditions
DEFAULT_INITIAL_CONDITIONS = [10.0, 5.0]

# App layout
app.layout = html.Div([
    html.H1("Lotka-Volterra Model Interactive App"),
    dcc.Graph(id='phase-plot', style={'width': '80%', 'height': 'auto', 'aspectRatio': '1/1'}),
    html.Div([
        html.Label("α (Prey Growth Rate):"),
        dcc.Slider(id='alpha-slider', min=0.1, max=2.0, step=0.1, value=1.0, marks={i: str(i) for i in np.arange(0.1, 2.1, 0.5)}),
        html.Label("β (Predation Rate):"),
        dcc.Slider(id='beta-slider', min=0.01, max=0.5, step=0.01, value=0.1, marks={i: str(i) for i in np.arange(0.01, 0.51, 0.1)}),
        html.Label("γ (Predator Death Rate):"),
        dcc.Slider(id='gamma-slider', min=0.1, max=2.0, step=0.1, value=1.5, marks={i: str(i) for i in np.arange(0.1, 2.1, 0.5)}),
        html.Label("δ (Predator Growth Rate):"),
        dcc.Slider(id='delta-slider', min=0.01, max=0.2, step=0.01, value=0.075, marks={i: str(i) for i in np.arange(0.01, 0.21, 0.05)})
    ], style={'width': '80%', 'padding': '20px'}),
    dcc.Store(id='initial-conditions-store', data=DEFAULT_INITIAL_CONDITIONS)  # Store for initial conditions
])

# Callback to update the graph based on sliders and clicks
@app.callback(
    [Output('phase-plot', 'figure'),
     Output('initial-conditions-store', 'data')],
    [
        Input('alpha-slider', 'value'),
        Input('beta-slider', 'value'),
        Input('gamma-slider', 'value'),
        Input('delta-slider', 'value'),
        Input('phase-plot', 'clickData')
    ],
    [State('initial-conditions-store', 'data')]
)
def update_graph(alpha, beta, gamma, delta, click_data, current_initial_conditions):
    # Update initial conditions if a click occurred
    if click_data:
        initial_conditions = [click_data['points'][0]['x'], click_data['points'][0]['y']]
    else:
        initial_conditions = current_initial_conditions
    
    # Solve the system
    prey, predators = solve_lotka_volterra(initial_conditions, alpha, beta, gamma, delta)
    
    # Create the Plotly figure
    fig = go.Figure()

    # Add invisible grid points for precise selection
    x_max = 100
    y_max = 100
    x_grid = np.linspace(0, x_max, 100)
    y_grid = np.linspace(0, y_max, 100)
    X_grid, Y_grid = np.meshgrid(x_grid, y_grid)

    fig.add_trace(go.Scatter(
        x=X_grid.flatten(),
        y=Y_grid.flatten(),
        mode='markers',
        marker=dict(color='rgba(0,0,0,0)', size=1),
        showlegend=False
    ))

    # Add trajectory
    fig.add_trace(go.Scatter(
        x=prey,
        y=predators,
        mode='lines',
        name='Trajectory',
        line=dict(color='blue')
    ))
    
    # Add initial condition point
    fig.add_trace(go.Scatter(
        x=[initial_conditions[0]],
        y=[initial_conditions[1]],
        mode='markers',
        name='Initial Condition',
        marker=dict(color='red', size=10)
    ))
    
    # Update layout
    fig.update_layout(
        title='Lotka-Volterra Phase Space',
        xaxis_title='Prey Population',
        yaxis_title='Predator Population',
        showlegend=True,
        xaxis=dict(range=[0, x_max]),
        yaxis=dict(range=[0, y_max]) 
    )
    
    return fig, initial_conditions

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)