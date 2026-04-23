# AI Portal Responsi - Sistem Cerdas Terpadu

Proyek ini adalah bentuk implementasi **Sistem Kecerdasan Buatan (Artifical Intelligence)** berbasis antarmuka Web Modern (HTML/CSS/JS di sisi *Frontend* dan Python Flask di sisi *Backend*). 

Proyek ini mendemonstrasikan dua jenis penerapan AI untuk pengambilan keputusan secara *real-time*: **Sistem Pakar** dan **Logika Fuzzy**.

---

## 1. Penjelasan Sistem Pakar (Klasifikasi Limbah B3)

Sistem Pakar (*Expert System*) ini difungsikan layaknya seorang pakar lingkungan untuk membantu pengguna mengidentifikasi jenis Sampah/Limbah B3 (Bahan Berbahaya Beracun) yang umum ada di rumah tangga.

*   **Metode:** *Forward Chaining* dipadukan dengan algortima *Knowledge-Based Elimination* (Eliminasi Heuristik).
*   **Cara Kerja:**
    Sistem tidak sekadar bertanya secara statis dari atas ke bawah. Sistem secara cerdas akan mengekstrak semua kemungkinan ciri limbah dari *Database/Rule Base*, lalu mencari karakteristik mana yang paling relevan untuk ditanyakan. 
    Jawaban "Ya" atau "Tidak" akan memengaruhi basis probabilitas, mengeliminasi limbah yang tidak masuk kriteria di memori, hingga menyisakan **1 hasil limbah akhir** secara instan.
*   **Manfaat/Urgensi:** Mencegah terjadinya keracunan, meledaknya sampah rumah tangga, atau pencemaran tanah berat akibat salah penanganan limbah korosif atau beracun.

## 2. Penjelasan Sistem Fuzzy (Peringatan Dini Banjir)

Sistem ini digunakan sebagai peredam ketidakpastian (*ambiguity*) dalam memproyeksikan kapan status status darurat/bahaya banjir harus diturunkan.

*   **Metode:** Inferensi Logika Fuzzy **Mamdani** menggunakan *framework* Python `scikit-fuzzy`.
*   **Cara Kerja:**
    Sistem memadukan komputasi 3 sensor sensorik simultan:
    1.  Tinggi Air (cm)
    2.  Curah Hujan (mm/jam)
    3.  Laju Kenaikan Air (cm/menit)
    
    Nilai crisp/numerik dari sensor tersebut akan difuzzifikasi, lalu diproses masuk ke dalam *Rule Base* (contoh: *Jika Hujan Lebat DAN Tinggi Air Sedang, maka WASPADA*), dan didefuzzifikasi menggunakan strategi rata-rata *(Centroid/COG)* untuk memperoleh satu status level pasti: **Aman (🟢), Waspada (🟡), atau Bahaya (🔴)**.
*   **Manfaat/Urgensi:** Mengatasi keterbatasan alarm konvensional yang hanya mendeteksi tinggi air. Sistem ini adaptif mendeteksi risiko banjir *bandang* atau hujan kiriman jauh lebih awal (*Golden Hour* untuk evakuasi).

---

## Arsitektur Aplikasi Terpadu (Persatuan Sistem)

Meskipun logika dasar dari Sistem Pakar dan Logika Fuzzy dijalankan oleh modul Python yang berbeda secara fondasi, keduanya secara elegan **dipersatukan di bawah satu payung kerangka kerja (Web Framework) yaitu Flask**.

1. **Routing Tunggal (`app.py`)**: Bertindak sebagai *server* terpusat yang menaungi *engine* probabilitas Fuzzy di satu *endpoint* (`/api/fuzzy`), sekaligus menaungi logika rekursif eliminasi Sistem Pakar di *endpoint* lainnya (`/api/pakar`).
2. **Asynchronous (Tanpa Refresh Laman)**: Kedua jenis sistem di *frontend* (dibangun dengan desain Glassmorphism Modern) didesain agar terus berkorespondensi langsung dengan Python *backend* secara *real-time* via `AJAX/Fetch API`. Pengguna dapat menikmati kekuatan kedua sistem canggih tersebut dalam satu dasbor Portal AI yang mulus tanpa sedikitpun jeda *loading* lambat.

## 🚀 Cara Menjalankan (Run)
1. Buka Terminal / CMD dan arahkan ke folder ini (`cd c:\prakkb\responsi1`).
2. Install requirement dengan `pip install flask scikit-fuzzy numpy`.
3. Jalankan server dengan perintah `python app.py`.
4. Buka Browser (Chrome/Edge) ke `http://localhost:8080`.
