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

API_URL = "http://127.0.0.1:8000"

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