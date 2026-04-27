import streamlit as st
import pandas as pd

# إعداد الصفحة
st.set_page_config(page_title="مجموعة أبو الفتوح التجارية", layout="wide")

# الرابط السحري لسحب البيانات من الشيت بتاعك مباشرة
# استبدلنا الرابط العادي برابط تصدير CSV
sheet_id = "1Ey5M-J_O50wvYty00cgZvsyKq_LLcQBmMwKWf_Nl_rk"
URL = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=1114501625"

if 'auth' not in st.session_state:
    st.session_state.auth = False

# واجهة الدخول
if not st.session_state.auth:
    st.title("🔐 نظام مجموعة أبو الفتوh")
    email_input = st.text_input("أدخل البريد الإلكتروني المسجل:")
    
    if st.button("تسجيل الدخول"):
        try:
            # قراءة البيانات
            df = pd.read_csv(URL)
            df.columns = df.columns.str.strip() # تنظيف أسماء الأعمدة
            
            # التأكد من وجود الإيميل في الشيت
            user_row = df[df['Email'].astype(str).str.strip() == email_input.strip()]
            
            if not user_row.empty:
                status = user_row.iloc[0]['Status']
                if status == "Approved":
                    st.session_state.auth = True
                    st.session_state.user_info = user_row.iloc[0]
                    st.rerun()
                else:
                    st.warning("⚠️ حسابك موجود ولكنه قيد الانتظار (Pending).")
            else:
                st.error("❌ هذا الإيميل غير مسجل في النظام.")
                if st.button("تقديم طلب انضمام"):
                    st.info("سيتم تحويلك لنموذج التسجيل قريباً")
        except Exception as e:
            st.error("تأكد من كتابة الإيميل بشكل صحيح")

else:
    # لوحة التحكم بعد الدخول
    st.balloons()
    user = st.session_state.user_info
    st.success(f"مرحباً بك: {user['Full_Name']}")
    st.sidebar.title(f"الصلاحية: {user['User_Role']}")
    
    if st.sidebar.button("تسجيل الخروج"):
        st.session_state.auth = False
        st.rerun()

    # هنا نعرض محتوى مختلف حسب الوظيفة
    st.write(f"### لوحة تحكم {user['User_Role']}")
    st.info("تم الاتصال بقاعدة البيانات بنجاح ✅")
