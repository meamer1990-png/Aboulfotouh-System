import streamlit as st
import pandas as pd
from datetime import datetime

# الإعدادات الأساسية
BASE_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR4tUjdMv4rY_meyVWCwB7MYbSGMqBeMzQzXWvI1jNhna34oxOmpMwFPg-HGCmVO7gfLVbDQjCBCbEX/pub?output=csv"
GIDS = {
    "Users": "0",
    "Inventory": "1608796075",
    "Visits": "1113063548",
    "Orders": "56426419",
    "Merchants": "162635924"
}

st.set_page_config(page_title="Pourquoi System", layout="wide")

def fetch_data(gid):
    try:
        df = pd.read_csv(f"{BASE_URL}&gid={gid}")
        df.columns = df.columns.str.strip()
        return df.fillna("")
    except: return None

if 'auth' not in st.session_state:
    st.session_state.auth, st.session_state.role, st.session_state.user_details = False, None, None

# --- [1] واجهة الدخول ---
if not st.session_state.auth:
    st.title("🛡️ بوابة Pourquoi")
    login_id = st.text_input("الإيميل المعتمد:").strip().lower()
    if st.button("دخول النظام"):
        if login_id in ["mamer2063@gmail.com", "meamer1990@gmail.com", "admin"]:
            st.session_state.auth, st.session_state.role, st.session_state.user_details = True, "الكنترول", {"الاسم": "د. محمد عصام"}
            st.rerun()
        df_u = fetch_data(GIDS["Users"])
        if df_u is not None:
            user = df_u[df_u.iloc[:, 2].astype(str).str.strip().str.lower() == login_id]
            if not user.empty and str(user.iloc[0].get('Status', '')).lower() == 'approved':
                st.session_state.auth = True
                st.session_state.role = user.iloc[0].get('الغرض من الدخول', 'عميل')
                st.session_state.user_details = {"الاسم": user.iloc[0].iloc[1], "Email": login_id}
                st.rerun()
            else: st.error("الحساب غير مفعل")

# --- [2] واجهات النظام ---
else:
    role = st.session_state.role
    st.sidebar.title(f"👤 {st.session_state.user_details['اسم المتقدم' if role != 'الكنترول' else 'الاسم']}")
    st.sidebar.info(f"الرتبة: {role}")

    if role == "الكنترول":
        tab1, tab2, tab3, tab4 = st.tabs(["📊 الأداء", "👥 الحسابات", "📦 المخزن", "📩 الشكاوى"])
        with tab1:
            st.subheader("📈 تقييم الأداء العام")
            st.write("مقارنة مبيعات المنتجات (يومي/شهري)")
        with tab2:
            st.dataframe(fetch_data(GIDS["Users"]))
        with tab3:
            st.dataframe(fetch_data(GIDS["Inventory"]))

    elif role == "محاسب":
        st.header("🧾 واجهة المحاسبة")
        menu = st.sidebar.radio("المهام", ["إدارة المناديب", "خطوط السير", "التقارير"])
        if menu == "خطوط السير":
            st.subheader("🗓️ تعيين خط سير")
            st.selectbox("اختر المندوب", ["أحمد", "محمود"]) # سيتم جلبهم من شيت Users
            st.text_input("المدن المستهدفة")
            st.button("تثبيت خط السير")

    elif role == "مندوب":
        st.header("🚗 بوابة المندوب")
        task = st.sidebar.radio("القائمة", ["📍 الزيارات اليومية", "📝 تسجيل عميل", "🧾 فاتورة"])
        
        if task == "📍 الزيارات اليومية":
            st.subheader("تأكيد الوصول للعميل")
            # محاكاة تسجيل الموقع
            if st.button("📍 تسجيل وصول GPS"):
                st.success(f"تم تسجيل الوقت: {datetime.now().strftime('%Y-%m-%d %H:%M')} والموقع بنجاح.")
        
        elif task == "📝 تسجيل عميل":
            with st.form("c_form"):
                st.text_input("اسم المحل/التاجر")
                st.text_input("العنوان")
                st.button("📍 التقاط إحداثيات GPS")
                st.form_submit_button("حفظ وإرسال للكنترول")

        elif task == "🧾 فاتورة":
            df_p = fetch_data(GIDS["Inventory"])
            item = st.selectbox("المنتج", df_p.iloc[:, 0])
            qty = st.number_input("الكمية", 1)
            if st.button("إضافة"):
                st.success("تمت الإضافة للسلة")
            if st.button("📤 إرسال واتساب"):
                st.info("جاري تجهيز الفاتورة بصيغة صورة...")

    if st.sidebar.button("خروج"):
        st.session_state.auth = False
        st.rerun()
