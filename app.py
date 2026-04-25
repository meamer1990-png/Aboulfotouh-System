import streamlit as st
import pandas as pd

st.set_page_config(page_title="مجموعة أبو الفتوح للتجارة", layout="wide")

# الرابط المباشر
sheet_id = "1Ey5M-J_O50wvYty00cgZvsyKq_LLcQBmMwKWf_Nl_rk"
URL = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet=Users"

if 'auth' not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.title("🔐 دخول نظام أبو الفتوح")
    user_input = st.text_input("اسم المستخدم (جرب admin)")
    pass_input = st.text_input("كلمة المرور (جرب 123)", type="password")
    
    if st.button("تسجيل الدخول"):
        try:
            df = pd.read_csv(URL)
            # تحويل كل شيء لحروف صغيرة ومسح المسافات لضمان الدخول
            df['الاسم'] = df['الاسم'].astype(str).str.strip().str.lower()
            df['كلمة_المرور'] = df['كلمة_المرور'].astype(str).str.strip().str.lower()
            
            u_in = user_input.strip().lower()
            p_in = pass_input.strip().lower()
            
            match = df[(df['الاسم'] == u_in) & (df['كلمة_المرور'] == p_in)]
            
            if not match.empty:
                st.session_state.auth = True
                st.session_state.user_role = match.iloc[0]['الصلاحية']
                st.session_state.user_full_name = user_input
                st.rerun()
            else:
                st.error("بيانات الدخول غير مطابقة لما في الجدول")
        except:
            st.error("فشل في قراءة الشيت.. تأكد من اتصال الإنترنت")
else:
    st.success(f"مرحباً بك يا دكتور في لوحة التحكم")
    st.balloons() # احتفالاً بالدخول
