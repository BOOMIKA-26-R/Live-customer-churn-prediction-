import streamlit as st
import requests
import time

st.set_page_config(page_title="Churn Radar", layout="wide")
st.title("📉 Real-Time Customer Churn Radar")


BASE_URL = " https://live-customer-churn-prediction.onrender.com" 

st.sidebar.header("Alert Settings")
risk_threshold = st.sidebar.slider("Churn Risk Threshold", 0.0, 1.0, 0.7)

st.sidebar.markdown("---")
st.sidebar.subheader("Admin Actions")

if st.sidebar.button("Retrain Churn Model"):
    with st.spinner("Updating AI Model..."):
        try:

            retrain_res = requests.post(f"{BASE_URL}/retrain").json()
            st.sidebar.success(retrain_res["message"])
            time.sleep(1)
        except Exception as e:
            st.sidebar.error(f"Retrain failed: {e}")

if st.button("Analyze Next Customer"):
    try:
        cust_res = requests.get(f"{BASE_URL}/live-customer").json()
        
        params = {
            "charges": cust_res['monthly_charges'], 
            "tenure": cust_res['tenure_months'], 
            "calls": cust_res['support_calls']
        }
        pred_res = requests.get(f"{BASE_URL}/predict", params=params).json()
        
        risk = pred_res['churn_probability']
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.info("### Customer Profile")
            st.write(f"**Customer ID:** {cust_res['customer_id']}")
            st.write(f"**Monthly Charges:** ${cust_res['monthly_charges']}")
            st.write(f"**Tenure:** {cust_res['tenure_months']} Months")
            st.write(f"**Support Calls:** {cust_res['support_calls']}")
            
        with col2:
            st.info("### AI Analysis")
            st.metric("Churn Probability", f"{risk*100:.1f}%")
            
            if risk > risk_threshold:
                st.error("🚨 HIGH RISK: This customer is likely to leave!")
            else:
                st.success("✅ LOW RISK: Customer behavior is stable.")
                
    except Exception as e:
        st.error(f"Connection Error: Is your API running at {BASE_URL}? \n\nError: {e}")

st.divider()
st.caption(f"Connected to Backend: {BASE_URL}")
