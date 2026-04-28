import streamlit as st
import pandas as pd

# إعدادات الصفحة الرئيسية
st.set_page_config(page_title="منظومة أبو الفتوح التجارية", layout="wide")

# الرابط الأساسي الذي أرسلته (بصيغة CSV)
BASE_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR4tUjdMv4rY_meyVWCwB7MYbSGMqBeMzQzXWvI1jNhna34oxOmpMwFPg-HGCmVO7gfLVbDQjCBCbEX/pub?output=csv"

# وظيفة لجلب البيانات من صفحات مختلفة بناءً على الـ GID
def get_sheet_data(gid):
    url = f"{BASE_URL}&gid={gid}"
    try:
        return pd.read_csv(url)
    except:
        return None

if 'auth' not in st.session_state:
    st.session_state.auth = False

# --- واجهة الدخول ---
if not st.session_state.auth:
    st.title("🛡️ نظام مجموعة أبو الفتوح - تسجيل الدخول")
    
    tab1, tab2 = st.tabs(["🔐 تسجيل دخول", "📝 طلب انضمام جديد"])
    
    with tab1:
        email_login = st.text_input("البريد الإلكتروني المعتمد")
        if st.button("دخول"):
            # دخولك كصاحب عمل
            if email_login.strip() == "mamer2063@gmail.com":
                st.session_state.auth = True
                st.session_state.user_info = {"Name": "د. محمد عصام", "Role": "صاحب العمل"}
                st.rerun()
            else:
                # التأكد من الموظفين (صفحة الردود gid=894869869)
                df_users = get_sheet_data("894869869")
                if df_users is not None:
                    user = df_users[df_users.iloc[:, 2].astype(str).str.strip() == email_login.strip()]
                    if not user.empty and str(user.iloc[0].get('Status', '')).lower() == 'approved':
                        st.session_state.auth = True
                        st.session_state.user_info = {"Name": user.iloc[0].iloc[1], "Role": user.iloc[0].iloc[4]}
                        st.rerun()
                    else:
                        st.warning("⚠️ الحساب بانتظار تفعيل الإدارة (Status: approved)")
                else:
                    st.error("❌ فشل الاتصال بقاعدة البيانات.")

    with tab2:
        st.subheader("تقديم طلب التحاق")
        url_form = "https://docs.google.com/forms/d/e/1FAIpQLSf3xBxqE0rDxeKJ8YuNZpdYckp8FKPt0eBiq1Sgevnp8ts9FQ/viewform"
        st.markdown(f'<a href="{url_form}" target="_blank"><button style="background-color: #4CAF50; color: white; padding: 12px 24px; border: none; border-radius: 8px; cursor: pointer;">🚀 افتح نموذج التسجيل</button></a>', unsafe_allow_html=True)

# --- واجهة النظام من الداخل ---
else:
    user = st.session_state.user_info
    st.sidebar.success(f"مرحباً: {user['Name']}")
    
    # القائمة الجانبية (الأيقونات اللي طلبتها)
    menu = st.sidebar.selectbox("القائمة الرئيسية", 
        ["الرئيسية", "📦 المخازن والتقييمات", "🤝 دليل التجار", "📝 سجل الطلبات", "👥 إدارة الموظفين"])

    if menu == "الرئيسية":
        st.title("🏡 لوحة التحكم الرئيسية")
        st.write("أهلاً بك في النظام الموحد لمجموعة أبو الفتوح.")
        col1, col2, col3 = st.columns(3)
        col1.metric("حالة النظام", "متصل ✅")
        col2.metric("قاعدة البيانات", "محدثة 📊")

    elif menu == "📦 المخازن والتقييمات":
        st.title("📦 جرد المخازن")
        # صفحة Inventory (gid=0)
        df_inv = get_sheet_data("0")
        if df_inv is not None:
            st.dataframe(df_inv, use_container_width=True)
        else:
            st.error("لم يتم العثور على بيانات المخزن.")

    elif menu == "🤝 دليل التجار":
        st.title("🤝 بيانات التجار والعملاء")
        # صفحة Merchants (سأضع gid افتراضي 0، يمكنك تغييره للرقم الصحيح)
        df_merch = get_sheet_data("0") 
        st.write("بيانات المناديب والعملاء المسجلين:")
        st.dataframe(df_merch)

    elif menu == "📝 سجل الطلبات":
        st.title("📝 العمليات التجارية")
        # تحديد فترة التقرير كما طلبت
        col1, col2 = st.columns(2)
        start_date = col1.date_input("من تاريخ")
        end_date = col2.date_input("إلى تاريخ")
        st.button("توليد تقرير الفترة")
        st.info("سيتم عرض الطلبات المحصورة في هذه الفترة هنا.")

    elif menu == "👥 إدارة الموظفين":
        st.title("📋 المتقدمين من النموذج")
        df_req = get_sheet_data("894869869")
        if df_req is not None:
            st.table(df_req)
            st.info("💡 قم بتغيير الحالة لـ approved في الشيت لتفعيل الموظف.")

    if st.sidebar.button("خروج"):
        st.session_state.auth = False
        st.rerun()
