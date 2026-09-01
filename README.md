# Pharmalytics 💊📊

Pharmalytics is a Python-based pharmacy inventory management dashboard. It helps monitor medication stock levels, identify medicines requiring reordering, and retrieve BNF information through a live API.

The project combines pharmacy knowledge, data analysis and software development to explore how simple digital tools can support pharmacy inventory management.

## 📷 Preview
<img width="1438" height="762" alt="Screenshot 2026-09-01 at 21 01 41" src="https://github.com/user-attachments/assets/15c511e8-1eff-4689-910e-8f0fa4196b94" />

<img width="1440" height="686" alt="Screenshot 2026-09-01 at 21 01 51" src="https://github.com/user-attachments/assets/6897ad19-376a-40ba-8fbc-bb05a8b8e586" />

## 🚀 Features
### 📊 Inventory Dashboard
- View total unique medications and overall stock levels
- Monitor current stock against minimum stock thresholds
- Calculate estimated days of stock remaining based on average daily usage
- Automatically flag medicines requiring reorder
- Search and filter medicines by name and category
- Visualise stock levels against daily demand
- Display low-stock alerts
  
### 🔍 Live BNF Lookup
- Search for medicines using a live BNF database
- Retrieve BNF codes and medication names through the OpenPrescribing API
- Select a medicine from the search results
- Add new medicines directly to the inventory
- Set initial stock, estimated daily usage and minimum stock thresholds
- Prevent duplicate medicines from being added
  
## 🛠️ Technologies
- Python — application logic and data processing
- Pandas — inventory data management and calculations
- Streamlit — interactive web dashboard
- Requests — API requests
- Git & GitHub — version control and project sharing

## ⚙️ How to run
1. Clone the repository
   
```bash
git clone https://github.com/saraabdull-stack/Pharmacy-Inventory-Analytics-and-Forecasting-Platform.git
cd Pharmacy-Inventory-Analytics-and-Forecasting-Platform
```

3. Install dependencies

```bash
pip install -r requirements.txt
```
 3. Run the app

```bash
streamlit run app.py
```

## 📈 How it works

- The application calculates the estimated number of days of stock remaining using:

*Days Left = Current Stock ÷ Average Daily Usage*

- A medicine is flagged for reorder when:

*Current Stock ≤ Minimum Stock Threshold*

This allows users to quickly identify medicines that may require replenishment.

## 💡 Why I built this

As a pharmacy student with growing experience in technology and data, I wanted to explore how I could combine my clinical knowledge with my technical skills to address a real-world problem within community pharmacy.

Community pharmacies can face a persistent gap between patient demand and medication supply. When stock levels do not accurately reflect demand, medicines may become unavailable when patients need them, while pharmacies can also be left holding excess stock that is not being used efficiently.

Pharmalytics is my first attempt at creating a small-scale model of a platform that could help address this problem. The aim is to move beyond simply recording inventory and towards using data on stock levels and medication demand to support better inventory decisions.

## 🔮 Future improvements

Potential future developments include:
- Persistent database storage
- User authentication and different access levels
- Medicine expiry-date tracking
- Automated stock alerts
- Prescription/dispensing data integration
- Improved BNF search functionality
- Integrate medication pricing data to compare supplier prices
- Interactive inventory analytics
- Deployment as a publicly accessible web application
  
## ⚠️ Disclaimer

This project is an educational/portfolio project and is not intended to replace professional pharmacy stock management systems, the BNF, or clinical decision-making tools.

The inventory data included in the application is example data.

## 👩‍💻 Author

Sara Haji Abdullahi

MPharm Pharmacy Student | Python & Data Analytics

Interested in combining clinical knowledge, technology and data analytics to develop solutions to real-world challenges.
