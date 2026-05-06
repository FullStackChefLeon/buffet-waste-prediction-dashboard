import joblib
import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(
    page_title="Buffet Food Waste Prediction Dashboard",
    layout="wide"
)


@st.cache_data
def load_data():
    return pd.read_csv("data/buffet_waste_sample.csv")


@st.cache_resource
def load_model():
    return joblib.load("models/high_waste_risk_model.pkl")


def build_prediction_input(
    meal_period,
    dish_category,
    kitchen_section,
    event_type,
    weather,
    estimated_guests,
    occupancy_rate,
    prepared_qty,
    service_time_remaining,
    refill_count
):
    prepared_qty_per_estimated_guest = prepared_qty / estimated_guests
    refill_per_15min = refill_count / (service_time_remaining / 15)

    is_late_service = int(service_time_remaining <= 30)
    is_low_occupancy = int(occupancy_rate < 0.60)
    is_normal_service = int(event_type == "normal")
    is_late_high_refill = int(service_time_remaining <= 30 and refill_count >= 2)

    row = {
        "meal_period": meal_period,
        "dish_category": dish_category,
        "kitchen_section": kitchen_section,
        "event_type": event_type,
        "weather": weather,
        "estimated_guests": estimated_guests,
        "occupancy_rate": occupancy_rate,
        "prepared_qty": prepared_qty,
        "service_time_remaining": service_time_remaining,
        "refill_count": refill_count,
        "prepared_qty_per_estimated_guest": prepared_qty_per_estimated_guest,
        "refill_per_15min": refill_per_15min,
        "is_late_service": is_late_service,
        "is_low_occupancy": is_low_occupancy,
        "is_normal_service": is_normal_service,
        "is_late_high_refill": is_late_high_refill,
    }

    return pd.DataFrame([row])


def generate_recommendation(probability, service_time_remaining, refill_count, event_type):
    if probability >= 0.65:
        return (
            "High risk detected. Consider reducing the initial production quantity, "
            "avoiding large final refills, and reviewing this item in the next weekly production meeting."
        )

    if probability >= 0.45 and service_time_remaining <= 30:
        return (
            "Moderate-to-high risk detected near the end of service. "
            "Use a smaller refill batch or avoid full refill."
        )

    if probability >= 0.45:
        return (
            "Potential high waste risk detected. Monitor demand closely and apply partial refill if needed."
        )

    if event_type in ["banquet", "wedding", "group_tour"]:
        return (
            "Risk appears manageable. Since guest numbers are clearer for this event type, "
            "maintain planned production but continue monitoring actual demand."
        )

    return (
        "Risk appears low. Maintain current production quantity, but continue recording leftovers "
        "for future planning."
    )


df = load_data()
model = load_model()

st.title("Buffet Food Waste Prediction & Production Planning Dashboard")

st.markdown(
    """
This dashboard demonstrates how data science and machine learning can support buffet production planning
and food waste reduction in hotel kitchen operations.

The project is based on a resort hotel buffet scenario and focuses on identifying high-risk buffet items,
analysing leftover patterns, and supporting refill decisions.
"""
)

tab1, tab2, tab3 = st.tabs([
    "Overview",
    "Waste Analysis",
    "High Waste Risk Prediction"
])


with tab1:
    st.header("Dataset Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Records", len(df))
    col2.metric("Average Leftover Ratio", f"{df['leftover_ratio'].mean():.2f}")
    col3.metric("High Waste Records", int((df["waste_level"] == "High").sum()))
    col4.metric("Average Occupancy Rate", f"{df['occupancy_rate'].mean():.2f}")

    st.subheader("Sample Data")
    st.dataframe(df.head(20))

    st.subheader("Waste Level Distribution")
    waste_counts = df["waste_level"].value_counts().reset_index()
    waste_counts.columns = ["waste_level", "count"]

    fig = px.bar(
        waste_counts,
        x="waste_level",
        y="count",
        title="Waste Level Distribution"
    )
    st.plotly_chart(fig, width="stretch")


