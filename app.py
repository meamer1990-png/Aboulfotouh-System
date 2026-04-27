import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة الأساسية
st.set_page_config(page_title="منظومة أبو الفتوح التجارية", layout="wide")

# 2. تعريف روابط الصفحات (استناداً لصورك)
SHEET_ID = "1Ey5M-J_O50wvYty00cgZvsyKq_LLcQBmMwKWf_Nl_rk"
# رابط الردود (gid=894869869)
URL_MAIN = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=894869869"
# رابط المخازن (Inventory) - سنفترض الترتيب التلقائي
URL_INV = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0" 

if 'auth' not in st.session_state:
    st.session_state.auth = False

# --- واجهة الدخول ---
if not st.session_state.auth:
    st.title("🛡️ نظام إدارة مؤسسة أبو الفتوح")
    email_login = st.text_input("أدخل البريد الإلكتروني المسجل:")
    
    if st.button("تسجيل الدخول"):
        # دخول مباشر لك يا دكتور محمد
        if email_login.strip() == "mamer2063@gmail.com":
            st.session_state.auth = True
            st.session_state.user_info = {"Name": "محمد عصام", "Role": "صاحب العمل"}
            st.rerun()
        else:
            try:
                df = pd.read_csv(URL_MAIN)
                # البحث عن الإيميل والتأكد من كلمة approved في عمود Status (صورة fda28b3f)
                user = df[df.iloc[:, 2].astype(str).str.strip() == email_login.strip()]
                if not user.empty and str(user.iloc[0]['Status']).lower() == "approved":
                    st.session_state.auth = True
                    st.session_state.user_info = {"Name": user.iloc[0].iloc[1], "Role": user.iloc[0].iloc[4]}
                    st.rerun()
                else:
                    st.error("❌ الحساب غير مفعل أو غير مسجل.")
            except:
                st.error("⚠️ خطأ في قراءة البيانات. تأكد من 'النشر على الويب'.")

# --- داخل السيستم (بعد الدخول) ---
else:
    user = st.session_state.user_info
    st.sidebar.success(f"مرحباً: {user['Name']}")
    menu = st.sidebar.selectbox("القائمة الرئيسية", ["لوحة التحكم", "📦 المخازن (Inventory)", "🤝 التجار (Merchants)", "📝 الطلبات (Orders)"])

    if menu == "لوحة التحكم":
        st.title(f"أهلاً بك في نظام أبو الفتوح - قطاع {user['Role']}")
        st.info("النظام مرتبط الآن بجداول البيانات التي قمت بتحديثها.")
        
    elif menu == "📦 المخازن (Inventory)":
        st.subheader("قائمة الأصناف المتوفرة")
        # هنا يقرأ من صفحة Inventory اللي في صورتك (b8590080)
        st.write("بيانات الأصناف والكميات المتاحة:")
        # ملاحظة: سنحتاج لضبط الـ gid الخاص بكل صفحة لاحقاً
        st.warning("سيتم عرض جدول الأصناف هنا فور ربط الـ gid الخاص بكل صفحة.")

    elif menu == "🤝 التجار (Merchants)":
        st.subheader("دليل التجار والعملاء")
        # يقرأ من صفحة Merchants (0fb35e18)

    elif menu == "📝 الطلبات (Orders)":
        st.subheader("سجل الطلبيات")
        # يقرأ من صفحة Orders (57cf132d)

    if st.sidebar.button("تسجيل خروج"):
        st.session_state.auth = False
        st.rerun()
