import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. الربط مع جوجل شيت (تأكد من إعداد st.secrets)
conn = st.connection("gsheets", type=GSheetsConnection)

# 2. دالة لجلب بيانات المستخدمين
def get_users_data():
    return conn.read(worksheet="Users_Database")

# 3. شاشة طلب التسجيل
def registration_form():
    st.subheader("📝 طلب انضمام لنظام مجموعة أبو الفتوح")
    with st.form("reg_form"):
        name = st.text_input("الأسم الكامل")
        phone = st.text_input("رقم الهاتف (واتساب)")
        role = st.selectbox("نوع الحساب", ["محاسب", "مندوب", "عميل", "مالك"])
        email = st.text_input("بريد الجيميل (الذي ستدخل به)")
        
        submit = st.form_submit_button("إرسال طلب التسجيل")
        
        if submit:
            if name and phone and email:
                # إضافة البيانات للشيت كطلب جديد (Pending)
                new_request = pd.DataFrame([{
                    "Timestamp": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Full_Name": name,
                    "Email": email,
                    "Phone": phone,
                    "User_Role": role,
                    "Status": "Pending"
                }])
                # تحديث الشيت (تطلب صلاحية الكتابة)
                conn.create(data=new_request, worksheet="Users_Database")
                st.success("تم إرسال طلبك! يرجى انتظار موافقة السيد محمد عصام.")
            else:
                st.error("يرجى ملء كافة الخانات.")

# 4. المنطق الأساسي للبرنامج
st.title("نظام مجموعة أبو الفتوح")

# هنا نفترض وجود زر دخول بسيط (أو ربط Google Auth)
user_email = st.text_input("أدخل بريدك الإلكتروني للدخول")

if user_email:
    users_df = get_users_data()
    user_record = users_df[users_df['Email'] == user_email]
    
    if not user_record.empty:
        status = user_record.iloc[0]['Status']
        role = user_record.iloc[0]['User_Role']
        
        if status == "Approved":
            st.success(f"مرحباً بك ({role})")
            
            # --- هنا يتم عرض الصفحات بناءً على الرتبة ---
            if role == "مالك":
                st.sidebar.button("لوحة تحكم المستخدمين")
                # عرض كافة الصفحات (Inventory, Orders, Merchants)
            elif role == "محاسب":
                # عرض (Orders, Merchants) فقط
                pass
            elif role == "مندوب":
                # عرض نموذج إضافة الطلبات فقط
                pass
        else:
            st.warning("حسابك مسجل ولكن لم يتم تفعيله بعد من قبل الإدارة.")
    else:
        st.info("هذا الإيميل غير مسجل لدينا.")
        registration_form()
