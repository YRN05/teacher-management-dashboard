import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from calc import generate_frequency_table, calculate_stats

st.set_page_config(page_title='Score Management', layout='wide', initial_sidebar_state='collapsed')

st.title("Welcome")
st.header("Your Personal Student's Score Manager")
st.write("\n")
with st.expander("Cara Penggunaan"):
    st.subheader("How it works?")
    st.markdown("Bapak/Ibu Dosen bisa memasukkan file xlsx ke dalam field **'Upload File'** dengan format file seperti ini")
    st.image("images/format-data.png", caption="Contoh Format Kolom")

    st.markdown("Atau silahkan download template dibawah ini")
    try:
        with open("assets/template_mahasiswa.xlsx", "rb") as file:
            st.download_button(
                label="📥 Download Template Excel",
                data=file,
                file_name="template_mahasiswa.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    except FileNotFoundError:
        st.error("File template tidak ditemukan di folder assets.")

st.write('\n')
st.divider()

st.subheader('Silahkan Upload File Bapak/Ibu')
uploaded_file = st.file_uploader(
    "Upload File", accept_multiple_files=False, type=["csv", "xlsx"]
)

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith('.xlsx') else pd.read_csv(uploaded_file)
        target_col = "Nilai"
        
        if target_col in df.columns:
            st.success(f"Berhasil mendeteksi kolom '{target_col}'")
            
            df_freq, bins = generate_frequency_table(df, target_col)
            
            st.subheader("📊 Tabel Distribusi Frekuensi")
            st.dataframe(df_freq, use_container_width=True)
            
            st.subheader("📝 Statistik Deskriptif")
            df_stats = calculate_stats(df, target_col)
            st.table(df_stats.style.format({"Nilai": "{:.2f}"}))
            
            st.divider()
            
            st.subheader("📈 Visualisasi Statistika")
            col1, col2 = st.columns(2)
            mid_points = [(bins[i] + bins[i+1])/2 for i in range(len(bins)-1)]
            
            with col1:
                fig1, ax1 = plt.subplots()
                ax1.bar(mid_points, df_freq['Frekuensi (f)'], width=(bins[1]-bins[0]), 
                        color='skyblue', edgecolor='black', alpha=0.6, label='Histogram')
                ax1.plot(mid_points, df_freq['Frekuensi (f)'], marker='o', color='red', label='Poligon')
                ax1.set_title("Histogram & Poligon Frekuensi")
                ax1.set_xlabel("Nilai")
                ax1.set_ylabel("Frekuensi")
                ax1.legend()
                st.pyplot(fig1)

            with col2:
                fig2, ax2 = plt.subplots()
                y_kurang = [0] + list(df_freq['Frek Kumulatif Kurang Dari (Ogiva Positif)'])
                ax2.plot(bins, y_kurang, marker='s', color='green', label='Ogiva Kurang Dari')
                
                y_lebih = list(df_freq['Frek Kumulatif Lebih Dari (Ogiva Negatif)']) + [0]
                ax2.plot(bins, y_lebih, marker='^', color='orange', label='Ogiva Lebih Dari')
                
                ax2.set_title("Kurva Ogiva (Kumulatif)")
                ax2.set_xlabel("Batas Kelas")
                ax2.set_ylabel("Frekuensi Kumulatif")
                ax2.legend()
                st.pyplot(fig2)
                
        else:
            st.error(f"Kolom '{target_col}' tidak ditemukan. Pastikan header Excel Anda benar.")
            st.info(f"Kolom yang tersedia: {', '.join(df.columns)}")

    except Exception as e:
        st.error("Gagal mengolah data.")
        print(f"Error Detail: {e}")