import streamlit as st
import fitz  # PyMuPDF
import os
from io import BytesIO

# إعدادات الصفحة
st.set_page_config(page_title="PDF Tools Pro", page_icon="📄")

st.title("📄 محرر الـ PDF المتكامل")
st.markdown("---")

# القائمة الجانبية
menu = ["دمج ملفات PDF", "تحويل PDF إلى صور", "تشفير الملف", "استخراج النصوص"]
choice = st.sidebar.selectbox("اختر الميزة", menu)

# --- وظيفة الدمج ---
if choice == "دمج ملفات PDF":
    st.subheader("🔗 دمج الملفات")
    files = st.file_uploader("ارفع ملفات PDF هنا", type="pdf", accept_multiple_files=True)
    if st.button("بدء الدمج"):
        if files:
            new_pdf = fitz.open()
            for f in files:
                with fitz.open(stream=f.read(), filetype="pdf") as m_pdf:
                    new_pdf.insert_pdf(m_pdf)
            out = BytesIO(new_pdf.tobytes())
            st.success("تم الدمج بنجاح!")
            st.download_button("تحميل الملف النهائي", out, "merged.pdf")

# --- وظيفة تحويل الصور ---
elif choice == "تحويل PDF إلى صور":
    st.subheader("🖼️ تحويل لصور")
    file = st.file_uploader("اختر ملف", type="pdf")
    if file:
        doc = fitz.open(stream=file.read(), filetype="pdf")
        for i in range(len(doc)):
            page = doc.load_page(i)
            pix = page.get_pixmap()
            st.image(pix.tobytes(), caption=f"صفحة {i+1}")

# --- وظيفة التشفير ---
elif choice == "تشفير الملف":
    st.subheader("🔐 حماية بكلمة سر")
    file = st.file_uploader("اختر ملف", type="pdf")
    pwd = st.text_input("كلمة السر", type="password")
    if st.button("تشفير"):
        if file and pwd:
            doc = fitz.open(stream=file.read(), filetype="pdf")
            # حفظ مؤقت للتشفير
            doc.save("temp.pdf", encryption=fitz.PDF_ENCRYPT_AES_256, owner_pw=pwd, user_pw=pwd)
            with open("temp.pdf", "rb") as f:
                st.download_button("تحميل الملف المحمي", f.read(), "protected.pdf")
            os.remove("temp.pdf")

# --- وظيفة النصوص ---
elif choice == "استخراج النصوص":
    st.subheader("📝 استخراج الكلام")
    file = st.file_uploader("اختر ملف", type="pdf")
    if file:
        doc = fitz.open(stream=file.read(), filetype="pdf")
        text = "".join([page.get_text() for page in doc])
        st.text_area("النص المكتوب:", text, height=300)
  
