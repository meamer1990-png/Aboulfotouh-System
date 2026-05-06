import streamlit as st
import pandas as pd

# الرابط الأساسي لجداول البيانات
BASE_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR4tUjdMv4rY_meyVWCwB7MYbSGMqBeMzQzXWvI1jNhna34oxOmpMwFPg-HGCmVO7gfLVbDQjCBCbEX/pub?output=csv"

st.set_page_config(page_title="Pourquoi System", layout="wide")

# دالة جلب البيانات
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

# --- [1] واجهة تسجيل الدخول ---
if not st.session_state.auth:
    st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>Pourquoi المؤسسة التجارية</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>نظام إدارة أبوالفتوح</h3>", unsafe_allow_html=True)
    
    login_id = st.text_input("البريد الإلكتروني المعتمد:").strip().lower()
    
    if st.button("دخول النظام", use_container_width=True):
        # تفعيل إيميلاتك ككنترول (الإيميلين لضمان الدخول)
        if login_id in ["mamer2063@gmail.com", "meamer1990@gmail.com", "admin"]:
            st.session_state.auth = True
            st.session_state.role = "الكنترول"
            st.session_state.user_details = {"الاسم": "د. محمد عصام"}
            st.rerun()
        
        # التحقق من بقية المستخدمين من شيت Users (gid=0)
        df_users = fetch_data("0")
        if df_users is not None:
            # البحث عن الإيميل في العمود المخصص (تأكد من اسم العمود في الشيت)
            user_row = df_users[df_users.iloc[:, 2].astype(str).str.strip().str.lower() == login_id]
            if not user_row.empty:
                status = str(user_row.iloc[0].get('Status', '')).strip().lower()
                if status == "approved":
                    st.session_state.auth = True
                    st.session_state.role = user_row.iloc[0].get('الغرض من الدخول', 'عميل')
                    st.session_state.user_details = {"الاسم": user_row.iloc[0].iloc[1]}
                    st.rerun()
                else:
                    st.warning("⚠️ بانتظار تفعيل الحساب من الإدارة.")
            else:
                st.error("❌ البريد غير مسجل.")

# --- [2] واجهات النظام بعد الدخول ---
else:
    role = st.session_state.role
    st.sidebar.markdown(f"### 👤 {st.session_state.user_details['الاسم']}")
    st.sidebar.markdown(f"**الرتبة: {role}**")
    st.sidebar.divider()

    # --- واجهة الكنترول ---
    if role == "الكنترول":
        menu = st.sidebar.radio("لوحة التحكم", ["👥 إدارة الحسابات", "📦 جرد المخزن", "📊 تقارير الأداء", "📩 الشكاوى"])
        
        if menu == "👥 إدارة الحسابات":
            st.header("👥 تفعيل وتعليق الحسابات")
            df_u = fetch_data("0")
            if df_u is not None:
                st.dataframe(df_u[['الاسم الكامل', 'الغرض من الدخول', 'رقم التليفون', 'Status']])
                st.info("💡 للتفعيل: اذهب للشيت واكتب 'approved' في عمود Status.")
        
        elif menu == "📦 جرد المخزن":
            st.header("📦 حالة الأصناف")
            df_inv = fetch_data("1608796075")
            st.dataframe(df_inv)

    # --- واجهة المندوب ---
    elif role == "مندوب":
        menu = st.sidebar.radio("قائمة المندوب", ["🚗 خط السير", "📝 تسجيل عميل جديد", "🧾 إصدار فاتورة"])
        if menu == "🚗 خط السير":
            st.title("🚗 مهامي اليومية")
            st.info("سيتم عرض المدن المحددة لك من قبل المحاسب.")

    # --- واجهة العميل ---
    elif role == "عميل":
        st.title("🛍️ طلب أوردر جديد")
        st.write("بيانات المندوب الخاص بك ومواعيد الزيارة.")

    if st.sidebar.button("تسجيل الخروج"):
        st.session_state.auth = False
        st.rerun()
