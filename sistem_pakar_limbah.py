import tkinter as tk
from tkinter import messagebox

gejala_karakteristik = {
    "K1": "Mudah terbakar (Flammable) saat terkena api atau panas",
    "K2": "Bersifat korosif/dapat membuat logam berkarat atau luka bakar pada kulit",
    "K3": "Beracun (Toxic) jika terhirup, tertelan, atau kontak dengan kulit",
    "K4": "Mudah meledak (Explosive) pada tekanan/suhu tertentu",
    "K5": "Mengandung logam berat (seperti Merkuri, Timbal, Cadmium)",
    "K6": "Berupa cairan kimia pekat / konsentrat keras yang mengeluarkan uap",
    "K7": "Berupa barang elektronik yang memiliki komponen sirkuit (E-Waste)"
}

daftar_limbah = {
    "Baterai Bekas": ["K3", "K5"],
    "Lampu Neon/Bohlam": ["K5", "K2"],
    "Oli Bekas / Minyak Pelumas": ["K1", "K3"],
    "Cairan Pembersih Lantai (Kuat)": ["K2", "K6", "K3"],
    "Kemasan Aerosol (Spray/Parfum/Pewangi)": ["K1", "K4"],
    "Sisa Pestisida / Racun Serangga": ["K3", "K6", "K1"],
    "Limbah Elektronik (HP/Kabel)": ["K7", "K5"]
}

class LimbahExpertSystemApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistem Pakar: Klasifikasi Limbah B3 Rumah Tangga")
        self.root.geometry("600x500")
        self.root.configure(bg="#E8F6F3") # Soft green/teal
        self.root.resizable(False, False)
        
        self.possible_waste = list(daftar_limbah.keys())
        self.asked_characteristics = []
        self.current_char = None
        
        self.setup_ui()
        self.next_question()

    def setup_ui(self):
        header_frame = tk.Frame(self.root, bg="#117A65", pady=20)
        header_frame.pack(fill=tk.X)
        
        title = tk.Label(header_frame, text="Identifikasi Limbah B3", 
                         font=("Verdana", 18, "bold"), bg="#117A65", fg="white")
        title.pack()
        
        subtitle = tk.Label(header_frame, text="Kenali limbah berbahaya Anda agar tidak mencemari lingkungan.", 
                            font=("Verdana", 10), bg="#117A65", fg="#D1F2EB")
        subtitle.pack()

        self.content_frame = tk.Frame(self.root, bg="#E8F6F3", pady=30)
        self.content_frame.pack(fill=tk.BOTH, expand=True)

        self.question_lbl = tk.Label(self.content_frame, text="", 
                                     font=("Verdana", 13), bg="#E8F6F3", fg="#17202A",
                                     wraplength=480, justify="center")
        self.question_lbl.pack(pady=30)

        self.btn_frame = tk.Frame(self.content_frame, bg="#E8F6F3")
        self.btn_frame.pack(pady=20)

        self.btn_yes = tk.Button(self.btn_frame, text="Ya", 
                                 font=("Verdana", 12, "bold"), bg="#27AE60", fg="white", 
                                 width=12, relief=tk.FLAT, cursor="hand2",
                                 command=lambda: self.answer("ya"))
        self.btn_yes.grid(row=0, column=0, padx=15)

        self.btn_no = tk.Button(self.btn_frame, text="Tidak", 
                                font=("Verdana", 12, "bold"), bg="#E74C3C", fg="white", 
                                width=12, relief=tk.FLAT, cursor="hand2",
                                command=lambda: self.answer("tidak"))
        self.btn_no.grid(row=0, column=1, padx=15)

        # Footer
        footer_frame = tk.Frame(self.root, bg="#E8F6F3")
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=15)

        self.btn_reset = tk.Button(footer_frame, text="🔄 Diagnosa Ulang", 
                                   font=("Verdana", 10), bg="#7F8C8D", fg="white",
                                   relief=tk.FLAT, cursor="hand2", command=self.reset)
        self.btn_reset.pack()

    def next_question(self):
        # Base Case: No diseases left
        if len(self.possible_waste) == 0:
            self.show_result("Hasil: Ini sepertinya bukan Limbah B3 umum di database kami.\nAtau limbah tersebut adalah sampah domestik organik/anorganik biasa.", "#E74C3C")
            return
            
        # Base Case: Exactly 1 left
        if len(self.possible_waste) == 1:
            waste = self.possible_waste[0]
            unasked = [sym for sym in daftar_limbah[waste] if sym not in self.asked_characteristics]
            if not unasked:
                self.show_result(f"Hasil Klasifikasi:\nLimbah ini termasuk jenis:\n\n☣️ {waste}\n\n⚠️ Harap simpan terpisah dan jangan buang di tempat sampah biasa!", "#C0392B")
                return

        # Heuristic approach: Find the most common unasked characteristic
        char_counts = {}
        for waste in self.possible_waste:
            for c in daftar_limbah[waste]:
                if c not in self.asked_characteristics:
                    char_counts[c] = char_counts.get(c, 0) + 1

        if not char_counts:
            # If no characteristics left but multiple diseases match, just list them
            wastes_str = "\n".join([f"- {d}" for d in self.possible_waste])
            self.show_result(f"Kemungkinan jenis limbah:\n{wastes_str}", "#D35400")
            return

        # Sort by frequency
        best_char = sorted(char_counts.items(), key=lambda x: (-x[1], x[0]))[0][0]
        self.current_char = best_char

        nama_karakteristik = gejala_karakteristik[best_char]
        self.question_lbl.config(text=f"Apakah limbah ini memiliki sifat/karakteristik berikut:\n\n\"{nama_karakteristik}\"?", fg="#2C3E50")

    def answer(self, reply):
        self.asked_characteristics.append(self.current_char)
        
        if reply == "ya":
            self.possible_waste = [d for d in self.possible_waste if self.current_char in daftar_limbah[d]]
        else:
            self.possible_waste = [d for d in self.possible_waste if self.current_char not in daftar_limbah[d]]

        self.next_question()

    def show_result(self, text, color):
        self.question_lbl.config(text=text, fg=color, font=("Verdana", 13, "bold"))
        self.btn_yes.config(state="disabled", bg="#BDC3C7")
        self.btn_no.config(state="disabled", bg="#BDC3C7")

    def reset(self):
        self.possible_waste = list(daftar_limbah.keys())
        self.asked_characteristics = []
        self.current_char = None
        
        self.btn_yes.config(state="normal", bg="#27AE60")
        self.btn_no.config(state="normal", bg="#E74C3C")
        self.question_lbl.config(font=("Verdana", 13))
        
        self.next_question()

if __name__ == "__main__":
    root = tk.Tk()
    app = LimbahExpertSystemApp(root)
    root.mainloop()
