import json
import os

import pandas as pd
import requests
import streamlit as st


st.set_page_config(
    page_title="LogiGuard AI",
    page_icon="📦",
    layout="wide",
)


API_URL = os.getenv(
    "API_URL",
    "http://127.0.0.1:8000",
)


def get_risk_level(probability: float) -> str:
    if probability < 0.40:
        return "No Risk"

    if probability < 0.60:
        return "Low Risk"

    if probability < 0.80:
        return "Medium Risk"

    return "High Risk"


def get_risk_emoji(risk_level: str) -> str:
    mapping = {
        "No Risk": "🟢",
        "Low Risk": "🟡",
        "Medium Risk": "🟠",
        "High Risk": "🔴",
    }

    return mapping.get(risk_level, "⚪")


def style_risk_row(row):
    risk_level = row["Risk Level"]

    if risk_level == "High Risk":
        return [
            "background-color: rgba(255, 0, 0, 0.18)"
        ] * len(row)

    if risk_level == "Medium Risk":
        return [
            "background-color: rgba(255, 165, 0, 0.18)"
        ] * len(row)

    if risk_level == "Low Risk":
        return [
            "background-color: rgba(255, 215, 0, 0.18)"
        ] * len(row)

    return [
        "background-color: rgba(0, 180, 0, 0.14)"
    ] * len(row)


def fetch_json(endpoint: str):
    try:
        response = requests.get(
            f"{API_URL}{endpoint}",
            timeout=10,
        )

        if response.status_code == 200:
            return response.json()

        return None

    except requests.RequestException:
        return None


def show_order_overview(order_id: int):
    shipment = fetch_json(
        f"/shipments/{order_id}"
    )

    raw_order_record = fetch_json(
        f"/raw-orders/{order_id}"
    )

    if shipment is None:
        st.error(
            "Could not load order overview."
        )
        return

    probability = shipment[
        "late_risk_probability"
    ]

    risk_level = get_risk_level(
        probability
    )

    risk_emoji = get_risk_emoji(
        risk_level
    )

    scheduled_shipping_days = None

    if raw_order_record is not None:
        raw_payload = raw_order_record.get(
            "raw_payload",
            {},
        )

        scheduled_shipping_days = (
            raw_payload.get(
                "scheduled_shipping_days"
            )
        )

    st.subheader(
        f"Order #{order_id}"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Risk Level",
            f"{risk_emoji} {risk_level}",
        )

    with col2:
        st.metric(
            "Late Risk Probability",
            f"{probability:.1%}",
        )

    with col3:
        st.metric(
            "Prediction",
            shipment["risk_label"],
        )

    with col4:
        if scheduled_shipping_days is not None:
            st.metric(
                "Scheduled Shipping",
                f"{scheduled_shipping_days} days",
            )
        else:
            st.metric(
                "Scheduled Shipping",
                "N/A",
            )

    st.caption(
        f"Model: {shipment['model_run_id']}"
    )


def show_raw_order(order_id: int):
    raw_record = fetch_json(
        f"/raw-orders/{order_id}"
    )

    if raw_record is None:
        st.info(
            "Raw order data is not available."
        )
        return

    raw_payload = raw_record.get(
        "raw_payload",
        {},
    )

    items = raw_payload.get(
        "items",
        [],
    )

    top_level_data = {
        key: value
        for key, value in raw_payload.items()
        if key != "items"
    }

    raw_table = pd.DataFrame(
        {
            "Field": list(
                top_level_data.keys()
            ),
            "Value": [
                str(value)
                for value
                in top_level_data.values()
            ],
        }
    )

    st.caption(
        f"Received at: "
        f"{raw_record.get('received_at', 'N/A')}"
    )

    st.dataframe(
        raw_table,
        use_container_width=True,
        hide_index=True,
    )

    st.subheader(
        f"Items ({len(items)})"
    )

    if items:
        st.dataframe(
            pd.DataFrame(items),
            use_container_width=True,
            hide_index=True,
        )

    else:
        st.info(
            "No items found."
        )


