ADMIN_EMAIL = "meamer1990@gmail.com" # ضع هنا إيميلك الذي ستستخدمه للدخول
# فحص هل المستخدم الحالي هو المدير؟
if user_email == ADMIN_EMAIL:
    st.sidebar.markdown("---") # خط فاصل في القائمة الجانبية
    admin_choice = st.sidebar.selectbox("🛠️ لوحة الإدارة", ["عرض البيانات", "الموافقة على الأعضاء"])

    if admin_choice == "الموافقة على الأعضاء":
        st.header("إدارة طلبات الانضمام الجديدة")
        
        # قراءة البيانات من الشيت
        users_df = conn.read(worksheet="Users_Database")
        
        # تصفية الأشخاص الذين حالتهم "Pending" (قيد الانتظار)
        pending_users = users_df[users_df['Status'] == 'Pending']
        
        if not pending_users.empty:
            for index, row in pending_users.iterrows():
                # عرض بيانات كل شخص في إطار منظم
                with st.expander(f"طلب من: {row['Full_Name']}"):
                    st.write(f"**الإيميل:** {row['Email']}")
                    st.write(f"**التليفون:** {row['Phone']}")
                    st.write(f"**الصفة المطلوبة:** {row['User_Role']}")
                    
                    # أزرار الموافقة أو الرفض
                    col1, col2 = st.columns(2)
                    if col1.button("✅ موافقة", key=f"app_{index}"):
                        # كود لتحديث حالة هذا الشخص في جوجل شيت إلى Approved
                        st.success(f"تم تفعيل حساب {row['Full_Name']} بنجاح!")
                        
                    if col2.button("❌ رفض", key=f"rej_{index}"):
                        # كود لمسح الطلب أو تحويله لـ Rejected
                        st.error("تم رفض الطلب.")
        else:
            st.info("لا توجد طلبات انضمام جديدة حالياً.")
