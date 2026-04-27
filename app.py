import streamlit as st
import pandas as pd

# إعدادات الصفحة
st.set_page_config(page_title="مجموعة أبو الفتوح التجارية", layout="wide")

# روابط قاعدة البيانات (الشيت)
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
        email_login = st.text_input("البريد الإلكتروني المعتمد:")
        if st.button("دخول"):
            try:
                # قراءة الشيت والتأكد من الحالة
                df = pd.read_csv(URL)
                df.columns = [str(c).strip() for c in df.columns]
                user = df[df['Email'].astype(str).str.strip() == email_login.strip()]
                
                if not user.empty:
                    # العمود G (رقم 7) فيه كلمة Approved
                    status = str(user.iloc[0].iloc[6]).strip()
                    if status == "Approved":
                        st.session_state.auth = True
                        st.session_state.user_info = user.iloc[0]
                        st.rerun()
                    else:
                        st.warning("⚠️ طلبك قيد المراجعة حالياً. سيتم تفعيل حسابك فور موافقة الإدارة.")
                else:
                    st.error("❌ هذا الإيميل غير مسجل. يرجى تقديم طلب انضمام أولاً.")
            except:
                st.error("⚠️ فشل الاتصال بقاعدة البيانات. تأكد من "نشر الشيت على الويب".")

    with tab2:
        st.subheader("هل أنت موظف جديد؟")
        st.write("يرجى الضغط على الزر أدناه لتعبئة بياناتك الرسمية. بعد الإرسال، سيقوم المدير بمراجعة طلبك.")
        st.markdown(f'''
            <a href="{FORM_URL}" target="_blank" style="text-decoration: none;">
                <button style="background-color: #4CAF50; color: white; padding: 15px 32px; text-align: center; font-size: 16px; margin: 4px 2px; cursor: pointer; border-radius: 8px; border: none;">
                    🚀 اضغط هنا لفتح نموذج التسجيل
                </button>
            </a>
            ''', unsafe_allow_html=True)

# --- الواجهة الداخلية (بعد الموافقة) ---
else:
    st.balloons()
    user_data = st.session_state.user_info
    role = user_data.iloc[4] # العمود E فيه الوظيفة
    
    st.sidebar.success(f"مرحباً بك يا {user_data.iloc[1]}")
    st.sidebar.write(f"الصلاحية: {role}")
    
    if st.sidebar.button("تسجيل الخروج"):
        st.session_state.auth = False
        st.rerun()

    # محتوى لوحة التحكم حسب الوظيفة
    st.title(f"لوحة تحكم: {role}")
    st.write("---")
    
    if role == "صاحب العمل":
        st.subheader("🏦 إدارة المؤسسة")
        col1, col2, col3 = st.columns(3)
        col1.metric("إجمالي المندوبين", "5")
        col2.metric("الطلبات النشطة", "12")
        col3.metric("ميزانية اليوم", "25,000 ج.م")
        st.info("إشعار: يمكنك الآن متابعة جميع حركات المندوبين من هنا.")
        
    elif role == "مندوب":
        st.subheader("🚚 قسم المندوبين")
        st.button("➕ تسجيل طلبية جديدة")
        st.button("📦 عرض المخزون المتاح")
        
    else:
        st.write("مرحباً بك في النظام. سيتم إضافة أدواتك الخاصة قريباً.")

    st.write("---")
    st.caption("نظام مجموعة أبو الفتوح التجارية - 2026")
