# Lotka-Volterra Model Interactive App

An interactive web application that visualizes the Lotka-Volterra predator-prey model using Dash and Plotly.

## Features
- Interactive phase space visualization
- Real-time parameter adjustment
- Click-to-set initial conditions
- Animated trajectory visualization
- Responsive design

## Setup

1. Clone the repository:
```bash
git clone https://github.com/jamiewannenburg/lotka-volterra.git
cd lotka-volterra
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the app:
```bash
python Lotka-Volterra.py
```

The app will be available at http://localhost:8050

## Deployment
This app is configured for deployment on Heroku. To deploy:

1. Create a new Heroku app
2. Push to Heroku:
```bash
git push heroku main
```

See https://up-openday-2025-57d03798734f.herokuapp.com/

## Model Description
The Lotka-Volterra equations describe the dynamics between predator and prey populations:

- α: Prey growth rate
- β: Predation rate
- γ: Predator death rate
- δ: Predator growth rate

The system exhibits oscillatory behavior, with predator and prey populations cycling over time. 