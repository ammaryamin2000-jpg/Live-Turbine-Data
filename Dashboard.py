import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Wind Turbine Monitoring", layout="wide")
st.title("🔌 Wind Turbine Real-Time Monitoring System")

try:
    # 1. القراءة بمرونة تامة (تحديد الفاصلة تلقائياً وتخطي الأخطاء)
    df = pd.read_csv("T1.csv", sep=None, engine='python', encoding='latin-1', on_bad_lines='skip')
    
    # 2. تنظيف البيانات وتحويلها لأرقام
    df = df.apply(pd.to_numeric, errors='coerce').dropna()

    if df.empty or len(df.columns) < 2:
        st.error("⚠️ الملف لا يحتوي على بيانات كافية أو لم يتم التعرف على الأعمدة بشكل صحيح.")
    else:
        # 3. جلب آخر قراءة بناءً على ترتيب الأعمدة
        latest_data = df.iloc[-1]
        
        # توزيع المؤشرات (Metrics)
        cols = st.columns(4)
        # نفترض الترتيب: التاريخ (0)، السرعة (1)، الباور الفعلي (2)، الباور النظري (3)
        cols[0].metric("Wind Speed", f"{latest_data.iloc[1]:.2f} m/s")
        cols[1].metric("Actual Power", f"{latest_data.iloc[2]:.2f} kW")
        cols[2].metric("Theoretical", f"{latest_data.iloc[3]:.2f} kW")
        
        loss = latest_data.iloc[3] - latest_data.iloc[2]
        status = "✅ Normal" if loss < 500 else "⚠️ Check System"
        cols[3].metric("Status", status)

        # 4. الرسم البياني (أول 500 نقطة للسرعة)
        st.subheader("📊 Performance Graph")
        fig = px.line(df.head(500), y=df.columns[2], title="Power Output Over Time")
        st.plotly_chart(fig, use_container_width=True)

        st.success("✅ Data loaded successfully!")
        st.dataframe(df.tail(5))

except Exception as e:
    st.error(f"❌ خطأ غير متوقع: {e}")
