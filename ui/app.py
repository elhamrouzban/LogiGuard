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


st.subheader("New Shipment Prediction")

with st.form("prediction_form"):
    order_id = st.number_input(
        "Order ID",
        min_value=1,
        step=1,
    )

    customer_id = st.number_input(
        "Customer ID",
        min_value=0,
        step=1,
    )

    order_date = st.text_input(
        "Order Date",
        value="2026-10-06T12:00:00",
    )

    order_type = st.selectbox(
        "Type",
        ["DEBIT", "TRANSFER", "PAYMENT", "CASH"],
    )

    customer_segment = st.selectbox(
        "Customer Segment",
        ["Consumer", "Corporate", "Home Office"],
    )

    customer_state = st.text_input(
        "Customer State",
        value="CA",
    )

    order_country = st.text_input(
        "Order Country",
        value="Estados Unidos",
    )

    order_region = st.text_input(
        "Order Region",
        value="West of USA",
    )

    shipping_mode = st.selectbox(
        "Shipping Mode",
        [
            "Standard Class",
            "Second Class",
            "First Class",
            "Same Day",
        ],
    )

    total_quantity = st.number_input(
        "Total Quantity",
        min_value=1,
        step=1,
    )

    total_discount = st.number_input(
        "Total Discount",
        min_value=0.0,
        step=1.0,
    )

    num_unique_products = st.number_input(
        "Unique Products",
        min_value=1,
        step=1,
    )

    num_unique_categories = st.number_input(
        "Unique Categories",
        min_value=1,
        step=1,
    )

    num_unique_departments = st.number_input(
        "Unique Departments",
        min_value=1,
        step=1,
    )

    submitted = st.form_submit_button("Predict")


if submitted:
    payload = {
        "order_id": int(order_id),
        "customer_id": int(customer_id),
        "order_date": order_date,
        "type": order_type,
        "customer_segment": customer_segment,
        "customer_state": customer_state,
        "order_country": order_country,
        "order_region": order_region,
        "shipping_mode": shipping_mode,
        "total_quantity": int(total_quantity),
        "total_discount": float(total_discount),
        "num_unique_products": int(num_unique_products),
        "num_unique_categories": int(num_unique_categories),
        "num_unique_departments": int(num_unique_departments),
    }

    try:
        prediction_response = requests.post(
            f"{API_URL}/predict",
            json=payload,
            timeout=10,
        )

        if prediction_response.status_code == 200:
            result = prediction_response.json()

            st.success("Prediction completed successfully.")

            st.metric(
                "Predicted Risk Probability",
                f"{result['late_risk_probability']:.1%}",
            )

            st.write(
                "Prediction:",
                result["late_risk_prediction"],
            )

            st.write(
                "Risk Label:",
                result["risk_label"],
            )

            st.write(
                "Model Run:",
                result["model_run_id"],
            )

        elif prediction_response.status_code == 409:
            st.warning("Order ID already exists.")

        else:
            st.error(
                f"Prediction failed. "
                f"Status code: {prediction_response.status_code}"
            )

    except requests.RequestException as exc:
        st.error(
            f"Could not connect to FastAPI: {exc}"
        )