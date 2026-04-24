import streamlit as st
import pandas as pd

# إعداد الصفحة
st.set_page_config(page_title="مجموعة أبو الفتوح للتجارة", layout="wide")

# الرابط السحري (تحويل الشيت لرابط مباشر CSV)
sheet_id = "1Ey5M-J_O50wvYty00cgZvsyKq_LLcQBmMwKWf_Nl_rk"
sheet_name = "Users"
URL = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"

if 'auth' not in st.session_state:
    st.session_state.auth = False

# واجهة تسجيل الدخول
if not st.session_state.auth:
    st.title("🔐 دخول نظام أبو الفتوح")
    user_input = st.text_input("اسم المستخدم")
    pass_input = st.text_input("كلمة المرور", type="password")
    
    if st.button("تسجيل الدخول"):
        try:
            # قراءة البيانات مباشرة بدون وسيط
            df = pd.read_csv(URL)
            df.columns = df.columns.str.strip() # تنظيف الأسماء
            
            # البحث عن المستخدم
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
            st.error(f"حدث خطأ في قراءة البيانات. تأكد أن الشيت متاح 'Anyone with the link'")
else:
    # لوحة التحكم
    st.sidebar.success(f"مرحباً د. {st.session_state.user_full_name}")
    if st.sidebar.button("خروج"):
        st.session_state.auth = False
        st.rerun()
    
    st.header(f"لوحة تحكم: {st.session_state.user_role}")
    st.info("تم الاتصال بنجاح بقاعدة بيانات مجموعة أبو الفتوح")
