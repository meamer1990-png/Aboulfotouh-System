import streamlit as st
import pandas as pd
from datetime import datetime

# الروابط و الـ GIDs الخاصة بملفاتك
BASE_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR4tUjdMv4rY_meyVWCwB7MYbSGMqBeMzQzXWvI1jNhna34oxOmpMwFPg-HGCmVO7gfLVbDQjCBCbEX/pub?output=csv"
GIDS = {
    "Users": "0",
    "Inventory": "1608796075",
    "Visits": "1113063548",
    "Orders": "56426419",
    "Merchants": "162635924"
}

st.set_page_config(page_title="Pourquoi - إدارة مؤسسة أبوالفتوح", layout="wide")

def fetch_data(gid):
    try:
        df = pd.read_csv(f"{BASE_URL}&gid={gid}")
        df.columns = df.columns.str.strip()
        return df.fillna("")
    except: return None

if 'auth' not in st.session_state:
    st.session_state.auth = False
    st.session_state.role = None
    st.session_state.user_details = None

# --- [1] واجهة الدخول والتسجيل ---
if not st.session_state.auth:
    st.title("🛡️ بوابة نظام Pourquoi")
    choice = st.radio("اختر الإجراء:", ["🔑 دخول", "📝 تسجيل جديد"], horizontal=True)

    if choice == "🔑 دخول":
        login_id = st.text_input("الإيميل:").strip().lower()
        if st.button("دخول النظام"):
            # دخول الكنترول المباشر
            if login_id in ["mamer2063@gmail.com", "meamer1990@gmail.com", "admin"]:
                st.session_state.auth = True
                st.session_state.role = "الكنترول"
                st.session_state.user_details = {"الاسم": "د. محمد عصام"}
                st.rerun()
            
            df_u = fetch_data(GIDS["Users"])
            if df_u is not None:
                user = df_u[df_u.iloc[:, 2].astype(str).str.strip().str.lower() == login_id]
                if not user.empty and str(user.iloc[0].get('Status', '')).lower() == 'approved':
                    st.session_state.auth = True
                    st.session_state.role = user.iloc[0].get('الغرض من الدخول', 'عميل')
                    st.session_state.user_details = {"الاسم": user.iloc[0].iloc[1]}
                    st.rerun()
                else: st.error("الحساب غير مفعل أو غير موجود")

    else:
        st.subheader("📝 طلب انضمام جديد")
        st.info("سيتم تحويلك لنموذج التسجيل لإرسال بياناتك للإدارة.")
        st.markdown(f"[اضغط هنا لفتح نموذج التسجيل](https://docs.google.com/forms/d/e/1FAIpQLSf3xBxqE0rDxeKJ8YuNZpdYckp8FKPt0eBiq1Sgevnp8ts9FQ/viewform)")

# --- [2] واجهات النظام الداخلية ---
else:
    role = st.session_state.role
    st.sidebar.title(f"👤 {st.session_state.user_details['الاسم']}")
    st.sidebar.write(f"الرتبة: {role}")

    if role == "الكنترول":
        st.header("🎛️ لوحة تحكم الإدارة")
        tab1, tab2, tab3 = st.tabs(["👥 الحسابات", "📦 المخزن", "📩 الشكاوى"])
        with tab1:
            st.dataframe(fetch_data(GIDS["Users"]))
        with tab2:
            st.dataframe(fetch_data(GIDS["Inventory"]))
        with tab3:
            st.write("صندوق الشكاوى السري")

    elif role == "مندوب":
        st.header("🚗 واجهة المندوب")
        if st.button("📍 تسجيل وصول GPS"):
            st.success("تم تأكيد الموقع والوقت بنجاح")
        st.subheader("🧾 إصدار فاتورة")
        # كود الفاتورة سيوضع هنا بالتفصيل

    elif role == "عميل":
        st.header("🤝 بوابة العميل")
        st.info("موعد زيارتك القادمة: متاح في جدول الزيارات")
        st.button("🛒 طلب أوردر جديد")

    if st.sidebar.button("تسجيل الخروج"):
        st.session_state.auth = False
        st.rerun()
