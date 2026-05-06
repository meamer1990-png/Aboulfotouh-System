import streamlit as st
import pandas as pd

# الرابط الخاص بك (تم التأكد من صحته)
BASE_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR4tUjdMv4rY_meyVWCwB7MYbSGMqBeMzQzXWvI1jNhna34oxOmpMwFPg-HGCmVO7gfLVbDQjCBCbEX/pub?output=csv"

st.set_page_config(page_title="مجموعة أبو الفتوح - النظام المتكامل", layout="wide")

# دالة جلب البيانات مع تنظيف كامل للأخطاء البشرية
def fetch_data(gid):
    try:
        url = f"{BASE_URL}&gid={gid}"
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip() # حذف المسافات من أسماء الأعمدة
        return df
    except:
        return None

if 'auth' not in st.session_state:
    st.session_state.auth = False

# --- واجهة تسجيل الدخول ---
if not st.session_state.auth:
    st.title("🛡️ بوابة الدخول الموحدة")
    email_in = st.text_input("البريد الإلكتروني المعتمد:").strip().lower()
    
    if st.button("تسجيل الدخول"):
        # 1. الدخول المباشر لك يا دكتور (صمام أمان)
        if email_in == "mamer2063@gmail.com":
            st.session_state.auth = True
            st.session_state.user_info = {"Name": "د. محمد عصام", "Role": "صاحب العمل"}
            st.rerun()
        
        # 2. فحص المناديب بدقة (صفحة الردود 894869869)
        df_users = fetch_data("894869869")
        if df_users is not None:
            # البحث عن الإيميل في العمود الثالث (Timestamp, Name, Email...)
            # وتأكد أن الحالة في عمود Status هي approved حصراً
            user_row = df_users[(df_users.iloc[:, 2].astype(str).str.strip().str.lower() == email_in) & 
                                (df_users['Status'].astype(str).str.strip().str.lower() == 'approved')]
            
            if not user_row.empty:
                st.session_state.auth = True
                st.session_state.user_info = {"Name": user_row.iloc[0].iloc[1], "Role": "مندوب مبيعات"}
                st.rerun()
            else:
                st.error("❌ الحساب غير مفعل أو الإيميل خطأ. (يجب أن تكون الحالة approved في الشيت)")
        else:
            st.error("⚠️ فشل الاتصال بقاعدة البيانات. تأكد من نشر الشيت للويب.")

# --- واجهة البرنامج بعد الدخول (التقسيم الداخلي) ---
else:
    st.sidebar.header(f"👤 {st.session_state.user_info['Name']}")
    # التقسيم الواضح الذي طلبته
    tab_menu = st.sidebar.radio("المنظومة الإدارية:", 
        ["📦 المخازن والجرد", "👥 دليل العملاء", "📍 جدول الزيارات", "📊 التقارير والفواتير"])

    if tab_menu == "📦 المخازن والجرد":
        st.header("📦 جرد الأصناف والتقييمات")
        df_inv = fetch_data("0") # صفحة Inventory
        if df_inv is not None:
            st.dataframe(df_inv, use_container_width=True)
        else: st.warning("لا توجد بيانات حالياً")

    elif tab_menu == "👥 دليل العملاء":
        st.header("👥 بيانات التجار والعملاء")
        df_merch = fetch_data("162635924") # صفحة Merchants (تأكد من الـ gid)
        if df_merch is not None:
            st.dataframe(df_merch)

    elif tab_menu == "📍 جدول الزيارات":
        st.header("📍 مواعيد زيارات المناديب")
        st.info("هذا القسم مربوط بصفحة Visits لتنظيم الميدان.")
        # هنا سنضع كود الـ GPS لاحقاً

    elif tab_menu == "📊 التقارير والفواتير":
        st.header("📋 استخراج التقارير")
        st.date_input("حدد الفترة")
        st.button("تحميل تقرير PDF")

    if st.sidebar.button("تسجيل الخروج"):
        st.session_state.auth = False
        st.rerun()