def show_processed_order(order_id: int):
    order = fetch_json(
        f"/orders/{order_id}"
    )

    if order is None:
        st.info(
            "Processed order data is not available."
        )
        return

    processed_table = pd.DataFrame(
        {
            "Field": list(order.keys()),
            "Value": [
                str(value)
                for value in order.values()
            ],
        }
    )

    st.dataframe(
        processed_table,
        use_container_width=True,
        hide_index=True,
    )


def show_prediction(order_id: int):
    prediction = fetch_json(
        f"/predictions/{order_id}"
    )

    if prediction is None:
        st.info(
            "Prediction data is not available."
        )
        return

    probability = prediction[
        "late_risk_probability"
    ]

    risk_level = get_risk_level(
        probability
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Risk Probability",
            f"{probability:.1%}",
        )

    with col2:
        st.metric(
            "Risk Level",
            (
                f"{get_risk_emoji(risk_level)} "
                f"{risk_level}"
            ),
        )

    with col3:
        st.metric(
            "Prediction",
            prediction["risk_label"],
        )

    prediction_table = pd.DataFrame(
        {
            "Field": list(
                prediction.keys()
            ),
            "Value": [
                str(value)
                for value
                in prediction.values()
            ],
        }
    )

    st.dataframe(
        prediction_table,
        use_container_width=True,
        hide_index=True,
    )


st.title("📦 LogiGuard AI")

st.caption(
    "Logistics Delay Risk Monitoring "
    "and Exception Management"
)


dashboard_tab, orders_tab, new_order_tab = (
    st.tabs(
        [
            "Dashboard",
            "Order Details",
            "New Raw Order",
        ]
    )
)


# =========================================================
# DASHBOARD
# =========================================================

with dashboard_tab:
    st.header(
        "Shipment Risk Dashboard"
    )

    try:
        response = requests.get(
            f"{API_URL}/shipments",
            timeout=10,
        )

        if response.status_code != 200:
            st.error(
                "Could not load shipments."
            )

        else:
            shipments = response.json()

            if not shipments:
                st.info(
                    "No shipments available."
                )

            else:
                shipment_rows = []

                for shipment in shipments:
                    probability = shipment[
                        "late_risk_probability"
                    ]

                    risk_level = get_risk_level(
                        probability
                    )

                    shipment_rows.append(
                        {
                            "Order ID": shipment[
                                "order_id"
                            ],
                            "Customer ID": shipment[
                                "customer_id"
                            ],
                            "Country": shipment[
                                "order_country"
                            ],
                            "Region": shipment[
                                "order_region"
                            ],
                            "Shipping Mode": shipment[
                                "shipping_mode"
                            ],
                            "Probability": probability,
                            "Risk Level": risk_level,
                            "Prediction": shipment[
                                "risk_label"
                            ],
                            "Model": shipment[
                                "model_run_id"
                            ],
                        }
                    )

                shipments_df = pd.DataFrame(
                    shipment_rows
                )

                shipments_df = (
                    shipments_df.sort_values(
                        "Probability",
                        ascending=False,
                    )
                )

                total_orders = len(
                    shipments_df
                )

                no_risk_count = (
                    shipments_df[
                        "Risk Level"
                    ]
                    == "No Risk"
                ).sum()

                low_risk_count = (
                    shipments_df[
                        "Risk Level"
                    ]
                    == "Low Risk"
                ).sum()

                medium_risk_count = (
                    shipments_df[
                        "Risk Level"
                    ]
                    == "Medium Risk"
                ).sum()

                high_risk_count = (
                    shipments_df[
                        "Risk Level"
                    ]
                    == "High Risk"
                ).sum()

                col1, col2, col3, col4, col5 = (
                    st.columns(5)
                )

                col1.metric(
                    "Total Orders",
                    total_orders,
                )

                col2.metric(
                    "🟢 No Risk",
                    int(no_risk_count),
                )

                col3.metric(
                    "🟡 Low Risk",
                    int(low_risk_count),
                )

                col4.metric(
                    "🟠 Medium Risk",
                    int(medium_risk_count),
                )

                col5.metric(
                    "🔴 High Risk",
                    int(high_risk_count),
                )

                st.divider()

                search_order = st.text_input(
                    "Search by Order ID",
                    placeholder=(
                        "Enter an Order ID..."
                    ),
                    key="dashboard_search",
                )

                filtered_df = (
                    shipments_df.copy()
                )

                if search_order.strip():
                    try:
                        searched_id = int(
                            search_order.strip()
                        )

                        filtered_df = (
                            shipments_df[
                                shipments_df[
                                    "Order ID"
                                ]
                                == searched_id
                            ]
                        )

                        if filtered_df.empty:
                            st.warning(
                                "Order ID not found."
                            )

                    except ValueError:
                        st.warning(
                            "Order ID must be a number."
                        )

                display_df = (
                    filtered_df.copy()
                )

                display_df[
                    "Probability"
                ] = display_df[
                    "Probability"
                ].map(
                    lambda value: (
                        f"{value:.1%}"
                    )
                )

                st.subheader(
                    "Orders by Risk"
                )

                styled_df = (
                    display_df.style.apply(
                        style_risk_row,
                        axis=1,
                    )
                )

                st.dataframe(
                    styled_df,
                    use_container_width=True,
                    hide_index=True,
                )

                if not filtered_df.empty:
                    st.subheader(
                        "Quick Order Overview"
                    )

                    available_ids = (
                        filtered_df[
                            "Order ID"
                        ]
                        .astype(int)
                        .tolist()
                    )

                    selected_order_id = (
                        st.selectbox(
                            "Select Order ID",
                            available_ids,
                            key=(
                                "dashboard_order_select"
                            ),
                        )
                    )

                    if st.button(
                        "View Details",
                        type="primary",
                        key=(
                            "dashboard_view_details"
                        ),
                    ):
                        st.session_state[
                            "selected_order_id"
                        ] = selected_order_id

                        show_order_overview(
                            selected_order_id
                        )

                        with st.expander(
                            "More Details",
                            expanded=True,
                        ):
                            raw_tab, processed_tab, prediction_tab = (
                                st.tabs(
                                    [
                                        "Raw Order",
                                        "Processed Order",
                                        "Prediction",
                                    ]
                                )
                            )

                            with raw_tab:
                                show_raw_order(
                                    selected_order_id
                                )

                            with processed_tab:
                                show_processed_order(
                                    selected_order_id
                                )

                            with prediction_tab:
                                show_prediction(
                                    selected_order_id
                                )

    except requests.RequestException as exc:
        st.error(
            f"Could not connect to FastAPI: {exc}"
        )


