import streamlit as st
import pandas as pd
from datetime import datetime

# -------------------------------------------------------------------
#  الإعدادات الأساسية
# -------------------------------------------------------------------
BASE_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR4tUjdMv4rY_meyVWCwB7MYbSGMqBeMzQzXWvI1jNhna34oxOmpMwFPg-HGCmVO7gfLVbDQjCBCbEX/pub?output=csv"
GIDS = {
    "Users": "0",
    "Inventory": "1608796075",
    "Visits": "1113063548",
    "Orders": "56426419",
    "Merchants": "162635924"
}

st.set_page_config(page_title="Pourquoi System", layout="wide")

# -------------------------------------------------------------------
#  دوال مساعدة
# -------------------------------------------------------------------
def fetch_data(gid):
    try:
        df = pd.read_csv(f"{BASE_URL}&gid={gid}")
        df.columns = df.columns.str.strip()
        return df.fillna("")
    except Exception as e:
        st.error(f"خطأ في تحميل البيانات: {e}")
        return None

# -------------------------------------------------------------------
#  تهيئة session_state
# -------------------------------------------------------------------
if 'auth' not in st.session_state:
    st.session_state.auth = False
    st.session_state.role = None
    st.session_state.user_details = None
    st.session_state.cart = []          # سلة المندوب
    st.session_state.new_customer_gps = None   # موقع العميل الجديد

# -------------------------------------------------------------------
#  1. واجهة تسجيل الدخول
# -------------------------------------------------------------------
if not st.session_state.auth:
    st.title("🛡️ بوابة Pourquoi")
    login_id = st.text_input("الإيميل المعتمد:").strip().lower()
    if st.button("دخول النظام"):
        # حسبات خاصة بالمديرين
        if login_id in ["mamer2063@gmail.com", "meamer1990@gmail.com", "admin"]:
            st.session_state.auth = True
            st.session_state.role = "الكنترول"
            st.session_state.user_details = {"الاسم": "د. محمد عصام", "Email": login_id}
            st.rerun()
        else:
            df_u = fetch_data(GIDS["Users"])
            if df_u is not None and len(df_u.columns) >= 3:
                # البحث عن الإيميل (العمود الثالث غالباً)
                matched = df_u[df_u.iloc[:, 2].astype(str).str.strip().str.lower() == login_id]
                if not matched.empty:
                    # تحديد عمود الحالة (قد يختلف اسمه)
                    status_col = "Status" if "Status" in matched.columns else matched.columns[4]
                    status_value = str(matched[status_col].iloc[0]).lower()
                    if status_value == "approved":
                        st.session_state.auth = True
                        st.session_state.role = matched.iloc[0].get("الغرض من الدخول", "عميل")
                        st.session_state.user_details = {
                            "الاسم": matched.iloc[0, 1],   # العمود الثاني غالباً فيه الاسم
                            "Email": login_id
                        }
                        st.rerun()
                    else:
                        st.error("الحساب غير مفعل (لم تتم الموافقة بعد)")
                else:
                    st.error("البريد الإلكتروني غير مسجل")
            else:
                st.error("تعذر تحميل بيانات المستخدمين")

