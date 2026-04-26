import streamlit as st
import pandas as pd

st.set_page_config(page_title="مجموعة أبو الفتوح التجارية", layout="wide")

# هذا الرابط هو "المفتاح السحري" لفتح الشيت دون الحاجة لـ Publish
sheet_id = "1Ey5M-J_O50wvYty00cgZvsyKq_LLcQBmMwKWf_Nl_rk"
URL = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=1114501625"

if 'auth' not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.title("🔐 نظام مجموعة أبو الفتوح")
    user_input = st.text_input("اسم المستخدم")
    pass_input = st.text_input("كلمة المرور", type="password")
    
    if st.button("تسجيل الدخول"):
        try:
            # قراءة البيانات مباشرة
            df = pd.read_csv(URL)
            df.columns = df.columns.str.strip()
            
            u_in = str(user_input).strip().lower()
            p_in = str(pass_input).strip().lower()
            
            # مطابقة الاسم والباسورد
            match = df[(df['الاسم'].astype(str).str.strip().str.lower() == u_in) & 
                       (df['كلمة_المرور'].astype(str).str.strip().str.lower() == p_in)]
            
            if not match.empty:
                st.session_state.auth = True
                st.session_state.user_role = match.iloc[0]['الصلاحية']
                st.session_state.user_full_name = user_input
                st.rerun()
            else:
                st.error("بيانات الدخول غير صحيحة")
        except:
            st.error("تأكد من كتابة الاسم والباسورد بشكل صحيح كما في الشيت")

else:
    st.success(f"مرحباً بك دكتور محمد في نظامك الخاص")
    st.balloons()
