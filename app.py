import streamlit as st
import pandas as pd

# الرابط الأساسي للشيت الخاص بك
BASE_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR4tUjdMv4rY_meyVWCwB7MYbSGMqBeMzQzXWvI1jNhna34oxOmpMwFPg-HGCmVO7gfLVbDQjCBCbEX/pub?output=csv"

st.set_page_config(page_title="Pourquoi - إدارة مؤسسة أبوالفتوح", layout="wide")

# دالة جلب البيانات مع التنظيف
def fetch_data(gid):
    try:
        url = f"{BASE_URL}&gid={gid}"
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip()
        return df
    except:
        return None

# إعداد حالة الجلسة (Session State)
if 'auth' not in st.session_state:
    st.session_state.auth = False
    st.session_state.role = None
    st.session_state.user_details = None

# --- [1] واجهة الدخول والتسجيل ---
if not st.session_state.auth:
    st.image("https://via.placeholder.com/150?text=Pourquoi", width=100) # ضع هنا لوجو Pourquoi لاحقاً
    st.title("🛡️ بوابة نظام Pourquoi التجارية")
    
    tab_login, tab_register = st.tabs(["🔐 تسجيل الدخول", "📝 طلب حساب جديد"])
    
    with tab_login:
        login_id = st.text_input("أدخل البريد الإلكتروني المعتمد:").strip().lower()
        if st.button("دخول النظام"):
            # 1. الدخول المباشر للكنترول (د. محمد)
            if login_id == "mamer2063@gmail.com":
                st.session_state.auth = True
                st.session_state.role = "الكنترول"
                st.session_state.user_details = {"الاسم": "د. محمد عصام"}
                st.rerun()
            
            # 2. التحقق من قاعدة بيانات المستخدمين (gid=894869869)
            df_users = fetch_data("894869869")
            if df_users is not None:
                # البحث عن المستخدم والتأكد من الموافقة
                user_row = df_users[(df_users.iloc[:, 2].astype(str).str.strip().str.lower() == login_id)]
                
                if not user_row.empty:
                    status = str(user_row.iloc[0]['Status']).strip().lower()
                    if status == "approved":
                        st.session_state.auth = True
                        st.session_state.role = user_row.iloc[0]['الغرض من الدخول'] # (عميل/مندوب/محاسب)
                        st.session_state.user_details = user_row.iloc[0].to_dict()
                        st.rerun()
                    else:
                        st.warning(f"⚠️ الحساب مسجل ولكن لم يتم تفعيله بعد. الحالة: {status}")
                else:
                    st.error("❌ هذا الإيميل غير مسجل. يرجى تقديم طلب حساب جديد.")

    with tab_register:
        st.subheader("📝 نموذج طلب انضمام للمؤسسة")
        with st.form("reg_form"):
            new_name = st.text_input("الاسم الكامل")
            new_address = st.text_input("العنوان بالتفصيل")
            new_role = st.selectbox("الغرض من الدخول", ["عميل", "مندوب", "محاسب"])
            new_phone = st.text_input("رقم التليفون")
            new_email = st.text_input("الإيميل (سيكون هو مفتاح دخولك)")
            submit = st.form_submit_button("إرسال طلب للكنترول")
            if submit:
                # هنا نوجه المستخدم لنموذج Google Form لضمان وصول البيانات للشيت
                st.success("يرجى إتمام التسجيل عبر نموذج جوجل الرسمي ليظهر لدى الكنترول.")
                st.markdown(f"[اضغط هنا لفتح نموذج التسجيل](https://docs.google.com/forms/d/e/1FAIpQLSf3xBxqE0rDxeKJ8YuNZpdYckp8FKPt0eBiq1Sgevnp8ts9FQ/viewform)")

# --- [2] واجهة البرنامج المخصصة حسب الرتبة ---
else:
    role = st.session_state.role
    user_name = st.session_state.user_details['الاسم']
    
    st.sidebar.title(f"مرحباً بك: {user_name}")
    st.sidebar.info(f"رتبتك: {role}")

    # تفريع الواجهات بناءً على طلبك
    if role == "الكنترول":
        import control_module # سنقوم ببنائه
        st.title("🎛️ لوحة تحكم الإدارة العليا")
        st.write("مرحباً دكتور محمد، لديك السيطرة الكاملة على النظام.")

    elif role == "محاسب":
        st.title("🧾 واجهة الإدارة المالية والمحاسبية")
        st.write("إدارة المناديب، خطوط السير، والتقارير.")

    elif role == "مندوب":
        st.title("🚗 بوابة المندوب الميدانية")
        st.write("خطوط السير، تسجيل الزيارات، وإصدار الفواتير.")

    elif role == "عميل":
        st.title("🤝 بوابة عملاء Pourquoi")
        st.write("مواعيد الزيارة، طلب أوردر، والشكاوى.")

    if st.sidebar.button("تسجيل الخروج"):
        st.session_state.auth = False
        st.rerun()
