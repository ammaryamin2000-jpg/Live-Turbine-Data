import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Wind Turbine Monitoring", layout="wide")
st.title("🔌 Wind Turbine Real-Time Monitoring System")

try:
    # قراءة الملف بأقصى مرونة
    df = pd.read_csv("T1.csv", encoding='latin-1', on_bad_lines='skip', engine='python')
    
    # تحويل كل البيانات لأرقام (عشان لو فيه نص يبوظ القراءة)
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    df = df.dropna() # مسح أي سطور فاضية

    # بدلاً من الأسماء، هنستخدم رقم العمود (0 هو الأول، 1 هو التاني، وهكذا)
    # تأكد أن ترتيب أعمدتك في الملف: Speed, ActivePower, TheoreticalPower
    wind_speed = df.iloc[:, 1] # العمود التاني
    active_power = df.iloc[:, 2] # العمود التالت
    theory_power = df.iloc[:, 3] # العمود الرابع
    
    latest_speed = wind_speed.iloc[-1]
    latest_active = active_power.iloc[-1]
    latest_theory = theory_power.iloc[-1]
    loss = latest_theory - latest_active

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Wind Speed", f"{latest_speed:.2f} m/s")
    col2.metric("Actual Power", f"{latest_active:.2f} kW")
    col3.metric("Theoretical Power", f"{latest_theory:.2f} kW")
    
    status = "✅ Normal" if loss < 500 else "⚠️ Maintenance"
    col4.metric("System Status", status)

    st.subheader("📊 Performance Analysis")
    fig = px.scatter(df.head(1000), x=df.columns[1], y=[df.columns[2], df.columns[3]], title="Real-time Power Curve")
    st.plotly_chart(fig, use_container_width=True)
    
    st.dataframe(df.tail(5), use_container_width=True)

except Exception as e:
    st.error(f"خطأ في قراءة الأعمدة: {e}")
    st.info("تأكد أن ملف CSV مرتب كالتالي: التاريخ، السرعة، الباور الفعلي، الباور النظري.")
