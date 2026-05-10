import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_geolocation import streamlit_geolocation

# الروابط و الـ GIDs الخاصة ببيانات مؤسسة Pourquoi
BASE_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR4tUjdMv4rY_meyVWCwB7MYbSGMqBeMzQzXWvI1jNhna34oxOmpMwFPg-HGCmVO7gfLVbDQjCBCbEX/pub?output=csv"
GIDS = {
    "Users": "0",
    "Inventory": "1608796075",
    "Visits": "1113063548",
    "Orders": "56426419",
    "Merchants": "162635924"
}

st.set_page_config(page_title="Pourquoi System - GPS Enabled", layout="wide")

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
    st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>Pourquoi المؤسسة التجارية</h1>", unsafe_allow_html=True)
    login_id = st.text_input("البريد الإلكتروني المعتمد:").strip().lower()
    
    if st.button("دخول النظام", use_container_width=True):
        if login_id in ["mamer2063@gmail.com", "meamer1990@gmail.com", "admin"]:
            st.session_state.auth, st.session_state.role, st.session_state.user_details = True, "الكنترول", {"الاسم": "د. محمد عصام"}
            st.rerun()
        
        df_u = fetch_data(GIDS["Users"])
        if df_u is not None:
            user = df_u[df_u.iloc[:, 2].astype(str).str.strip().str.lower() == login_id]
            if not user.empty and str(user.iloc[0].get('Status', '')).lower() == 'approved':
                st.session_state.auth = True
                st.session_state.role = user.iloc[0].get('الغرض من الدخول', 'عميل')
                st.session_state.user_details = {"الاسم": user.iloc[0].iloc[1]}
                st.rerun()
            else: st.error("❌ الحساب غير مفعل أو البريد خطأ.")

# --- [2] واجهات النظام الداخلية ---
else:
    role = st.session_state.role
    st.sidebar.title(f"👤 {st.session_state.user_details['الاسم']}")
    st.sidebar.info(f"الرتبة: {role}")

    # واجهة الكنترول
    if role == "الكنترول":
        tab1, tab2, tab3 = st.tabs(["👥 الحسابات", "📦 المخزن", "📩 الشكاوى"])
        with tab1:
            st.dataframe(fetch_data(GIDS["Users"]))
        with tab2:
            st.dataframe(fetch_data(GIDS["Inventory"]))

    # واجهة المندوب (المهمة جداً للـ GPS)
    elif role == "مندوب":
        st.header("🚗 بوابة المندوب الميدانية")
        task = st.sidebar.radio("القائمة الميدانية", ["📍 تسجيل زيارة (GPS)", "🧾 فاتورة بيع", "📝 تسجيل عميل جديد"])
        
        if task == "📍 تسجيل زيارة (GPS)":
            st.subheader("تأكيد التواجد عند العميل")
            st.write("فضلاً اضغط على أيقونة الموقع بالأسفل لجلب الإحداثيات:")
            
            # استدعاء أداة الـ GPS
            location = streamlit_geolocation()
            
            if location.get('latitude'):
                st.success("✅ تم التقاط الموقع بنجاح!")
                st.write(f"📍 إحداثياتك الحالية: {location['latitude']}, {location['longitude']}")
                
                # ربط الموقع بالعميل
                df_merchants = fetch_data(GIDS["Merchants"])
                client = st.selectbox("اختر العميل الذي تزوره الآن", df_merchants.iloc[:, 1])
                
                if st.button("💾 حفظ الزيارة في السجل الميداني"):
                    st.info(f"جاري حفظ الزيارة للعميل {client} مع توثيق الموقع والوقت...")
                    # هنا يتم الربط مع شيت Visits لاحقاً
            else:
                st.warning("⚠️ في انتظار السماح بالوصول للموقع... يرجى الضغط على زر الموقع أعلاه.")

    elif role == "عميل":
        st.header("🛍️ طلب أوردر جديد")
        st.write("مرحباً بك في متجر Pourquoi")

    if st.sidebar.button("تسجيل الخروج"):
        st.session_state.auth = False
        st.rerun()
