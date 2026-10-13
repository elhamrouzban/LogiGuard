import json

import os



import pandas as pd

import requests

import streamlit as st



from src.shared.risk import get_risk_level





st.set_page_config(

    page_title="LogiGuard AI",

    page_icon="📦",

    layout="wide",

)



st.markdown(
    """
    <style>
        /* Hide Streamlit chrome (Deploy / menu header) */
        [data-testid="stHeader"],
        [data-testid="stToolbar"],
        [data-testid="stDecoration"],
        #MainMenu,
        footer {
            display: none !important;
            visibility: hidden !important;
        }

        .stApp {
            background:
                radial-gradient(circle at 8% 0%, rgba(37, 99, 235, 0.07), transparent 27%),
                radial-gradient(circle at 92% 0%, rgba(14, 165, 233, 0.05), transparent 24%),
                #f7f9fc;
        }

        .block-container {
            max-width: 1500px;
            padding-top: 0.8rem;
            padding-bottom: 1rem;
            padding-left: 1.4rem;
            padding-right: 1.4rem;
        }

        h1, h2, h3 {
            letter-spacing: -0.02em;
            line-height: 1.15 !important;
            margin-top: 0.15rem !important;
            margin-bottom: 0.35rem !important;
        }

        h1 {
            color: #0f172a;
            font-size: 1.75rem !important;
            font-weight: 800;
        }

        h2 {
            color: #1e293b;
            font-size: 1.18rem !important;
            font-weight: 760;
        }

        h3 {
            color: #334155;
            font-size: 0.98rem !important;
            font-weight: 700;
        }

        [data-testid="stCaptionContainer"] {
            color: #7b8aa0;
            font-size: 0.78rem;
            margin-bottom: 0.1rem;
        }

        [data-testid="stMarkdownContainer"] p {
            font-size: 0.88rem;
            line-height: 1.4;
        }

        div[data-testid="stVerticalBlock"] {
            gap: 0.42rem;
        }

        /* Compact KPI cards */
        [data-testid="stMetric"] {
            width: 100%;
            max-width: 225px;
            min-height: 68px;
            margin-left: auto;
            margin-right: auto;
            background: rgba(255, 255, 255, 0.96);
            border: 1px solid #e3e8ef;
            border-radius: 12px;
            padding: 0.55rem 0.72rem;
            box-shadow: 0 5px 16px rgba(15, 23, 42, 0.045);
        }

        [data-testid="stMetricLabel"] {
            color: #64748b;
            font-weight: 650;
            font-size: 0.72rem !important;
        }

        [data-testid="stMetricValue"] {
            color: #0f172a;
            font-weight: 800;
            font-size: 1.15rem !important;
            line-height: 1.1 !important;
        }

        /* Compact navigation */
        .stTabs [data-baseweb="tab-list"] {
            gap: 0.15rem;
            background: transparent;
            border-bottom: 1px solid #dde3eb;
            border-radius: 0;
            padding: 0;
            box-shadow: none;
        }

        .stTabs [data-baseweb="tab"] {
            min-height: 2rem;
            border-radius: 8px 8px 0 0;
            padding: 0.32rem 0.68rem;
            font-size: 0.80rem;
            font-weight: 650;
            color: #475569;
        }

        .stTabs [aria-selected="true"] {
            background: #eef4ff;
            color: #1d4ed8;
        }

        label,
        [data-testid="stWidgetLabel"] {
            font-size: 0.78rem !important;
            font-weight: 650 !important;
            color: #475569 !important;
        }

        /* Search/select fields stay intentionally compact */
        .stSelectbox {
            max-width: 540px;
        }

        div[data-baseweb="select"] > div,
        .stTextInput input,
        .stTextArea textarea {
            border-radius: 10px !important;
            border: 1px solid #d5dce6 !important;
            background: rgba(255, 255, 255, 0.98) !important;
            font-size: 0.84rem !important;
        }

        div[data-baseweb="select"] > div {
            min-height: 2.15rem !important;
            box-shadow: 0 2px 8px rgba(15, 23, 42, 0.025);
        }

        div[data-baseweb="select"] > div:hover {
            border-color: #9cb8ee !important;
            background: #fbfdff !important;
        }

        div[data-baseweb="select"] > div:focus-within,
        .stTextInput input:focus,
        .stTextArea textarea:focus {
            border-color: #4f7fe8 !important;
            box-shadow: 0 0 0 2px rgba(79, 127, 232, 0.11) !important;
        }

        /* Keep dropdown menus from taking over the screen */
        [role="listbox"] {
            max-height: 260px !important;
        }

        .stButton > button,
        .stFormSubmitButton > button {
            border-radius: 9px;
            min-height: 2.15rem;
            padding: 0.3rem 0.8rem;
            font-size: 0.80rem;
            font-weight: 700;
            transition: transform 0.15s ease, box-shadow 0.15s ease;
        }

        .stButton > button:hover,
        .stFormSubmitButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 5px 13px rgba(37, 99, 235, 0.12);
        }

        [data-testid="stDataFrame"] {
            border: 1px solid #e2e8f0;
            border-radius: 11px;
            overflow: hidden;
            box-shadow: 0 4px 14px rgba(15, 23, 42, 0.035);
            background: white;
        }

        [data-testid="stExpander"] {
            border: 1px solid #e2e8f0;
            border-radius: 10px;
            background: rgba(255, 255, 255, 0.95);
            box-shadow: 0 3px 10px rgba(15, 23, 42, 0.03);
        }

        /* Raw-order form should be a focused card, not full width */
        [data-testid="stForm"] {
            width: 100%;
            max-width: 860px;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 0.65rem 0.8rem 0.35rem 0.8rem;
            background: rgba(255, 255, 255, 0.96);
            box-shadow: 0 5px 16px rgba(15, 23, 42, 0.04);
        }

        [data-testid="stAlert"] {
            max-width: 860px;
            border-radius: 10px;
            padding-top: 0.5rem;
            padding-bottom: 0.5rem;
        }

        hr {
            border: none;
            border-top: 1px solid #e2e8f0;
            margin: 0.55rem 0;
        }

        @media (max-width: 900px) {
            .block-container {
                padding-left: 0.8rem;
                padding-right: 0.8rem;
            }

            h1 {
                font-size: 1.5rem !important;
            }

            h2 {
                font-size: 1.08rem !important;
            }

            [data-testid="stMetric"] {
                max-width: none;
            }

            .stSelectbox,
            [data-testid="stForm"] {
                max-width: none;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)






API_URL = os.getenv(

    "API_URL",

    "http://127.0.0.1:8000",

)





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





dashboard_tab, orders_tab, new_order_tab, operations_colilot_tab = (

    st.tabs(

        [

            "Dashboard",

            "Order Details",

            "New Raw Order",

            "Operations Copilot",



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



                available_order_ids = (

                    shipments_df["Order ID"]

                    .astype(int)

                    .sort_values()

                    .tolist()

                )



                searched_order_id = st.selectbox(

                    "Search by Order ID",

                    options=available_order_ids,

                    index=None,

                    placeholder="Search and select an Order ID...",

                    key="dashboard_search",

                )



                if searched_order_id is None:

                    filtered_df = shipments_df.copy()

                else:

                    filtered_df = shipments_df[

                        shipments_df["Order ID"] == searched_order_id

                    ]

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

                    height=260,

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

    shipments = fetch_json("/shipments")

    if shipments:

        order_ids = sorted(
            shipment["order_id"]
            for shipment in shipments
        )

        order_search = st.selectbox(
            "Order ID",
            options=order_ids,
            index=None,
            placeholder="Search and select an Order ID...",
            key="details_search",
        )

        if st.button(
            "Search Order",
            key="details_search_button",
        ):

            if order_search is None:

                st.warning(
                    "Please select an Order ID."
                )

            else:

                st.session_state[
                    "details_order_id"
                ] = order_search

    else:

        st.info(
            "No shipments are available."
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
                        f"{shipment['late_risk_probability']:.1%}"
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

            height=150,

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





# =========================================================

# OPERATIONS COPILOT

# =========================================================



with operations_colilot_tab:

    st.header("Operations Copilot")



    shipments = fetch_json("/shipments")



    if not shipments:

        st.info(

            "No shipments are available for Copilot queries."

        )



    else:

        order_ids = sorted(

            shipment["order_id"]

            for shipment in shipments

        )



        selected_order_id = st.selectbox(

            "Order ID",

            options=order_ids,

            index=None,

            placeholder="Search and select an Order ID...",

            key="copilot_order_id",

        )



        action = st.selectbox(

            "What would you like to know?",

            options=[

                "Risk Prediction",

                "Shipment Status",

                "Similar Shipments",

            ],

            index=None,

            placeholder="Select an action...",

            key="copilot_action",

        )



        if st.button(

            "Ask Copilot",

            type="primary",

            key="copilot_submit",

        ):

            if selected_order_id is None:

                st.warning(

                    "Please select an Order ID."

                )



            elif action is None:

                st.warning(

                    "Please select an action."

                )



            else:



                action_mapping = {

                    "Risk Prediction": "prediction",

                    "Shipment Status": "shipment_status",

                    "Similar Shipments": "similar_shipments",

                }



                try:

                    response = requests.post(

                        f"{API_URL}/copilot",

                        json={

                            "order_id": selected_order_id,

                            "action": action_mapping[action],

                        },

                        timeout=30,

                    )



                    if response.ok:

                        result = response.json()



                        answer = result.get("answer")



                        if answer:

                            st.markdown(answer)

                        else:

                            st.info(

                                "Copilot returned validated evidence "

                                "without a generated explanation."

                            )



                        with st.expander("Validated Evidence"):

                            evidence = {

                                key: value

                                for key, value in result.items()

                                if key != "answer"

                            }



                            st.json(evidence)



                    else:

                        st.error(

                            "Copilot request failed: "

                            f"{response.status_code}"

                        )



                except requests.RequestException as exc:

                    st.error(

                        "Could not connect to FastAPI: "

                        f"{exc}"

                    )