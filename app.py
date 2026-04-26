import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. إعداد الاتصال بجوجل شيت
conn = st.connection("gsheets", type=GSheetsConnection)

# 2. تعريف إيميل المدير (اكتب إيميلك هنا بدقة)
ADMIN_EMAIL = "meamer1990@gmail.com
# 3. دالة جلب البيانات من شيت Users_Database
def get_users():
    return conn.read(worksheet="Users_Database")

# --- بداية البرنامج ---
st.title("نظام مجموعة أبو الفتوح الذكي 🛡️")

# محاكاة لعملية الدخول (ستستبدل لاحقاً بزر جوجل لوجن)
user_email = st.text_input("سجل دخولك بإدخال البريد الإلكتروني:")

if user_email:
    df = get_users()
    # البحث عن المستخدم في الشيت
    user_data = df[df['Email'] == user_email]

    if not user_data.empty:
        status = user_data.iloc[0]['Status']
        role = user_data.iloc[0]['User_Role']

        if status == "Approved":
            st.success(f"أهلاً بك.. صفتك في النظام: {role}")

            # --- لوحة التحكم الخاصة بك (تظهر للمدير فقط) ---
            if user_email == ADMIN_EMAIL:
                st.sidebar.header("⚙️ لوحة الإدارة")
                menu = st.sidebar.selectbox("القائمة الإدارية", ["الرئيسية", "الموافقة على الأعضاء"])
                
                if menu == "الموافقة على الأعضاء":
                    st.subheader("طلبات الانضمام المعلقة")
                    pending = df[df['Status'] == 'Pending']
                    if not pending.empty:
                        st.table(pending[['Full_Name', 'Email', 'User_Role']])
                        st.info("يمكنك تفعيلهم مباشرة من ملف جوجل شيت حالياً لضمان استقرار الكود.")
                    else:
                        st.write("لا توجد طلبات جديدة.")

            # هنا تضع بقية صفحات البرنامج (المخازن، الطلبات، إلخ)
            st.write("---")
            st.info("هنا تظهر بيانات العمل الخاصة بك...")

        else:
            st.warning("حسابك قيد المراجعة.. يرجى التواصل مع الإدارة للتفعيل.")
    else:
        st.error("هذا البريد غير مسجل.")
        if st.button("تقديم طلب انضمام"):
            st.write("سيتم فتح نموذج التسجيل هنا...")
