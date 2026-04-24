import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# إعداد الصفحة وتصميمها
st.set_page_config(page_title="مجموعة أبو الفتوح للتجارة", layout="wide")

# رابط الشيت الخاص بك
URL = "https://docs.google.com/spreadsheets/d/1Ey5M-J_O50wvYty00cgZvsyKq_LLcQBmMwKWf_Nl_rk/edit?usp=sharing"

# الاتصال بالقاعدة
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except:
    st.error("خطأ في الاتصال.. تأكد من إعدادات الربط")

if 'auth' not in st.session_state:
    st.session_state.auth = False

# واجهة تسجيل الدخول
if not st.session_state.auth:
    st.title("🔐 دخول نظام أبو الفتوح")
    user_input = st.text_input("اسم المستخدم")
    pass_input = st.text_input("كلمة المرور", type="password")
    
    if st.button("تسجيل الدخول"):
        try:
            # قراءة صفحة Users
            df = conn.read(spreadsheet=URL, worksheet="Users")
            # تنظيف أسماء الأعمدة من أي مسافات زائدة
            df.columns = df.columns.str.strip()
            
            # البحث عن المستخدم (الاسم وكلمة_المرور)
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
            st.warning("تأكد من وجود صفحة باسم 'Users' وأعمدة: الاسم، كلمة_المرور، الصلاحية")
else:
    # واجهة التحكم الرئيسية
    role = st.session_state.user_role
    st.sidebar.success(f"مرحباً: {st.session_state.user_full_name}")
    if st.sidebar.button("خروج"):
        st.session_state.auth = False
        st.rerun()
    
    st.header(f"لوحة تحكم: {role}")
    
    # توزيع المهام حسب الصلاحية
    if role == "Control":
        st.subheader("📊 إحصائيات الإدارة العامة")
        # هنا ستظهر جداول العملاء والطلبات لاحقاً
    elif role == "Sales":
        st.subheader("📑 تسجيل طلبات المندوب")
