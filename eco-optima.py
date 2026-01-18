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
        df.loc[700:, "fuel level"] -= np.arange(affected_rows) * 5 #Fuel
        df.loc[700:, "pressure"] -= 10 #Pressure

        return df

    df = generate_sensor_data()
    return (mo,)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