# =========================================================
# ORDER DETAILS
# =========================================================

with orders_tab:
    st.header(
        "Order Details"
    )

    order_search = st.text_input(
        "Order ID",
        placeholder=(
            "Enter an Order ID..."
        ),
        key="details_search",
    )

    if st.button(
        "Search Order",
        key="details_search_button",
    ):
        if not order_search.strip():
            st.warning(
                "Enter an Order ID."
            )

        else:
            try:
                order_id = int(
                    order_search.strip()
                )

                shipment = fetch_json(
                    f"/shipments/{order_id}"
                )

                if shipment is None:
                    st.error(
                        "Order not found."
                    )

                else:
                    st.session_state[
                        "details_order_id"
                    ] = order_id

            except ValueError:
                st.error(
                    "Order ID must be a number."
                )

    details_order_id = (
        st.session_state.get(
            "details_order_id"
        )
    )

    if details_order_id is not None:
        show_order_overview(
            details_order_id
        )

        st.divider()

        overview_tab, raw_tab, processed_tab, prediction_tab = (
            st.tabs(
                [
                    "Overview",
                    "Raw Order",
                    "Processed Order",
                    "Prediction",
                ]
            )
        )

        with overview_tab:
            shipment = fetch_json(
                f"/shipments/{details_order_id}"
            )

            if shipment is not None:
                overview_data = {
                    "Order ID": shipment[
                        "order_id"
                    ],
                    "Customer ID": shipment[
                        "customer_id"
                    ],
                    "Country": shipment[
                        "order_country"
                    ],
                    "Region": shipment[
                        "order_region"
                    ],
                    "Shipping Mode": shipment[
                        "shipping_mode"
                    ],
                    "Prediction": shipment[
                        "risk_label"
                    ],
                    "Probability": (
                        f"{shipment[
                            'late_risk_probability'
                        ]:.1%}"
                    ),
                    "Model Run": shipment[
                        "model_run_id"
                    ],
                }

                overview_table = pd.DataFrame(
                    {
                        "Field": list(
                            overview_data.keys()
                        ),
                        "Value": list(
                            overview_data.values()
                        ),
                    }
                )

                st.dataframe(
                    overview_table,
                    use_container_width=True,
                    hide_index=True,
                )

        with raw_tab:
            show_raw_order(
                details_order_id
            )

        with processed_tab:
            show_processed_order(
                details_order_id
            )

        with prediction_tab:
            show_prediction(
                details_order_id
            )


