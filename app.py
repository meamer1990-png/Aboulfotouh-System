import streamlit as st
import pandas as pd

st.set_page_config(page_title="مجموعة أبو الفتوح", layout="wide")

# الرابط المباشر لصفحة Users_Database
URL = "https://docs.google.com/spreadsheets/d/1Ey5M-J_O50wvYty00cgZvsyKq_LLcQBmMwKWf_Nl_rk/gviz/tq?tqx=out:csv&gid=154670233"

if 'auth' not in st.session_state:
    st.session_state.auth = False

st.title("🔐 نظام إدارة مؤسسة أبو الفتوح")

if not st.session_state.auth:
    email_input = st.text_input("أدخل البريد الإلكتروني المعتمد:")
    
    if st.button("تسجيل الدخول"):
        try:
            # قراءة البيانات مع ضمان جلب كافة الأعمدة
            df = pd.read_csv(URL)
            
            # تنظيف البيانات
            df.columns = [str(c).strip() for c in df.columns]
            
            # البحث عن الإيميل في العمود رقم 3 (Email)
            email_col = 'Email' if 'Email' in df.columns else df.columns[2]
            user_row = df[df[email_col].astype(str).str.strip() == email_input.strip()]
            
            if not user_row.empty:
                # العمود G هو العمود رقم 7 في ترتيب الإكسيل (Status)
                # في البرمجة الترتيب يبدأ من 0، لذا العمود G هو index 6
                status = str(user_row.iloc[0].iloc[6]).strip()
                
                if status == "Approved":
                    st.session_state.auth = True
                    st.session_state.user_info = user_row.iloc[0]
                    st.rerun()
                else:
                    st.warning(f"⚠️ حالة الحساب الحالية: {status}. يرجى الانتظار للموافقة.")
            else:
                st.error("❌ هذا البريد الإلكتروني غير مسجل.")
                
        except Exception as e:
            st.error(f"خطأ تقني: {e}")
else:
    st.balloons()
    # جلب الاسم من العمود الثاني (Full_Name)
    st.success(f"مرحباً بك يا {st.session_state.user_info.iloc[1]}")
    st.write(f"صلاحيتك الحالية: {st.session_state.user_info.iloc[4]}") # العمود E (User_Role)
    
    if st.sidebar.button("تسجيل الخروج"):
        st.session_state.auth = False
        st.rerun()