# -------------------------------------------------------------------
#  2. الواجهات الرئيسية بعد تسجيل الدخول
# -------------------------------------------------------------------
else:
    role = st.session_state.role
    user_name = st.session_state.user_details.get("الاسم", "مستخدم")
    st.sidebar.title(f"👤 {user_name}")
    st.sidebar.info(f"الرتبة: {role}")

    # -----------------------------------------------------------------
    #  أ. دور الكنترول
    # -----------------------------------------------------------------
    if role == "الكنترول":
        tab1, tab2, tab3, tab4 = st.tabs(["📊 الأداء", "👥 الحسابات", "📦 المخزن", "📩 الشكاوى"])
        with tab1:
            st.subheader("📈 تقييم الأداء العام")
            st.write("مخططات المبيعات هنا لاحقاً")
        with tab2:
            users_df = fetch_data(GIDS["Users"])
            if users_df is not None:
                st.dataframe(users_df)
            else:
                st.warning("لا توجد بيانات للحسابات")
        with tab3:
            inv_df = fetch_data(GIDS["Inventory"])
            if inv_df is not None:
                st.dataframe(inv_df)
            else:
                st.warning("لا توجد بيانات للمخزن")
        with tab4:
            st.info("قسم الشكاوى قيد الإعداد")

    # -----------------------------------------------------------------
    #  ب. دور المحاسب
    # -----------------------------------------------------------------
    elif role == "محاسب":
        st.header("🧾 واجهة المحاسبة")
        menu = st.sidebar.radio("المهام", ["إدارة المناديب", "خطوط السير", "التقارير"])
        if menu == "خطوط السير":
            st.subheader("🗓️ تعيين خط سير")
            users_df = fetch_data(GIDS["Users"])
            if users_df is not None and len(users_df) > 0:
                # اختيار المندوبين (من يفترض أن دورهم "مندوب")
                mandوبين = users_df[users_df.iloc[:, 3].astype(str).str.contains("مندوب", na=False)].iloc[:, 1].tolist()
                if mandوبين:
                    st.selectbox("اختر المندوب", mandوبين)
                else:
                    st.warning("لا يوجد مناديب مسجلون")
            st.text_input("المدن المستهدفة")
            st.button("تثبيت خط السير")

    # -----------------------------------------------------------------
    #  ج. دور المندوب
    # -----------------------------------------------------------------
    elif role == "مندوب":
        st.header("🚗 بوابة المندوب")
        task = st.sidebar.radio("القائمة", ["📍 الزيارات اليومية", "🔒 تسجيل عميل", "🧾 فاتورة"])

        # ---------- الزيارات اليومية ----------
        if task == "📍 الزيارات اليومية":
            st.subheader("تأكيد الوصول للعميل")
            if st.button("📍 تسجيل وصول GPS"):
                st.success(f"تم تسجيل الوقت: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} والموقع بنجاح (محاكاة).")

        # ---------- تسجيل عميل جديد ----------
        elif task == "🔒 تسجيل عميل":
            st.subheader("📝 تسجيل عميل جديد")

            # زر التقاط الموقع (سيظهر الزر، وعند الضغط سيتم تخزين النتيجة)
            # نستخدم streamlit_geolocation إذا كانت مثبتة، وإلا نعطي محاكاة
            try:
                from streamlit_geolocation import streamlit_geolocation
                geo = streamlit_geolocation()
                if geo and isinstance(geo, dict) and geo.get('latitude'):
                    st.session_state.new_customer_gps = geo
                    st.success(f"✅ تم التقاط الموقع: {geo['latitude']:.6f}, {geo['longitude']:.6f}")
                else:
                    if st.session_state.new_customer_gps is None:
                        st.info("اضغط على الزر الأحمر لالتقاط موقع العميل")
            except ImportError:
                st.warning("مكتبة streamlit-geolocation غير مثبتة. سيتم استخدام محاكاة.")
                if st.button("📍 التقاط إحداثيات GPS (محاكاة)"):
                    # محاكاة إحداثيات القاهرة
                    st.session_state.new_customer_gps = {"latitude": 30.0444, "longitude": 31.2357}
                    st.success("تم التقاط موقع تجريبي (محاكاة)")

            # نموذج إدخال بيانات العميل
            with st.form("form_new_customer"):
                name = st.text_input("اسم المحل/التاجر")
                address = st.text_input("العنوان التفصيلي")
                submitted = st.form_submit_button("💾 حفظ وإرسال للكنترول")
                if submitted:
                    if not name:
                        st.error("يرجى إدخال اسم العميل")
                    elif st.session_state.new_customer_gps is None:
                        st.error("يرجى التقاط موقع GPS أولاً باستخدام الزر أعلاه")
                    else:
                        st.success(f"تم حفظ العميل {name} مع الموقع {st.session_state.new_customer_gps}")
                        # هنا يمكن إضافة كود رفع البيانات إلى Google Sheets
                        # إعادة تعيين موقع العميل بعد الحفظ
                        st.session_state.new_customer_gps = None

        # ---------- إنشاء فاتورة ----------
        elif task == "🧾 فاتورة":
            st.subheader("🧾 إنشاء فاتورة")
            df_inv = fetch_data(GIDS["Inventory"])
            if df_inv is not None and not df_inv.empty:
                # عرض المنتجات في السلة الحالية
                if st.session_state.cart:
                    st.markdown("### 🛒 المنتجات المضافة")
                    cart_df = pd.DataFrame(st.session_state.cart, columns=["المنتج", "الكمية"])
                    st.table(cart_df)
                    if st.button("🗑️ تفريغ السلة"):
                        st.session_state.cart = []
                        st.rerun()

                col1, col2 = st.columns(2)
                with col1:
                    product = st.selectbox("المنتج", df_inv.iloc[:, 0].tolist())
                with col2:
                    qty = st.number_input("الكمية", min_value=1, step=1, value=1)

                if st.button("➕ إضافة إلى السلة"):
                    st.session_state.cart.append([product, qty])
                    st.success(f"تمت إضافة {qty} من {product}")
                    st.rerun()

                if st.button("📤 إرسال فاتورة واتساب"):
                    if st.session_state.cart:
                        invoice_text = "\n".join([f"{p[0]}: {p[1]}" for p in st.session_state.cart])
                        st.info(f"سيتم إرسال:\n{invoice_text}")
                        # يمكن إضافة واجهة واتساب حقيقية عبر pywhatkit مثلاً
                    else:
                        st.warning("السلة فارغة")
            else:
                st.error("لا توجد بيانات للمنتجات")

    # -----------------------------------------------------------------
    #  دور غير معروف
    # -----------------------------------------------------------------
    else:
        st.warning(f"⚠️ دور '{role}' غير معروف في النظام")

    # -----------------------------------------------------------------
    #  زر الخروج في الشريط الجانبي
    # -----------------------------------------------------------------
    if st.sidebar.button("🚪 خروج"):
        st.session_state.auth = False
        st.session_state.cart = []
        st.session_state.new_customer_gps = None
        st.rerun()
