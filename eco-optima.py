import marimo

__generated_with = "0.19.4"
app = marimo.App(width="medium")


@app.cell
def _(mo):
    mo.md(r"""
    1. Generate Synthetic Fuel Data
    """)
    return


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import numpy as np


    def generate_sensor_data(n_days = 30):
        np.random.seed(42)

        # 30 days of data per hour
        time_index = pd.date_range("2026-01-01", periods=n_days*24, freq="H")

        fuel_level = 1000 - (np.arange(len(time_index)) * 0.5) + np.random.normal(0,1, len(time_index))
        pressure = np.random.normal(30, 0.5, len(time_index)) #Normal PSI is ~30

        df = pd.DataFrame({"time stamp": time_index, "fuel level": fuel_level, "pressure": pressure})

        # Injecting an Anomaly at the end (Leak)
        affected_rows = len(df.loc[700:])
        df.loc[700:, "fuel level"] -= np.arange(affected_rows) * 5 #Fuel Rapid Drop
        df.loc[700:, "pressure"] -= 10 #Pressure Drop

        return df

    data = generate_sensor_data()
    return data, mo


@app.cell
def _(mo):
    mo.md(r"""
    2. Visualize the Data
    """)
    return


@app.cell
def _(data):
    data.describe()
    return


@app.cell
def _(mo):
    mo.md(r"""
    3. Detection Model
    """)
    return


@app.cell
def _(data, mo):
    from sklearn.ensemble import IsolationForest

    #Training the model
    model = IsolationForest(contamination=0.05, random_state=42)
    features = data[["fuel level", "pressure"]]
    model.fit(features[:600])  # Training only on normal data

    #Predicting all data (anomalies will be -1)
    data["anomaly"] = model.predict(features)
    is_anomaly = data["anomaly"] == -1

    if is_anomaly:
        alert = mo.Alert("Critical Anomaly Detected in Fuel System", severity=mo.AlertSeverity.CRITICAL)

    else:
        alert = mo.Alert("Fuel System Operating Normally", severity=mo.AlertSeverity.INFO)

    alert.send()
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
