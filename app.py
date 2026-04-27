import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="مجموعة أبو الفتوح التجارية", layout="wide")

# الرابط المباشر لجلب البيانات
URL = "https://docs.google.com/spreadsheets/d/1Ey5M-J_O50wvYty00cgZvsyKq_LLcQBmMwKWf_Nl_rk/gviz/tq?tqx=out:csv&gid=154670233"

if 'auth' not in st.session_state:
    st.session_state.auth = False

# --- واجهة تسجيل الدخول أو تقديم طلب جديد ---
if not st.session_state.auth:
    tab1, tab2 = st.tabs(["🔐 تسجيل الدخول", "📝 تقديم طلب انضمام جديد"])
    
    with tab1:
        st.subheader("دخول الأعضاء المعتمدين")
        email_login = st.text_input("البريد الإلكتروني المعتمد")
        if st.button("دخول"):
            try:
                df = pd.read_csv(URL)
                df.columns = [str(c).strip() for c in df.columns]
                user_row = df[df['Email'].astype(str).str.strip() == email_login.strip()]
                
                if not user_row.empty:
                    status = str(user_row.iloc[0].iloc[6]).strip() # عمود G (Status)
                    if status == "Approved":
                        st.session_state.auth = True
                        st.session_state.user_info = user_row.iloc[0]
                        st.rerun()
                    else:
                        st.warning("⚠️ حسابك قيد المراجعة من الإدارة.")
                else:
                    st.error("❌ هذا البريد غير مسجل، يرجى تقديم طلب انضمام.")
            except:
                st.error("خطأ في الاتصال.")

    with tab2:
        st.subheader("نموذج تسجيل مستخدم جديد")
        new_name = st.text_input("الاسم الثلاثي")
        new_email = st.text_input("البريد الإلكتروني (سيكون وسيلة دخولك)")
        new_phone = st.text_input("رقم الهاتف")
        new_role = st.selectbox("الوظيفة المطلوبة", ["مندوب", "محاسب", "مدير مخزن", "عميل"])
        
        if st.button("إرسال الطلب"):
            # هنا سنعطي المستخدم رابط نموذج جوجل "Forms" مربوط بالشيت لسهولة الإضافة
            st.success("تم تسجيل بياناتك المبدئية.")
            st.info("لإتمام الطلب ليصل للإدارة فوراً، يرجى ملء هذا النموذج السريع:")
            # ملاحظة: يفضل هنا وضع رابط Google Form مربوط بنفس الشيت بتاعك لضمان وصول البيانات فوراً
            st.markdown(f"[اضغط هنا لإرسال بياناتك للإدارة](https://docs.google.com/forms/d/e/YOUR_FORM_ID/viewform?entry.1={new_name}&entry.2={new_email})")

# --- واجهة البرنامج من الداخل بعد الموافقة ---
else:
    st.balloons()
    user = st.session_state.user_info
    st.sidebar.success(f"مرحباً: {user.iloc[1]}")
    st.sidebar.write(f"الدور: {user.iloc[4]}")
    
    if st.sidebar.button("تسجيل الخروج"):
        st.session_state.auth = False
        st.rerun()

    # --- تقسيم الصلاحيات (ماذا يرى كل مستخدم) ---
    st.title(f"لوحة تحكم {user.iloc[4]}")
    
    if user.iloc[4] == "صاحب العمل":
        st.write("### 🏦 نظرة عامة على المؤسسة")
        # هنا تضع روابط أو جداول الأرباح والطلبات الكلية
        st.metric("إجمالي المبيعات اليوم", "50,000 ج.م")
        
    elif user.iloc[4] == "محاسب":
        st.write("### 📊 الحسابات والميزانية")
        # عرض شيت الحسابات فقط
        
    elif user.iloc[4] == "مندوب":
        st.write("### 🚚 تسجيل طلبات العملاء")
        # هنا تضع فورم لتسجيل الأوردرات الجديدة

    st.write("---")
    st.write("📦 النظام الآن جاهز لاستقبال بيانات المنتجات والمخازن.")
