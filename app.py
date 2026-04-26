import streamlit as st
import pandas as pd

st.set_page_config(page_title="مجموعة أبو الفتوح التجارية", layout="wide")

# الرابط المباشر للملف (تم تحديثه ليعمل مع إعداداتك الحالية)
sheet_id = "1Ey5M-J_O50wvYty00cgZvsyKq_LLcQBmMwKWf_Nl_rk"
# هذا الرابط يقرأ الصفحة التي اسمها Users مباشرة
URL = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet=Users"

if 'auth' not in st.session_state:
    st.session_state.auth = False

# واجهة تسجيل الدخول بالعربي
if not st.session_state.auth:
    st.title("🔐 نظام مجموعة أبو الفتوح")
    user_input = st.text_input("اسم المستخدم")
    pass_input = st.text_input("كلمة المرور", type="password")
    
    if st.button("تسجيل الدخول"):
        try:
            # قراءة البيانات مع تنظيفها من المسافات
            df = pd.read_csv(URL)
            df.columns = df.columns.str.strip()
            
            # تحويل المدخلات لنفس تنسيق الشيت
            u_in = str(user_input).strip()
            p_in = str(pass_input).strip()
            
            # البحث عن المستخدم
            match = df[(df['الاسم'].astype(str).str.strip() == u_in) & 
                       (df['كلمة_المرور'].astype(str).str.strip() == p_in)]
            
            if not match.empty:
                st.session_state.auth = True
                st.session_state.user_role = match.iloc[0]['الصلاحية']
                st.session_state.user_full_name = u_in
                st.rerun()
            else:
                st.error("❌ البيانات غير مطابقة.. تأكد من كتابة الاسم والباسورد بالظبط")
        except:
            st.error("⚠️ فشل في الاتصال.. تأكد من تحديث صفحة البرنامج")

else:
    # لوحة التحكم الرئيسية
    st.balloons()
    st.success(f"مرحباً بك يا دكتور محمد في نظامك الخاص")
    st.sidebar.button("خروج")
    st.header(f"لوحة التحكم - قسم: {st.session_state.user_role}")
    st.info("تم تفعيل الربط بنجاح مع Google Sheets")
