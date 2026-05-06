import streamlit as st
import pandas as pd

# روابط الجداول من صورك (Users, Inventory, Orders, Merchants)
# تأكد من تحديث الـ gid لكل جدول بناءً على الملفات المرفوعة
BASE_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR4tUjdMv4rY_meyVWCwB7MYbSGMqBeMzQzXWvI1jNhna34oxOmpMwFPg-HGCmVO7gfLVbDQjCBCbEX/pub?output=csv"

st.set_page_config(page_title="Pourquoi - إدارة مؤسسة أبوالفتوح", layout="wide")

def fetch_data(gid):
    try:
        url = f"{BASE_URL}&gid={gid}"
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip()
        return df
    except:
        return None

if 'auth' not in st.session_state:
    st.session_state.auth = False
    st.session_state.role = None
    st.session_state.user_details = None

# --- [1] واجهة الدخول ---
if not st.session_state.auth:
    st.title("🛡️ نظام Pourquoi - تسجيل الدخول")
    login_id = st.text_input("أدخل البريد الإلكتروني المعتمد:").strip().lower()
    
    if st.button("دخول"):
        # الدخول المباشر لحضرتك كمسؤول (الكنترول)
        if login_id == "meamer1990@gmail.com" or login_id == "admin": 
            st.session_state.auth = True
            st.session_state.role = "الكنترول"
            st.session_state.user_details = {"الاسم": "د. محمد عصام"}
            st.rerun()
        
        # التحقق من بقية المستخدمين من شيت Users (gid=0 أو حسب صورتك)
        df_users = fetch_data("0") 
        if df_users is not None:
            user_row = df_users[df_users['البريد الإلكتروني'].astype(str).str.strip().str.lower() == login_id]
            if not user_row.empty:
                status = str(user_row.iloc[0]['Status']).strip().lower()
                if status == "approved":
                    st.session_state.auth = True
                    st.session_state.role = user_row.iloc[0]['الوظيفة المطلوبة']
                    st.session_state.user_details = user_row.iloc[0].to_dict()
                    st.rerun()
                else:
                    st.warning("⚠️ الحساب بانتظار موافقة الكنترول.")
            else:
                st.error("❌ البريد غير مسجل.")

# --- [2] واجهات النظام ---
else:
    role = st.session_state.role
    st.sidebar.title(f"مرحباً: {st.session_state.user_details['الاسم']}")
    
    if role == "الكنترول":
        st.header("🎛️ لوحة تحكم الإدارة (الكنترول)")
        
        menu = st.sidebar.selectbox("القائمة", ["إدارة طلبات المستخدمين", "المخزن", "الطلبات الواردة"])
        
        if menu == "إدارة طلبات المستخدمين":
            st.subheader("📝 طلبات التسجيل الجديدة")
            df_req = fetch_data("0") # شيت المستخدمين
            if df_req is not None:
                # عرض الطلبات التي حالتها ليست approved
                pending = df_req[df_req['Status'] != 'approved']
                st.table(pending[['الاسم ثلاثي', 'الوظيفة المطلوبة', 'رقم الهاتف', 'Status']])
                
                # أزرار التحكم (محاكاة التفعيل)
                st.info("لقبول طلب: يرجى تغيير الحالة في شيت جوجل إلى 'approved' وسيتم تفعيل الدخول فوراً.")
        
        elif menu == "المخزن":
            st.subheader("📦 حالة المخزن والأصناف")
            df_inv = fetch_data("1608796075") # من صورتك لجدول Inventory
            if df_inv is not None:
                st.dataframe(df_inv)

    elif role == "مندوب":
        st.title("🚗 واجهة المندوب")
        st.write("سيتم إضافة أزرار الـ GPS وإصدار الفواتير هنا في الخطوة القادمة.")

    if st.sidebar.button("تسجيل الخروج"):
        st.session_state.auth = False
        st.rerun()
