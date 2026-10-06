import os

import requests
import streamlit as st

import requests
import streamlit as st


st.set_page_config(
    page_title="LogiGuard AI",
    page_icon="📦",
    layout="wide",
)

st.title("LogiGuard AI")
st.subheader("Logistics Exception Management Dashboard")

st.write(
    "Monitor shipment risk, review high-risk orders, "
    "and inspect prediction details."
)

API_URL = os.getenv(
    "API_URL",
    "http://127.0.0.1:8000",
)

st.subheader("Shipment Exceptions")

try:
    response = requests.get(
        f"{API_URL}/shipments",
        timeout=10,
    )

    if response.status_code == 200:
        shipments = response.json()

        if shipments:
            st.dataframe(
                shipments,
                use_container_width=True,
            )

            st.subheader("Selected Shipment Details")

            order_ids = [shipment["order_id"] for shipment in shipments]

            selected_order_id = st.selectbox(
                "Select an Order ID",
                order_ids,
            )

            detail_response = requests.get(
                f"{API_URL}/shipments/{selected_order_id}",
                timeout=10,
            )

            if detail_response.status_code == 200:
                shipment_detail = detail_response.json()

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric(
                        "Risk Probability",
                        f"{shipment_detail['late_risk_probability']:.1%}",
                    )
                    st.write("Risk Label:", shipment_detail["risk_label"])

                with col2:
                    st.write("Order ID:", shipment_detail["order_id"])
                    st.write("Customer ID:", shipment_detail["customer_id"])
                    st.write("Shipping Mode:", shipment_detail["shipping_mode"])

                with col3:
                    st.write("Country:", shipment_detail["order_country"])
                    st.write("Region:", shipment_detail["order_region"])
                    st.write("Model Run:", shipment_detail["model_run_id"])

            else:
                st.error("Could not load shipment details.")
        else:
            st.info("No shipments available.")

    else:
        st.error(
            f"Could not load shipments. "
            f"API returned status code {response.status_code}."
        )

except requests.RequestException as exc:
    st.error(
        f"Could not connect to FastAPI: {exc}"
    )