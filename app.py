import streamlit as st
import pandas as pd

# 1. إعداد الصفحة
st.set_page_config(page_title="مجموعة أبو الفتوح التجارية", layout="wide")

# 2. الروابط الخاصة بك
URL = "https://docs.google.com/spreadsheets/d/1Ey5M-J_O50wvYty00cgZvsyKq_LLcQBmMwKWf_Nl_rk/gviz/tq?tqx=out:csv&gid=154670233"
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSf3xBxqE0rDxeKJ8YuNZpdYckp8FKPt0eBiq1Sgevnp8ts9FQ/viewform"

if 'auth' not in st.session_state:
    st.session_state.auth = False

# --- الواجهة الخارجية ---
if not st.session_state.auth:
    st.title("🛡️ نظام إدارة مجموعة أبو الفتوح")
    
    tab1, tab2 = st.tabs(["🔐 تسجيل الدخول", "📝 طلب انضمام جديد"])
    
    with tab1:
        st.subheader("دخول الأعضاء المعتمدين")
        email_login = st.text_input("البريد الإلكتروني المعتمد")
        if st.button("دخول"):
            try:
                df = pd.read_csv(URL)
                df.columns = [str(c).strip() for c in df.columns]
                user = df[df['Email'].astype(str).str.strip() == email_login.strip()]
                
                if not user.empty:
                    # التحقق من عمود الحالة (العمود رقم 7)
                    status = str(user.iloc[0].iloc[6]).strip()
                    if status == "Approved":
                        st.session_state.auth = True
                        st.session_state.user_info = user.iloc[0]
                        st.rerun()
                    else:
                        st.warning("⚠️ طلبك قيد المراجعة حالياً.")
                else:
                    st.error("❌ هذا الإيميل غير مسجل.")
            except Exception as e:
                st.error("⚠️ فشل الاتصال بقاعدة البيانات.")

    with tab2:
        st.subheader("هل أنت موظف جديد؟")
        st.write("يرجى الضغط على الزر أدناه لتعبئة بياناتك. بعد الإرسال، سيقوم المدير بمراجعة طلبك.")
        # زر كبير وواضح للتسجيل
        st.markdown(f'<a href="{FORM_URL}" target="_blank"><button style="background-color: #4CAF50; color: white; padding: 15px 32px; border: none; border-radius: 8px; cursor: pointer; font-size: 18px;">🚀 اضغط هنا لفتح نموذج التسجيل</button></a>', unsafe_allow_html=True)

# --- الواجهة الداخلية (بعد الموافقة) ---
else:
    st.balloons()
    user_data = st.session_state.user_info
    # جلب الوظيفة من العمود رقم 5 (Index 4)
    role = str(user_data.iloc[4]).strip()
    
    st.sidebar.success(f"مرحباً: {user_data.iloc[1]}")
    st.sidebar.write(f"الوظيفة: {role}")
    
    if st.sidebar.button("تسجيل الخروج"):
        st.session_state.auth = False
        st.rerun()

    st.title(f"لوحة تحكم: {role}")
    st.write("---")
    
    if role == "صاحب العمل":
        st.subheader("🏦 إدارة المؤسسة")
        st.info("أهلاً يا دكتور محمد. يمكنك الآن متابعة جميع الحركات.")
        # عرض البيانات الأساسية
        col1, col2 = st.columns(2)
        col1.metric("حالة النظام", "متصل ✅")
        col2.metric("قاعدة البيانات", "محدثة 📊")
        
    elif role == "مندوب":
        st.subheader("🚚 قسم المندوبين")
        st.write("مرحباً بك. يمكنك البدء في تسجيل العمليات.")
        
    else:
        st.write("مرحباً بك في النظام. سيتم تخصيص أدواتك قريباً.")

    st.write("---")
    st.caption("نظام مجموعة أبو الفتوح التجارية - 2026")
