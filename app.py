import streamlit as st
import pandas as pd

# الرابط الأساسي للشيت الخاص بك
BASE_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR4tUjdMv4rY_meyVWCwB7MYbSGMqBeMzQzXWvI1jNhna34oxOmpMwFPg-HGCmVO7gfLVbDQjCBCbEX/pub?output=csv"

st.set_page_config(page_title="منظومة أبو الفتوح", layout="wide")

if 'auth' not in st.session_state:
    st.session_state.auth = False

# --- واجهة الدخول ---
if not st.session_state.auth:
    st.title("🛡️ تسجيل الدخول")
    email_input = st.text_input("أدخل بريدك الإلكتروني:").strip().lower() # تنظيف الإدخال
    
    if st.button("دخول"):
        # دخولك أنت كمالك (ثابت لضمان وصولك دائماً)
        if email_input == "mamer2063@gmail.com":
            st.session_state.auth = True
            st.session_state.user_info = {"Name": "د. محمد عصام", "Role": "صاحب العمل"}
            st.rerun()
            
        try:
            # جلب بيانات المتقدمين (gid=894869869)
            df = pd.read_csv(f"{BASE_URL}&gid=894869869")
            # تنظيف البيانات في الشيت (إزالة المسافات وتحويلها لحروف صغيرة)
            df.columns = [c.strip() for c in df.columns]
            df.iloc[:, 2] = df.iloc[:, 2].astype(str).str.strip().str.lower() # عمود الإيميل
            df['Status'] = df['Status'].astype(str).str.strip().str.lower() # عمود الحالة
            
            # البحث عن المندوب
            user_data = df[df.iloc[:, 2] == email_input]
            
            if not user_data.empty:
                status = user_data.iloc[0]['Status']
                if status == "approved":
                    st.session_state.auth = True
                    st.session_state.user_info = {"Name": user_data.iloc[0].iloc[1], "Role": "مندوب"}
                    st.rerun()
                else:
                    st.warning(f"⚠️ حسابك بانتظار التفعيل. الحالة الحالية: ({status})")
            else:
                st.error("❌ هذا الإيميل غير مسجل في المنظومة.")
        except Exception as e:
            st.error("⚠️ حدث خطأ في الاتصال بالشيت. تأكد من نشر الملف للويب.")

else:
    st.title(f"أهلاً بك يا {st.session_state.user_info['Name']}")
    if st.button("خروج"):
        st.session_state.auth = False
        st.rerun()
