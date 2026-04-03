import streamlit as st
import pandas as pd
import plotly.express as px

# 1. إعدادات الصفحة
st.set_page_config(page_title="Wind Turbine Monitoring", layout="wide")

st.title("🔌 Wind Turbine Real-Time Monitoring System")
st.markdown("---")

# 2. تحميل البيانات - تأكد من مسار الملف عندك
try:
    # أنا عدلت المسار ليكون الملف اللي إنت شغال عليه
    path = r"T1.csv"
    df = pd.read_csv(path)

    # حساب الـ Loss لو مش موجود
    df['Loss'] = df['Theoretical_Power_Curve (KWh)'] - df['LV ActivePower (kW)']

    # 3. العدادات العلوية (Metrics)
    # هناخد آخر سطر في الداتا كأنه القراءة الحالية
    latest_data = df.iloc[-1]

    col1, col2, col3, col4 = st.columns(4)

    # تعديل الأسماء لتطابق صورة الإكسيل بالظبط
    col1.metric("Wind Speed", f"{latest_data['Wind Speed (m/s)']:.2f} m/s")
    col2.metric("Actual Power", f"{latest_data['LV ActivePower (kW)']:.2f} kW")
    col3.metric("Theoretical Power", f"{latest_data['Theoretical_Power_Curve (KWh)']:.2f} kW")

    # تحديد الحالة بناءً على الـ Loss
    if latest_data['Loss'] > 500:
        status = "⚠️ Maintenance Required"
        color = "normal"  # بيظهر بلون تنبيه في ستريمليت
    else:
        status = "✅ Normal Operation"
        color = "inverse"

    col4.metric("System Status", status)

    # 4. الرسوم البيانية التفاعلية
    st.subheader("📊 Performance Analysis")
    c1, c2 = st.columns(2)

    with c1:
        st.write("**Power Curve: Actual vs Theoretical**")
        # رسم علاقة سرعة الرياح بالباور (نقط زرقاء وحمراء)
        fig = px.scatter(df.head(2000),
                         x='Wind Speed (m/s)',
                         y=['LV ActivePower (kW)', 'Theoretical_Power_Curve (KWh)'],
                         labels={'value': 'Power (kW)', 'variable': 'Type'},
                         color_discrete_sequence=['#1f77b4', '#ff7f0e'])
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.write("**Energy Loss Trend**")
        # رسم خط بيبين فقد الطاقة (Loss)
        fig2 = px.line(df.head(2000),
                       y='Loss',
                       title="Power Loss (kW)",
                       color_discrete_sequence=['#d62728'])
        st.plotly_chart(fig2, use_container_width=True)

    # 5. عرض جدول البيانات
    st.subheader("📋 Recent Data Logs")
    st.dataframe(df.tail(100), use_container_width=True)

except Exception as e:
    st.error(f"خطأ في قراءة البيانات: {e}")
    st.info("تأكد أن ملف T1.csv موجود في المسار الصحيح وأن أسماء الأعمدة مطابقة.")
