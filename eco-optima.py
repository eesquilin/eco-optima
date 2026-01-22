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
    mo.md("Asset & Compliance Monitoring - Fuel System Anomaly Detection")
    mo.hstack([mo.ui.table(data.head())])
    return data, mo


@app.cell
def _(mo):
    mo.md(r"""
    2. Detection Model
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

    if is_anomaly is True:
        alert = mo.callout("Critical Anomaly Detected in Fuel System", kind="danger")

    else:
        alert = mo.callout("Fuel System Operating Normally", kind="success")

    alert
    return (is_anomaly,)


@app.cell
def _(mo):
    mo.md(r"""
    3. Agentic Workflow
    """)
    return


@app.cell
def _(mo):

    from langchain_google_genai import ChatGoogleGenerativeAI
    import os


    # Loading compliance rules from a text file
    def get_rules():
        with open("compliance_rules.txt", "r") as file:
            rules = file.read()
            return rules

    rules_content = get_rules()

    def get_cloud_agent():
        api_key = os.getenv("GOOGLE_API_KEY")
        if "GOOGLE_API_KEY" not in os.environ:
            return mo.md("Google API Key not found. Please set the GOOGLE_API_KEY environment variable.")
        return ChatGoogleGenerativeAI(
            model="gemini-2.5-flash-lite", 
            api_key=api_key, 
            temperature=0)

    llm = get_cloud_agent() 
    status = mo.md("**Eco-Optima Chain Initialized Successfully.**").callout(kind="success") if llm else mo.md("**Warning:** Google Generative AI LLM not initialized. Please check your API key.").callout(kind="warning")

    status
    return llm, rules_content


@app.cell
def _(llm, rules_content):
    from langchain_core.prompts import ChatPromptTemplate

    prompt_template = ChatPromptTemplate.from_messages([
        ("system", f"""
        You are the Eco-Optima Compliance Monitoring Agent. 
        Your task is to analyze fuel tank sensor data and identify any anomalies based on the following compliance manual:
        <COMPLIANCE_MANUAL>
        {rules_content}
        <COMPLIANCE_MANUAL>

        If you detect a violation , explain which rule applies and draft a professional 
        maintenance work order. If no violations are found, state 'STATUS: All systems normal'.
        """),
        ("user", "LATEST SENSOR DATA: {sensor_input}")
    ])


    compliance_chain = prompt_template | llm
    return (compliance_chain,)


@app.cell
def _(compliance_chain, data, is_anomaly, mo):
    if is_anomaly.any():
        anomalies = data[data["anomaly"] == -1].tail(1).to_markdown()

        # Running the compliance check
        report = compliance_chain.invoke({"sensor_input": anomalies})
        if "STATUS: All systems normal" in report.content:
            ui = mo.vstack([
                mo.md("### Compliance Report"),
                mo.md(report.content).callout(kind="success")
            ])
        else:
            ui = mo.vstack([
                mo.md("### Compliance Report"),
                mo.md(report.content).callout(kind="warn")
            ])
    else:
        ui = mo.md("### Compliance Report").callout(kind="success") + mo.md("STATUS: All systems normal").callout(kind="success")
    ui
    return


if __name__ == "__main__":
    app.run()