with tab2:
    st.header("Buffet Waste Analysis")

    st.subheader("Top 10 Dishes by Average Leftover Ratio")
    dish_waste = (
        df.groupby("dish_name")["leftover_ratio"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig = px.bar(
        dish_waste,
        x="dish_name",
        y="leftover_ratio",
        title="Top 10 Dishes by Average Leftover Ratio"
    )
    st.plotly_chart(fig, width="stretch")

    st.subheader("Average Leftover Ratio by Kitchen Section")
    section_waste = (
        df.groupby("kitchen_section")["leftover_ratio"]
        .mean()
        .sort_values(ascending=False)
        .reset_index()
    )

    fig = px.bar(
        section_waste,
        x="kitchen_section",
        y="leftover_ratio",
        title="Average Leftover Ratio by Kitchen Section"
    )
    st.plotly_chart(fig, width="stretch")

    st.subheader("Average Leftover Ratio by Meal Period")
    meal_waste = (
        df.groupby("meal_period")["leftover_ratio"]
        .mean()
        .sort_values(ascending=False)
        .reset_index()
    )

    fig = px.bar(
        meal_waste,
        x="meal_period",
        y="leftover_ratio",
        title="Average Leftover Ratio by Meal Period"
    )
    st.plotly_chart(fig, width="stretch")

    st.subheader("Average Leftover Ratio by Event Type")
    event_waste = (
        df.groupby("event_type")["leftover_ratio"]
        .mean()
        .sort_values(ascending=False)
        .reset_index()
    )

    fig = px.bar(
        event_waste,
        x="event_type",
        y="leftover_ratio",
        title="Average Leftover Ratio by Event Type"
    )
    st.plotly_chart(fig, width="stretch")


with tab3:
    st.header("High Waste Risk Prediction")

    st.markdown(
        """
Use this form to estimate whether a buffet item may become a high waste risk.
The model predicts high waste risk based on operational conditions before or during service.
"""
    )

    col1, col2 = st.columns(2)

    with col1:
        meal_period = st.selectbox(
            "Meal Period",
            sorted(df["meal_period"].unique())
        )

        dish_category = st.selectbox(
            "Dish Category",
            sorted(df["dish_category"].unique())
        )

        kitchen_section = st.selectbox(
            "Kitchen Section",
            sorted(df["kitchen_section"].unique())
        )

        event_type = st.selectbox(
            "Event Type",
            sorted(df["event_type"].unique())
        )

        weather = st.selectbox(
            "Weather",
            sorted(df["weather"].unique())
        )

    with col2:
        estimated_guests = st.number_input(
            "Estimated Guests",
            min_value=1,
            max_value=500,
            value=120
        )

        occupancy_rate = st.slider(
            "Occupancy Rate",
            min_value=0.00,
            max_value=1.00,
            value=0.70,
            step=0.01
        )

        prepared_qty = st.number_input(
            "Prepared Quantity",
            min_value=0.1,
            max_value=50.0,
            value=8.0,
            step=0.1
        )

        service_time_remaining = st.selectbox(
            "Service Time Remaining (minutes)",
            [15, 30, 45, 60, 90]
        )

        refill_count = st.slider(
            "Refill Count",
            min_value=0,
            max_value=5,
            value=2
        )

    if st.button("Predict High Waste Risk"):
        input_df = build_prediction_input(
            meal_period=meal_period,
            dish_category=dish_category,
            kitchen_section=kitchen_section,
            event_type=event_type,
            weather=weather,
            estimated_guests=estimated_guests,
            occupancy_rate=occupancy_rate,
            prepared_qty=prepared_qty,
            service_time_remaining=service_time_remaining,
            refill_count=refill_count
        )

        probability = model.predict_proba(input_df)[0][1]
        threshold = 0.45
        is_high_risk = probability >= threshold

        st.subheader("Prediction Result")

        col_a, col_b = st.columns(2)

        col_a.metric("High Waste Risk Probability", f"{probability:.2%}")
        col_b.metric("Decision Threshold", f"{threshold:.2f}")

        if is_high_risk:
            st.error("Prediction: High Waste Risk")
        else:
            st.success("Prediction: Not High Waste Risk")

        recommendation = generate_recommendation(
            probability=probability,
            service_time_remaining=service_time_remaining,
            refill_count=refill_count,
            event_type=event_type
        )

        st.subheader("Operational Recommendation")
        st.write(recommendation)

        st.subheader("Model Input")
        st.dataframe(input_df)
