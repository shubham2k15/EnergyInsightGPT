import pandas as pd


# ---------------- LOAD FACTORS ----------------
def load_emission_factors():
    df = pd.read_csv("energy_data/carbon_factors_reference/carbon_factors.csv")
    df.columns = df.columns.str.strip().str.lower()
    return df


# ---------------- BASIC CARBON ----------------
def calculate_carbon(energy_kwh, source):
    df = load_emission_factors()

    row = df[df["energy_source"] == source]

    if row.empty:
        return {
            "emission": 0,
            "level": "Unknown",
            "suggestion": "Invalid energy source"
        }

    factor = float(row["emission_factor"].values[0])
    emission = round(energy_kwh * factor, 2)

    if emission < 100:
        level = "Low"
        suggestion = "Good efficiency"
    elif emission < 300:
        level = "Moderate"
        suggestion = "Consider optimizing usage"
    else:
        level = "High"
        suggestion = "Reduce consumption or switch to cleaner sources"

    return {
        "emission": emission,
        "level": level,
        "suggestion": suggestion,
        "factor": factor
    }


# ---------------- TOTAL EMISSIONS (NEW) ----------------
def estimate_total_emissions(appliances, electricity_kwh, source, transport_km):
    df = load_emission_factors()

    row = df[df["energy_source"] == source]

    if row.empty:
        return 0, 0

    factor = float(row["emission_factor"].values[0])

    # Electricity
    electricity_emission = electricity_kwh * factor

    # Appliances (already in kWh)
    appliance_emission = sum(appliances.values()) * factor

    # Transport (simple factor)
    transport_emission = transport_km * 0.12

    monthly_total = electricity_emission + appliance_emission + transport_emission
    yearly_total = monthly_total * 12

    return round(monthly_total, 2), round(yearly_total, 2)


# ---------------- ENRICH DATAFRAME ----------------
def enrich_energy_dataframe(df):
    factors = load_emission_factors()

    df.columns = df.columns.str.strip()

    merged = df.merge(factors, on="energy_source", how="left")

    merged["emission_factor"] = merged["emission_factor"].fillna(0)

    merged["CO2_emission_kg"] = (
        merged["energy_usage_kWh"] * merged["emission_factor"]
    ).round(2)

    total = merged["energy_usage_kWh"].sum()

    if total > 0:
        merged["usage_share_pct"] = (
            merged["energy_usage_kWh"] / total * 100
        ).round(1)
    else:
        merged["usage_share_pct"] = 0

    return merged


# ---------------- INSIGHTS ----------------
def generate_energy_insights(df):
    insights = []

    if df.empty:
        return ["No data available."]

    avg = df["energy_usage_kWh"].mean()

    # 🔥 Above average usage
    high = df[df["energy_usage_kWh"] > avg * 1.2]

    for _, row in high.iterrows():
        percent = round((row["energy_usage_kWh"] / avg - 1) * 100, 1)
        insights.append(
            f"{row['location']} is consuming {percent}% above average energy."
        )

    # 🔥 Top consumer
    top = df.loc[df["energy_usage_kWh"].idxmax()]
    insights.append(f"{top['location']} has the highest energy usage.")

    # 🔥 High contribution
    heavy = df[df["usage_share_pct"] > 30]
    for _, row in heavy.iterrows():
        insights.append(
            f"{row['location']} contributes {row['usage_share_pct']}% of total consumption."
        )

    return insights