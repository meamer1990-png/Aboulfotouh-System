import streamlit as st
import pandas as pd

st.set_page_config(page_title="مجموعة أبو الفتوح التجارية", layout="wide")

# روابط الشيت (ردود الفورم)
SHEET_ID = "1Ey5M-J_O50wvYty00cgZvsyKq_LLcQBmMwKWf_Nl_rk"
URL_RESPONSES = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=894869869"

if 'auth' not in st.session_state:
    st.session_state.auth = False

# --- الواجهة الخارجية (قبل الدخول) ---
if not st.session_state.auth:
    st.title("🛡️ نظام مجموعة أبو الفتوح التجارية")
    
    # هنا الجزء اللي بيسأل المستخدم: إنت مين؟
    tab1, tab2 = st.tabs(["🔐 تسجيل الدخول للأعضاء", "📝 طلب انضمام لموظف جديد"])
    
    with tab1:
        email_login = st.text_input("أدخل بريدك الإلكتروني:")
        if st.button("دخول"):
            if email_login.strip() == "mamer2063@gmail.com":
                st.session_state.auth = True
                st.session_state.user_info = {"Name": "محمد عصام", "Role": "صاحب العمل"}
                st.rerun()
            else:
                try:
                    df = pd.read_csv(URL_RESPONSES)
                    df.columns = [str(c).strip() for c in df.columns]
                    # التأكد من الإيميل والحالة Approved
                    user = df[df.iloc[:, 2].astype(str).str.strip() == email_login.strip()]
                    if not user.empty and str(user.iloc[0].get('Status', '')).strip() == "Approved":
                        st.session_state.auth = True
                        st.session_state.user_info = {"Name": user.iloc[0].iloc[1], "Role": user.iloc[0].iloc[4]}
                        st.rerun()
                    else:
                        st.warning("⚠️ الحساب بانتظار تفعيل الإدارة.")
                except:
                    st.error("❌ فشل الدخول.")

    with tab2:
        st.subheader("تقديم طلب التحاق بالمنظومة")
        st.write("أهلاً بك. لكي تتمكن من استخدام النظام، يجب ملء طلب الانضمام أولاً:")
        url_form = "https://docs.google.com/forms/d/e/1FAIpQLSf3xBxqE0rDxeKJ8YuNZpdYckp8FKPt0eBiq1Sgevnp8ts9FQ/viewform"
        st.markdown(f'<a href="{url_form}" target="_blank"><button style="background-color: #4CAF50; color: white; padding: 15px 32px; border: none; border-radius: 8px; cursor: pointer; font-size: 18px;">🚀 اضغط هنا لفتح نموذج التسجيل</button></a>', unsafe_allow_html=True)

# --- الواجهة الداخلية (بعد الدخول) ---
else:
    user = st.session_state.user_info
    st.sidebar.success(f"مرحباً بك: {user['Name']}")
    
    options = ["الرئيسية"]
    if user['Role'] == "صاحب العمل":
        options.append("👥 إدارة طلبات المستخدمين")
    
    menu = st.sidebar.selectbox("القائمة", options)
    
    if menu == "👥 إدارة طلبات المستخدمين":
        st.title("📋 قائمة المتقدمين الجدد")
        # عرض الجدول ليك إنت بس عشان تعرف مين سجل في الفورم
        df_new = pd.read_csv(URL_RESPONSES)
        st.dataframe(df_new) 
