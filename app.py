# ... الكود السابق لقسم المندوب ...

elif task == "📝 تسجيل عميل":
    st.subheader("تسجيل عميل جديد")
    
    # 1. التقاط الموقع
    if st.button("📍 التقاط إحداثيات GPS"):
        new_location = streamlit_geolocation()
        if new_location and isinstance(new_location, dict) and new_location.get('latitude'):
            st.session_state.new_customer_gps = new_location
            st.success(f"تم التقاط الموقع: ({new_location['latitude']:.6f}, {new_location['longitude']:.6f})")
        else:
            st.warning("لم يتم الحصول على الموقع. تأكد من السماح للمتصفح بتحديد موقعك.")
    
    # 2. النموذج لإدخال البيانات
    with st.form("new_customer_form"):
        st.text_input("اسم المحل/التاجر")
        st.text_input("العنوان")
        # عرض حالة الموقع
        if st.session_state.get('new_customer_gps'):
            st.info(f"الموقع الملتقط: {st.session_state.new_customer_gps['latitude']}, {st.session_state.new_customer_gps['longitude']}")
        else:
            st.warning("لم يتم التقاط الموقع بعد، استخدم الزر أعلاه.")
        
        submitted = st.form_submit_button("💾 حفظ وإرسال للكنترول")
        if submitted:
            if st.session_state.get('new_customer_gps'):
                st.success(f"تم حفظ بيانات العميل مع الموقع: {st.session_state.new_customer_gps}")
                # إضافة كود رفع البيانات إلى جدول Google Sheets هنا
            else:
                st.error("لا يمكن حفظ العميل دون التقاط الموقع.")

# ... باقي الكود الخاص بالمندوب والمحاسب والكنترول ...
