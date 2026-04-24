import streamlit as st
import pandas as pd

# إعداد الصفحة
st.set_page_config(page_title="مجموعة أبو الفتوح للتجارة", layout="wide")

# الرابط المباشر (بعد ما جعلته عاماً في الصورة الأخيرة)
sheet_id = "1Ey5M-J_O50wvYty00cgZvsyKq_LLcQBmMwKWf_Nl_rk"
URL = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet=Users"

if 'auth' not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.title("🔐 دخول نظام أبو الفتوح")
    user_input = st.text_input("اسم المستخدم")
    pass_input = st.text_input("كلمة المرور", type="password")
    
    if st.button("تسجيل الدخول"):
        try:
            # قراءة مباشرة كملف CSV
            df = pd.read_csv(URL)
            df.columns = df.columns.str.strip()
            
            # مطابقة البيانات
            match = df[(df['الاسم'].astype(str).str.strip() == user_input.strip()) & 
                       (df['كلمة_المرور'].astype(str).str.strip() == pass_input.strip())]
            
            if not match.empty:
                st.session_state.auth = True
                st.session_state.user_role = match.iloc[0]['الصلاحية']
                st.session_state.user_full_name = user_input
                st.rerun()
            else:
                st.error("بيانات الدخول غير صحيحة")
        except Exception as e:
            st.error("تأكد من وجود صفحة باسم 'Users' وأعمدة: الاسم، كلمة_المرور")
else:
    st.header(f"مرحباً بك في لوحة تحكم أبو الفتوح: {st.session_state.user_role}")
