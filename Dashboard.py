import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Wind Turbine Monitoring", layout="wide")
st.title("🔌 Wind Turbine Real-Time Monitoring System")

try:
    # الحل النهائي: فصلنا الفواصل بشكل يدوي وتخطينا أي غلطات
    df = pd.read_csv("T1.csv", 
                     sep=None,          # يكتشف الفاصلة لوحدة (coma او semicolon)
                     engine='python',   # المحرك الأكثر مرونة
                     on_bad_lines='skip', 
                     encoding='latin-1',
                     quotechar='"')     # عشان يحل مشكلة علامات التنصيص اللي ظاهرة لك

    # حساب الفقد (Loss)
    df['Loss'] = df['Theoretical_Power_Curve (KWh)'] - df['LV ActivePower (kW)']
    latest_data = df.iloc[-1] 

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Wind Speed", f"{latest_data['Wind Speed (m/s)']:.2f} m/s")
    col2.metric("Actual Power", f"{latest_data['LV ActivePower (kW)']:.2f} kW")
    col3.metric("Theoretical Power", f"{latest_data['Theoretical_Power_Curve (KWh)']:.2f} kW")
    
    status = "✅ Normal Operation" if latest_data['Loss'] < 500 else "⚠️ Maintenance Required"
    col4.metric("System Status", status)

    st.subheader("📊 Performance Analysis")
    # عرض أول 500 نقطة بس عشان الصفحة متهنجش
    fig = px.scatter(df.head(500), x='Wind Speed (m/s)', y=['LV ActivePower (kW)', 'Theoretical_Power_Curve (KWh)'])
    st.plotly_chart(fig, use_container_width=True)
    
    st.dataframe(df.tail(10), use_container_width=True)

except Exception as e:
    st.error(f"خطأ في قراءة البيانات: {e}")
    st.info("نصيحة: تأكد أن ملف T1.csv لا يحتوي على علامات تنصيص زائدة في السطور الأولى.")
