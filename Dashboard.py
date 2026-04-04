import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Wind Turbine Monitoring", layout="wide")
st.title("🔌 Wind Turbine Real-Time Monitoring System")

try:
    # 1. قراءة الملف بمرونة تامة (detect separator)
    df = pd.read_csv("T1.csv", sep=None, engine='python', encoding='latin-1', on_bad_lines='skip')
    
    # 2. تنظيف البيانات من أي نصوص أو قيم فاضية
    df = df.apply(pd.to_numeric, errors='coerce').dropna()

    if len(df.columns) < 2:
        st.error("الملف مقروء كعمود واحد فقط. تأكد أن البيانات مفصولة بفاصلة (,) وليس مسافات.")
    else:
        # 3. اختيار الأعمدة بناءً على "المحتوى" مش الاسم ولا الرقم الثابت
        # بنفترض إن سرعة الرياح هي اللي قيمها صغيرة (أول عمود فيه أرقام غالباً)
        # والباور هو القيم الكبيرة
        
        latest_data = df.iloc[-1]
        
        # عرض البيانات بشكل ديناميكي
        cols = st.columns(len(df.columns))
        for i, col_name in enumerate(df.columns):
            cols[i % 4].metric(f"Field {i+1}", f"{latest_data[col_name]:.2f}")

        st.subheader("📊 Live Data Overview")
        st.line_chart(df.iloc[:, 1:4].head(100)) # رسم أول 3 أعمدة بيانات
        
        st.success("تم قراءة البيانات بنجاح!")
        st.dataframe(df.tail(5))

except Exception as e:
    st.error(f"خطأ: {e}")
