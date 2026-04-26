import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. إعداد الاتصال بجوجل شيت
conn = st.connection("gsheets", type=GSheetsConnection)

# 2. تعريف إيميل المدير (تأكد من وجود علامات التنصيص في البداية والنهاية)
ADMIN_EMAIL = "meamer1990@gmail.com" 

# 3. دالة جلب البيانات من شيت Users_Database
def get_users():
    return conn.read(worksheet="Users_Database")

# --- واجهة البرنامج ---
st.title("نظام مجموعة أبو الفتوح الذكي 🛡️")

# إدخال الإيميل للدخول
user_email = st.text_input("سجل دخولك بإدخال البريد الإلكتروني:")

# التحقق من أن المستخدم أدخل إيميل بالفعل
if user_email:
    # جلب البيانات من الشيت
    df = get_users()
    
    # البحث عن الإيميل المدخل في الشيت
    user_data = df[df['Email'] == user_email]

    if not user_data.empty:
        status = user_data.iloc[0]['Status']
        role = user_data.iloc[0]['User_Role']

        # إذا كان الحساب مفعل
        if status == "Approved":
            st.success(f"أهلاً بك.. صفتك في النظام: {role}")

            # --- ظهور لوحة الإدارة للمدير فقط ---
            if user_email == ADMIN_EMAIL:
                st.sidebar.header("⚙️ لوحة الإدارة")
                menu = st.sidebar.selectbox("القائمة الإدارية", ["الرئيسية", "طلبات الأعضاء"])
                
                if menu == "طلبات الأعضاء":
                    st.subheader("إدارة طلبات الانضمام")
                    # عرض الطلبات التي حالتها Pending فقط
                    pending = df[df['Status'] == 'Pending']
                    if not pending.empty:
                        st.write("الطلبات الجديدة:")
                        st.dataframe(pending[['Full_Name', 'Email', 'User_Role']])
                    else:
                        st.info("لا توجد طلبات جديدة حالياً.")

            # هنا تضع بقية أجزاء برنامجك (المخازن والطلبات)
            st.write("---")
            st.info("تم تسجيل الدخول بنجاح. لوحة العمل مفعلة.")

        else:
            st.warning("حسابك مسجل ولكن لم يتم تفعيله بعد من قبل الإدارة.")
    else:
        st.error("عذراً، هذا البريد غير مسجل في النظام.")
        if st.button("تقديم طلب تسجيل جديد"):
            st.info("يرجى التواصل مع المدير لإضافتك في قاعدة البيانات.")
