import streamlit as st
import pandas as pd

st.set_page_config(page_title="مجموعة أبو الفتوح للتجارة", layout="wide")

# الرابط المباشر الصحيح الذي لا يحتاج صلاحيات معقدة
sheet_id = "1Ey5M-J_O50wvYty00cgZvsyKq_LLcQBmMwKWf_Nl_rk"
# لاحظ كلمة export?format=csv هي السر هنا
URL = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=1114501625"

if 'auth' not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.title("🔐 دخول نظام أبو الفتوح")
    user_input = st.text_input("اسم المستخدم")
    pass_input = st.text_input("كلمة المرور", type="password")
    
    if st.button("تسجيل الدخول"):
        try:
            # قراءة مباشرة وسهلة
            df = pd.read_csv(URL)
            df.columns = df.columns.str.strip()
            
            u_in = str(user_input).strip().lower()
            p_in = str(pass_input).strip().lower()
            
            # البحث في الشيت (أصلحنا الكود ليناسب admain و Mohamed Essam)
            match = df[(df['الاسم'].astype(str).str.strip().str.lower() == u_in) & 
                       (df['كلمة_المرور'].astype(str).str.strip().str.lower() == p_in)]
            
            if not match.empty:
                st.session_state.auth = True
                st.session_state.user_role = match.iloc[0]['الصلاحية']
                st.session_state.user_full_name = user_input
                st.rerun()
            else:
                st.error("الاسم أو كلمة المرور غير مطابقة للجدول")
        except Exception as e:
            st.error("عذراً.. تأكد من نشر الشيت (Share -> Anyone with the link)")
else:
    st.success(f"أهلاً بك دكتور محمد في نظامك الخاص")
    st.balloons()
