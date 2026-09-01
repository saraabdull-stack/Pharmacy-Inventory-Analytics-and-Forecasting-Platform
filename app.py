import pandas as pd
import requests
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Pharmacy Stock & BNF Predictor", layout="wide"
)

st.title("💊 Pharmalytics")

# 1. Initialize Inventory in Session State
if "inventory" not in st.session_state:
  st.session_state.inventory = pd.DataFrame({
      "Medication": [
          "Amoxicillin 500mg",
          "Paracetamol 500mg",
          "Ibuprofen 400mg",
          "Atorvastatin 20mg",
          "Omeprazole 20mg",
          "Metformin 500mg",
          "Sertraline 50mg",
          "Salbutamol 100mcg Inhaler",
          "Cetirizine 10mg",
          "Lisinopril 10mg",
          "Amlodipine 5mg",
          "Carbamazepine 200mg",
          "Digoxin 0.25mg",
      ],
      "Category": [
          "Antibiotic",
          "Analgesic",
          "Analgesic",
          "Cardiovascular",
          "Gastrointestinal",
          "Diabetes",
          "Mental Health",
          "Respiratory",
          "Allergy",
          "Cardiovascular",
          "Cardiovascular",
          "Mental Health",
          "Cardiovascular"
      ],
      "Current Stock": [120, 1500, 80, 450, 200, 600, 90, 30, 150, 70, 200, 40, 25],
      "Avg Daily Usage": [25, 100, 30, 15, 20, 40, 10, 8, 5, 12, 10, 5, 5],
      "Minimum Stock Threshold": [
          100,
          300,
          100,
          100,
          100,
          150,
          50,
          20,
          50,
          30,
          100,
          50,
          30,
      ],
  })

# Dynamic Column Calculations
df = st.session_state.inventory
df["Days Left"] = (df["Current Stock"] / df["Avg Daily Usage"]).round(1)
df["Reorder Needed"] = df["Current Stock"] <= df["Minimum Stock Threshold"]

# Create Tabs
tab1, tab2 = st.tabs(["📊 Inventory Dashboard", "🔍 Live BNF Lookup"])

# ==========================================
# TAB 1: INVENTORY DASHBOARD
# ==========================================
with tab1:
  col1, col2, col3 = st.columns(3)
  with col1:
    st.metric(label="Total Unique Medications", value=len(df))
  with col2:
    low_stock_count = int(df["Reorder Needed"].sum())
    st.metric(
        label="Items Requiring Reorder",
        value=low_stock_count,
        delta=-low_stock_count if low_stock_count > 0 else 0,
    )
  with col3:
    st.metric(
        label="Total Units in Stock", value=int(df["Current Stock"].sum())
    )

  st.divider()

  st.subheader("Inventory Overview")

  # Side-by-Side Filters
  col_filter1, col_filter2 = st.columns(2)

  with col_filter1:
    selected_categories = st.multiselect(
        "Filter by Category:", options=df["Category"].unique(), default=[]
    )

  with col_filter2:
    search_term = st.text_input("🔍 Search Medication Name:", value="")

  # Combined Filtering Logic
  filtered_df = df.copy()

  # 1. Filter by Category (if selected)
  if selected_categories:
    filtered_df = filtered_df[
        filtered_df["Category"].isin(selected_categories)
    ]

  # 2. Filter by Search Term (if typed)
  if search_term:
    filtered_df = filtered_df[
        filtered_df["Medication"].str.contains(
            search_term, case=False, na=False
        )
    ]

  # Single Clean Table Display
  st.dataframe(
      filtered_df,
      column_config={
          "Current Stock": st.column_config.NumberColumn("Current Stock"),
          "Avg Daily Usage": st.column_config.NumberColumn("Avg Daily Usage"),
          "Days Left": st.column_config.NumberColumn("Days Left"),
          "Reorder Needed": st.column_config.CheckboxColumn("Reorder Needed"),
      },
      use_container_width=True,
      hide_index=True,
  )

  st.subheader("⚠️ Low Stock Alerts")
  reorder_df = df[df["Reorder Needed"]]

  if not reorder_df.empty:
    st.warning(f"{len(reorder_df)} item(s) are below safety threshold levels:")
    for _, row in reorder_df.iterrows():
      st.write(
          f"• **{row['Medication']}**: {row['Current Stock']} units remaining "
          f"(~{row['Days Left']} days left based on daily usage of {row['Avg Daily Usage']})"
      )
  else:
    st.success("All medication stock levels are above the safety threshold.")

  st.subheader("Stock vs. Daily Demand Analysis")
  st.bar_chart(
      data=filtered_df,
      x="Medication",
      y=["Current Stock", "Avg Daily Usage"],
      use_container_width=True,
  )

# ==========================================
# TAB 2: LIVE BNF LOOKUP & ADD
# ==========================================
with tab2:
  st.subheader("Search Official BNF Codes & Add to Inventory")
  search_query = st.text_input(
      "Enter drug name to query BNF database:", "Amoxicillin"
  )

  if search_query:
    api_url = f"https://openprescribing.net/api/1.0/bnf_code/?q={search_query}&format=json"
    response = requests.get(api_url)

    if response.status_code == 200:
      results = response.json()
      if results:
        bnf_df = pd.DataFrame(results)
        bnf_df = bnf_df.rename(columns={"id": "BNF Code", "name": "BNF Name"})

        st.success(f"Found {len(results)} matching BNF records:")
        st.dataframe(
            bnf_df[["BNF Code", "BNF Name"]],
            use_container_width=True,
            hide_index=True,
        )

        st.divider()
        st.subheader("➕ Add Selected Drug to Inventory")

        # Form to enter stock details for the new drug
        with st.form("add_drug_form"):
          selected_drug = st.selectbox(
              "Select BNF Record to Add:", options=bnf_df["BNF Name"].tolist()
          )
          category = st.text_input("Category:", "General Medicine")

          col1, col2, col3 = st.columns(3)
          with col1:
            stock = st.number_input(
                "Initial Stock Quantity:", min_value=1, value=100
            )
          with col2:
            usage = st.number_input(
                "Estimated Daily Usage:", min_value=1, value=10
            )
          with col3:
            threshold = st.number_input(
                "Minimum Stock Threshold:", min_value=1, value=30
            )

          submit = st.form_submit_button("Add to Inventory")

          if submit:
            # Check for duplicate entry
            if (
                selected_drug
                in st.session_state.inventory["Medication"].values
            ):
              st.warning(f"'{selected_drug}' is already in your inventory.")
            else:
              # Create new row entry
              new_item = pd.DataFrame([{
                  "Medication": selected_drug,
                  "Category": category,
                  "Current Stock": stock,
                  "Avg Daily Usage": usage,
                  "Minimum Stock Threshold": threshold,
              }])

              # Append to session state dataframe
              st.session_state.inventory = pd.concat(
                  [st.session_state.inventory, new_item], ignore_index=True
              )
              st.success(
                  f"Added **{selected_drug}** to inventory! Switch to the"
                  " Inventory tab to view."
              )
              st.rerun()
      else:
        st.warning("No matching BNF records found.")
    else:
      st.error("Error connecting to the BNF OpenPrescribing API.")