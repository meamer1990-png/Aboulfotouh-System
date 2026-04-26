import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# إعداد واجهة البرنامج
st.set_page_config(page_title="نظام أبو الفتوح الذكي", layout="wide")

# 1. الاتصال بجوجل شيت مع محاولة معالجة الخطأ
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(worksheet="Users_Database", ttl=0) # ttl=0 لضمان تحديث البيانات فوراً
except Exception as e:
    st.error("خطأ في الاتصال بقاعدة البيانات. تأكد من إعدادات الـ Secrets وصلاحية رابط الشيت.")
    st.stop()

# 2. تعريف إيميل المدير
ADMIN_EMAIL = "meamer1990@gmail.com" 

st.title("نظام مجموعة أبو الفتوح الذكي 🛡️")

# إدخال الإيميل للدخول
user_email = st.text_input("سجل دخولك بإدخال البريد الإلكتروني:")

if user_email:
    # التأكد من وجود بيانات في الشيت
    if not df.empty:
        # البحث عن الإيميل
        user_data = df[df['Email'].str.strip() == user_email.strip()]

        if not user_data.empty:
            status = user_data.iloc[0]['Status']
            role = user_data.iloc[0]['User_Role']

            if status == "Approved":
                st.success(f"مرحباً بك.. الصلاحية: {role}")

                # ظهور لوحة المدير
                if user_email == ADMIN_EMAIL:
                    st.sidebar.header("⚙️ إدارة النظام")
                    mode = st.sidebar.radio("انتقل إلى:", ["الرئيسية", "طلبات الانضمام"])
                    
                    if mode == "طلبات الانضمام":
                        st.subheader("مراجعة طلبات المستخدمين الجدد")
                        pending = df[df['Status'] == 'Pending']
                        st.dataframe(pending)
                
                st.write("---")
                st.info("لوحة العمل الرئيسية مفعلة الآن.")
            else:
                st.warning("عذراً، حسابك قيد المراجعة. يرجى مراجعة المدير.")
        else:
            st.error("هذا البريد غير مسجل.")
            if st.button("إرسال طلب تسجيل"):
                st.info("تم توجيه طلبك للإدارة.")
