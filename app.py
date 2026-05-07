import streamlit as st
import pandas as pd
from datetime import datetime

# الروابط و الـ GIDs المستخرجة من شيتاتك
BASE_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR4tUjdMv4rY_meyVWCwB7MYbSGMqBeMzQzXWvI1jNhna34oxOmpMwFPg-HGCmVO7gfLVbDQjCBCbEX/pub?output=csv"
GIDS = {
    "Users": "0",
    "Inventory": "1608796075",
    "Visits": "1113063548",
    "Orders": "56426419",
    "Merchants": "162635924"
}

def fetch_data(gid):
    try:
        return pd.read_csv(f"{BASE_URL}&gid={gid}").fillna("")
    except: return None

# --- [1] واجهة الكنترول (الإدارة العليا) ---
def show_control():
    st.header("🎛️ لوحة تحكم الإدارة العليا")
    m = st.tabs(["👥 الحسابات", "📊 الأداء العام", "📦 المخزن", "📩 الشكاوى"])
    
    with m[0]:
        st.subheader("إدارة المستخدمين")
        df = fetch_data(GIDS["Users"])
        st.dataframe(df)
        st.info("💡 تحكم في القبول/التعليق من الشيت مباشرة (Status).")
        
    with m[1]:
        st.subheader("📈 تقييم أداء المؤسسة")
        st.write("مقارنة المبيعات (يومي/أسبوعي/شهري)")
        # سيتم ربطها بشيت المبيعات لرسم بياني
        
    with m[3]:
        st.subheader("📩 صندوق الشكاوى والاقتراحات")
        st.warning("هذا القسم خاص بالكنترول فقط ولا يظهر للمحاسب أو المندوب.")

# --- [2] واجهة المحاسب (المايسترو) ---
def show_accountant():
    st.header("🧾 الواجهة المحاسبية")
    m = st.tabs(["🚗 خطوط السير", "📑 تقارير المبيعات", "📦 طلبات العملاء"])
    
    with m[0]:
        st.subheader("تحديد خط سير المندوب")
        # واجهة لاختيار المندوب وتحديد مدن الزيارة
        st.selectbox("اختر المندوب", ["مندوب 1", "مندوب 2"])
        st.date_input("موعد الزيارة")
        st.button("تأكيد خط السير")

# --- [3] واجهة المندوب (الميدانية) ---
def show_salesman():
    st.header("🚗 بوابة المندوب الميدانية")
    m = st.tabs(["📍 الزيارات اليومية", "📝 تسجيل عميل جديد", "🧾 فاتورة بيع"])
    
    with m[0]:
        st.subheader("📍 تأكيد الزيارة بالـ GPS")
        st.info("خط السير المحدد لك اليوم: (القاهرة - وسط البلد)")
        if st.button("📍 تسجيل وصول (تأكيد الموقع والوقت)"):
            st.success(f"تم تسجيل الزيارة في {datetime.now().strftime('%H:%M')} مع مطابقة الموقع.")
            
    with m[1]:
        st.subheader("📝 إضافة عميل جديد")
        with st.form("new_client"):
            st.text_input("اسم النشاط")
            st.text_input("العنوان")
            st.button("📍 التقاط موقع GPS للعميل")
            st.form_submit_button("حفظ وإرسال للكنترول")

    with m[2]:
        st.subheader("🧾 إصدار فاتورة واتساب")
        # واجهة اختيار المنتجات وحساب الإجمالي
        df_inv = fetch_data(GIDS["Inventory"])
        selected_item = st.selectbox("اختر المنتج", df_inv.iloc[:, 0])
        qty = st.number_input("الكمية", min_value=1)
        if st.button("إضافة للسلة"):
            st.write(f"تمت الإضافة. الإجمالي: {qty * 10} جنيه")
        st.button("📤 إرسال الفاتورة واتساب للعميل")

# --- [4] واجهة العميل (الخدمة الذاتية) ---
def show_customer():
    st.header("🤝 بوابة عملاء Pourquoi")
    m = st.tabs(["📅 مواعيدي", "🛒 طلب أوردر", "💬 شكاوى"])
    
    with m[0]:
        st.info("موعد زيارة المندوب القادمة: الأحد 10 مايو - مندوب: أحمد علي")
        
    with m[1]:
        st.subheader("🛒 سلة المشتريات")
        st.write("اختر منتجاتك وسنصدر لك فاتورة مبدئية.")
        st.warning("⚠️ ملاحظة: طلب لم يتم تنفيذه حتى الآن")

# --- محرك التشغيل الأساسي ---
if st.session_state.auth:
    role = st.session_state.role
    if role == "الكنترول": show_control()
    elif role == "محاسب": show_accountant()
    elif role == "مندوب": show_salesman()
    elif role == "عميل": show_customer()
