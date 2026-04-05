import streamlit as st

st.set_page_config(page_title="Partner | White Label", layout="centered")

st.title("🤝 White Label İş Ortaklığı")
st.write("Kendi İşe Alım Yazılım Markanızı Bugün Kurun.")

st.divider()

# Kâr Hesaplayıcı
st.subheader("💰 Kâr Marjı Analizi")
st.write("Sizin alış fiyatınız ile müşteriye satış fiyatınız arasındaki fark sizin kârınızdır.")

col_a, col_b, col_c = st.columns(3)
col_a.metric("Alış Fiyatınız", "105 ₺")
col_b.metric("Önerilen Satış", "875 ₺")
col_c.metric("Net Kârınız", "770 ₺", delta="800%")

st.divider()

st.write("### Neden Partner Olmalısınız?")
st.write("1. **Sıfır Altyapı Maliyeti:** Yazılımı biz geliştiriyoruz, siz satıyorsunuz.")
st.write("2. **Tam Bağımsızlık:** Kendi logonuz ve kendi fiyat politikanız.")
st.write("3. **7/24 Teknik Destek:** Arka planda biz varız, ön planda sizin markanız.")

if st.button("Bayilik Sözleşmesini İndir"):
    st.write("Sözleşme hazırlanıyor, lütfen bekleyiniz...")