# =========================================================
# NEW RAW ORDER
# =========================================================

with new_order_tab:
    st.header(
        "Process New Raw Order"
    )

    st.write(
        "Paste one complete raw order JSON. "
        "LogiGuard will validate, process, "
        "store, and predict the order."
    )

    with st.form(
        "raw_order_form"
    ):
        raw_order_text = st.text_area(
            "Raw Order JSON",
            height=400,
            placeholder=(
                "Paste one complete "
                "raw order JSON here..."
            ),
        )

        submitted = (
            st.form_submit_button(
                "Process Raw Order",
                type="primary",
            )
        )

    if submitted:
        if not raw_order_text.strip():
            st.error(
                "Raw order JSON is required."
            )

        else:
            try:
                raw_order = json.loads(
                    raw_order_text
                )

            except json.JSONDecodeError as exc:
                st.error(
                    f"Invalid JSON: {exc.msg}"
                )

            else:
                try:
                    prediction_response = (
                        requests.post(
                            (
                                f"{API_URL}"
                                "/predict/raw"
                            ),
                            json=raw_order,
                            timeout=30,
                        )
                    )

                    if (
                        prediction_response
                        .status_code
                        == 200
                    ):
                        result = (
                            prediction_response
                            .json()
                        )

                        probability = result[
                            "late_risk_probability"
                        ]

                        risk_level = (
                            get_risk_level(
                                probability
                            )
                        )

                        st.success(
                            "Order processed successfully."
                        )

                        result_col1, result_col2, result_col3 = (
                            st.columns(3)
                        )

                        with result_col1:
                            st.metric(
                                "Order ID",
                                result[
                                    "order_id"
                                ],
                            )

                        with result_col2:
                            st.metric(
                                "Risk Probability",
                                f"{probability:.1%}",
                            )

                        with result_col3:
                            st.metric(
                                "Risk Level",
                                (
                                    f"{get_risk_emoji(risk_level)} "
                                    f"{risk_level}"
                                ),
                            )

                        st.write(
                            "Prediction:",
                            result[
                                "risk_label"
                            ],
                        )

                        st.write(
                            "Model:",
                            result[
                                "model_run_id"
                            ],
                        )

                    elif (
                        prediction_response
                        .status_code
                        == 409
                    ):
                        detail = (
                            prediction_response
                            .json()
                            .get(
                                "detail",
                                (
                                    "Order already "
                                    "exists."
                                ),
                            )
                        )

                        st.warning(
                            detail
                        )

                    elif (
                        prediction_response
                        .status_code
                        == 422
                    ):
                        detail = (
                            prediction_response
                            .json()
                            .get(
                                "detail",
                                (
                                    "Raw order "
                                    "validation failed."
                                ),
                            )
                        )

                        st.error(
                            detail
                        )

                    else:
                        try:
                            detail = (
                                prediction_response
                                .json()
                                .get(
                                    "detail",
                                    (
                                        "Prediction "
                                        "failed."
                                    ),
                                )
                            )

                        except ValueError:
                            detail = (
                                "Prediction failed."
                            )

                        st.error(
                            f"{detail} "
                            f"Status code: "
                            f"{prediction_response.status_code}"
                        )

                except requests.RequestException as exc:
                    st.error(
                        "Could not connect to "
                        f"FastAPI: {exc}"
                    )