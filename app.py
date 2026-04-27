import streamlit as st
import pandas as pd

# 1. إعداد الصفحة
st.set_page_config(page_title="مجموعة أبو الفتوح التجارية", layout="wide")

# 2. الرابط المحدث لجدول Users_Database (gid=154670233)
sheet_id = "1Ey5M-J_O50wvYty00cgZvsyKq_LLcQBmMwKWf_Nl_rk"
URL = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=154670233"

if 'auth' not in st.session_state:
    st.session_state.auth = False

# 3. واجهة تسجيل الدخول
if not st.session_state.auth:
    st.title("🔐  pourquoi نظام مؤسسه أبو الفتوح التجارية")
    st.write("يرجى إدخال البريد الإلكتروني للوصول إلى لوحة التحكم")
    
    email_input = st.text_input("البريد الإلكتروني")
    
    if st.button("تسجيل الدخول"):
        try:
            # سحب البيانات من الشيت
            df = pd.read_csv(URL)
            # تنظيف المسافات من أسماء الأعمدة والبيانات
            df.columns = df.columns.str.strip()
            
            # البحث عن الإيميل
            user_row = df[df['Email'].astype(str).str.strip() == email_input.strip()]
            
            if not user_row.empty:
                status = user_row.iloc[0]['Status']
                if str(status).strip() == "Approved":
                    st.session_state.auth = True
                    st.session_state.user_info = user_row.iloc[0]
                    st.rerun()
                else:
                    st.warning("⚠️ حسابك قيد المراجعة (Pending).. يرجى التواصل مع الإدارة.")
            else:
                st.error("❌ هذا البريد الإلكتروني غير مسجل في قاعدة البيانات.")
        except Exception as e:
            st.error("⚠️ عذراً، حدث خطأ في الاتصال بقاعدة البيانات. تأكد من إعدادات المشاركة.")

else:
    # 4. لوحة التحكم بعد النجاح
    st.balloons()
    user = st.session_state.user_info
    st.success(f"أهلاً بك يا {user['Full_Name']}")
    st.sidebar.title(f"الوظيفة: {user['User_Role']}")
    
    if st.sidebar.button("تسجيل الخروج"):
        st.session_state.auth = False
        st.rerun()

    st.write("---")
    st.subheader(f"لوحة تحكم: {user['User_Role']}")
    st.info("تم تفعيل الربط بنجاح مع Google Sheets ✅")
