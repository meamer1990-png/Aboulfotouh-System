import streamlit as st
import pandas as pd

st.set_page_config(page_title="مجموعة أبو الفتوح التجارية", layout="wide")

# رابط الشيت الأساسي (بصيغة CSV)
# تأكد من أن "النشر على الويب" يشمل المستند بأكمله
sheet_id = "1Ey5M-J_O50wvYty00cgZvsyKq_LLcQBmMwKWf_Nl_rk"
# رابط صفحة ردود النموذج (Form Responses) - gid=894869869 كما في صورتك
URL_RESPONSES = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=894869869"

if 'auth' not in st.session_state:
    st.session_state.auth = False

# --- الواجهة الخارجية ---
if not st.session_state.auth:
    st.title("🛡️ نظام إدارة مجموعة أبو الفتوح")
    
    tab1, tab2 = st.tabs(["🔐 تسجيل الدخول", "📝 طلب انضمام جديد"])
    
    with tab1:
        email_login = st.text_input("البريد الإلكتروني")
        if st.button("دخول"):
            # دخول استثنائي لك يا دكتور محمد كصاحب عمل
            if email_login.strip() == "mamer2063@gmail.com":
                st.session_state.auth = True
                st.session_state.user_info = {"Name": "Mohamed Essam", "Role": "صاحب العمل"}
                st.rerun()
            
            try:
                df = pd.read_csv(URL_RESPONSES)
                df.columns = [str(c).strip() for c in df.columns]
                # البحث في عمود البريد الإلكتروني (العمود C في صورتك)
                user = df[df.iloc[:, 2].astype(str).str.strip() == email_login.strip()]
                
                if not user.empty:
                    # التحقق من عمود الموافقة (سنفترض أنك ستضيف عمود في الشيت للموافقة)
                    st.warning("⚠️ طلبك وصل للإدارة وهو قيد المراجعة حالياً.")
                else:
                    st.error("❌ هذا الإيميل غير مسجل.")
            except:
                st.error("⚠️ فشل الاتصال.. تأكد من تفعيل 'النشر على الويب' لصفحة الردود.")

    with tab2:
        st.subheader("تقديم طلب جديد")
        st.write("بياناتك ستظهر فوراً عند الإدارة بعد ملء النموذج.")
        url_form = "https://docs.google.com/forms/d/e/1FAIpQLSf3xBxqE0rDxeKJ8YuNZpdYckp8FKPt0eBiq1Sgevnp8ts9FQ/viewform"
        st.markdown(f'<a href="{url_form}" target="_blank"><button style="background-color: #4CAF50; color: white; padding: 12px 24px; border: none; border-radius: 8px; cursor: pointer;">🚀 افتح نموذج التسجيل</button></a>', unsafe_allow_html=True)

# --- الواجهة الداخلية ---
else:
    st.balloons()
    user = st.session_state.user_info
    st.sidebar.success(f"مرحباً: {user['Name']}")
    
    if st.sidebar.button("خروج"):
        st.session_state.auth = False
        st.rerun()

    st.title(f"لوحة تحكم: {user['Role']}")
    
    # ميزة لك يا دكتور محمد: رؤية المتقدمين الجدد من داخل البرنامج
    if user['Role'] == "صاحب العمل":
        st.subheader("📋 طلبات الانضمام الجديدة (من الشيت مباشرة)")
        try:
            data = pd.read_csv(URL_RESPONSES)
            st.dataframe(data) # سيعرض لك الجدول الذي في صورتك الأخيرة داخل البرنامج
            st.info("💡 يمكنك الموافقة عليهم من خلال ملف الإكسيل مباشرة.")
        except:
            st.write("لا توجد بيانات حالياً أو تأكد من النشر على الويب.")
