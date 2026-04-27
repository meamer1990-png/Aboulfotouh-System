import streamlit as st
import pandas as pd

st.set_page_config(page_title="مجموعة أبو الفتوح", layout="wide")

# الرابط المباشر بعد النشر (بصيغة CSV)
URL = "https://docs.google.com/spreadsheets/d/1Ey5M-J_O50wvYty00cgZvsyKq_LLcQBmMwKWf_Nl_rk/gviz/tq?tqx=out:csv&gid=154670233"

if 'auth' not in st.session_state:
    st.session_state.auth = False

st.title("🔐 نظام إدارة مؤسسة أبو الفتوح")

if not st.session_state.auth:
    email_input = st.text_input("أدخل البريد الإلكتروني المعتمد:")
    
    if st.button("تسجيل الدخول"):
        try:
            # قراءة البيانات وتجاهل الأخطاء البسيطة في التنسيق
            df = pd.read_csv(URL, on_bad_lines='skip')
            
            # تنظيف البيانات تماماً من المسافات
            df.columns = [str(c).strip() for c in df.columns]
            
            # البحث عن عمود الإيميل سواء كان بالعربي أو بالإنجليزي
            email_col = 'Email' if 'Email' in df.columns else df.columns[0]
            
            # فلترة الجدول
            user_row = df[df[email_col].astype(str).str.strip() == email_input.strip()]
            
            if not user_row.empty:
                # التأكد من حالة الحساب (العمود رقم 5 أو 6)
                status = str(user_row.iloc[0].get('Status', user_row.iloc[0][-1])).strip()
                
                if status.lower() in ["approved", "مقبول"]:
                    st.session_state.auth = True
                    st.session_state.user_info = user_row.iloc[0]
                    st.rerun()
                else:
                    st.warning(f"⚠️ حسابك موجود ولكن حالته حالياً: {status}")
            else:
                st.error("❌ هذا الإيميل غير موجود في القائمة.")
                # لإظهار الأعمدة اللي البرنامج شايفها عشان نعرف المشكلة فين
                st.write("الأعمدة التي قرأها البرنامج:", list(df.columns))
                
        except Exception as e:
            st.error(f"حدث خطأ في قراءة البيانات: {e}")
            st.info("تأكد أنك اخترت 'قيم مفصولة بفاصلة CSV' عند النشر على الويب.")

else:
    st.balloons()
    st.success(f"مرحباً بك يا {st.session_state.user_info.iloc[1]}")
    if st.sidebar.button("خروج"):
        st.session_state.auth = False
        st.rerun()
