import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Wind Turbine Monitoring", layout="wide")
st.title("🔌 Wind Turbine Real-Time Monitoring System")

try:
    # قراءة الملف من نفس المسار على جيت هاب
    df = pd.read_csv("T1.csv",encoding='latin-1')
    
    # التأكد من حساب الفقد
    df['Loss'] = df['Theoretical_Power_Curve (KWh)'] - df['LV ActivePower (kW)']
    latest_data = df.iloc[-1] 

    col1, col2, col3, col4 = st.columns(4)
    # الأسماء دي متعدلة عشان تطابق ملف الـ CSV بتاعك بالظبط
    col1.metric("Wind Speed", f"{latest_data['Wind Speed (m/s)']:.2f} m/s")
    col2.metric("Actual Power", f"{latest_data['LV ActivePower (kW)']:.2f} kW")
    col3.metric("Theoretical Power", f"{latest_data['Theoretical_Power_Curve (KWh)']:.2f} kW")
    
    status = "⚠️ Maintenance Required" if latest_data['Loss'] > 500 else "✅ Normal Operation"
    col4.metric("System Status", status)

    st.subheader("📊 Performance Analysis")
    fig = px.scatter(df.head(2000), x='Wind Speed (m/s)', y=['LV ActivePower (kW)', 'Theoretical_Power_Curve (KWh)'])
    st.plotly_chart(fig, use_container_width=True)
    
    st.dataframe(df.tail(10), use_container_width=True)

except Exception as e:
    st.error(f"خطأ في قراءة البيانات: {e}")
