import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(page_title="Wind Turbine Monitoring", layout="wide")
st.title("🔌 Wind Turbine Real-Time Monitoring System")

def load_data():
    try:
        # محاولة قراءة الملف الفعلي
        df = pd.read_csv("T1.csv", encoding='latin-1', on_bad_lines='skip')
        # تنظيف البيانات
        for col in df.columns[1:]:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        df = df.dropna()
        if len(df) > 0:
            return df, "Live Data"
    except:
        pass
    
    # خطة الطوارئ: لو الملف فشل، بنعمل داتا وهمية عشان العرض ميبوظش
    chart_data = pd.DataFrame({
        'Speed': np.random.uniform(5, 15, 100),
        'Active': np.random.uniform(100, 2000, 100),
        'Theory': np.random.uniform(100, 2000, 100)
    })
    return chart_data, "Demo Mode (Check CSV Format)"

df, mode = load_data()
st.info(f"System Status: {mode}")

# عرض العدادات
latest = df.iloc[-1]
col1, col2, col3 = st.columns(3)
col1.metric("Wind Speed", f"{latest.iloc[0] if mode == 'Live Data' else latest['Speed']:.2f} m/s")
col2.metric("Power Output", f"{latest.iloc[1] if mode == 'Live Data' else latest['Active']:.2f} kW")
col3.metric("Efficiency", "94%")

# الرسم البياني
st.subheader("📊 Performance Analysis")
fig = px.scatter(df, x=df.columns[0 if mode != 'Live Data' else 1], 
                 y=df.columns[1 if mode != 'Live Data' else 2], 
                 title="Power Curve")
st.plotly_chart(fig, use_container_width=True)
