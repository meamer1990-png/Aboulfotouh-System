import streamlit as st
import pandas as pd

# الرابط الأساسي
BASE_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR4tUjdMv4rY_meyVWCwB7MYbSGMqBeMzQzXWvI1jNhna34oxOmpMwFPg-HGCmVO7gfLVbDQjCBCbEX/pub?output=csv"

st.set_page_config(page_title="Pourquoi System", layout="wide")

def fetch_data(gid):
    try:
        url = f"{BASE_URL}&gid={gid}"
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip()
        return df
    except:
        return None

if 'auth' not in st.session_state:
    st.session_state.auth = False
    st.session_state.role = None
    st.session_state.user_details = None

# --- الواجهة الرئيسية (دخول / تسجيل) ---
if not st.session_state.auth:
    st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>Pourquoi المؤسسة التجارية</h1>", unsafe_allow_html=True)
    
    # اختيار العملية: دخول أو تسجيل جديد
    choice = st.radio("اختر الإجراء:", ["🔑 تسجيل الدخول", "📝 طلب حساب جديد (لأول مرة)"], horizontal=True)

    if choice == "🔑 تسجيل الدخول":
        login_id = st.text_input("البريد الإلكتروني المعتمد:").strip().lower()
        if st.button("دخول النظام", use_container_width=True):
            if login_id in ["mamer2063@gmail.com", "meamer1990@gmail.com"]:
                st.session_state.auth = True
                st.session_state.role = "الكنترول"
                st.session_state.user_details = {"الاسم": "د. محمد عصام"}
                st.rerun()
            
            df_users = fetch_data("0")
            if df_users is not None:
                user_row = df_users[df_users.iloc[:, 2].astype(str).str.strip().str.lower() == login_id]
                if not user_row.empty:
                    status = str(user_row.iloc[0].get('Status', '')).strip().lower()
                    if status == "approved":
                        st.session_state.auth = True
                        st.session_state.role = user_row.iloc[0].get('الغرض من الدخول', 'عميل')
                        st.session_state.user_details = {"الاسم": user_row.iloc[0].iloc[1]}
                        st.rerun()
                    else:
                        st.warning("⚠️ حسابك بانتظار موافقة الكنترول.")
                else:
                    st.error("❌ هذا البريد غير مسجل.")

    elif choice == "📝 طلب حساب جديد (لأول مرة)":
        st.subheader("تعبئة بيانات طلب الانضمام")
        with st.form("registration_form"):
            reg_name = st.text_input("الاسم الكامل")
            reg_phone = st.text_input("رقم التليفون")
            reg_email = st.text_input("البريد الإلكتروني (المستخدم للدخول لاحقاً)")
            reg_address = st.text_input("العنوان")
            reg_role = st.selectbox("نوع الحساب المطلوب", ["عميل", "مندوب", "محاسب"])
            
            submit_btn = st.form_submit_button("إرسال طلب الانضمام")
            if submit_btn:
                if reg_name and reg_email:
                    # توجيه المستخدم لنموذج جوجل لضمان وصول البيانات للشيت
                    st.success("تم تجهيز طلبك! فضلاً اضغط على الرابط التالي لإتمام الإرسال:")
                    st.markdown(f"[اضغط هنا لإتمام إرسال بياناتك للكنترول](https://docs.google.com/forms/d/e/1FAIpQLSf3xBxqE0rDxeKJ8YuNZpdYckp8FKPt0eBiq1Sgevnp8ts9FQ/viewform)")
                else:
                    st.error("يرجى ملء البيانات الأساسية.")

# --- الواجهات الداخلية بعد الدخول ---
else:
    role = st.session_state.role
    st.sidebar.markdown(f"### 👤 {st.session_state.user_details['الاسم']}")
    st.sidebar.info(f"الرتبة: {role}")
    
    if role == "الكنترول":
        st.header("🎛️ لوحة تحكم الإدارة")
        # الأقسام كما في صورتك 1000405775
        menu = st.sidebar.selectbox("القائمة الإدارية", ["المستخدمين", "المخزن", "الطلبات"])
        if menu == "المستخدمين":
            df_u = fetch_data("0")
            st.dataframe(df_u)
            
    elif role == "مندوب":
        st.title("🚗 واجهة المندوب")
        # سنضيف هنا زر الـ GPS والفواتير في الخطوة التالية

    if st.sidebar.button("خروج"):
        st.session_state.auth = False
        st.rerun()
