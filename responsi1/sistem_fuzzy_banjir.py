import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

class FuzzyFloodWarningApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistem Fuzzy: Peringatan Dini Banjir Adaptif")
        self.root.geometry("600x650")
        self.root.configure(bg="#EAF2F8") # Soft blue
        self.root.resizable(False, False)
        
        self.setup_fuzzy_system()
        self.setup_ui()

    def setup_fuzzy_system(self):
        self.tinggi_air = ctrl.Antecedent(np.arange(0, 301, 1), 'tinggi_air')
        self.curah_hujan = ctrl.Antecedent(np.arange(0, 101, 1), 'curah_hujan')
        self.laju_naik = ctrl.Antecedent(np.arange(0, 11, 1), 'laju_naik')

        self.status_siaga = ctrl.Consequent(np.arange(0, 101, 1), 'status_siaga')

        self.tinggi_air['rendah'] = fuzz.trimf(self.tinggi_air.universe, [0, 0, 150])
        self.tinggi_air['sedang'] = fuzz.trimf(self.tinggi_air.universe, [100, 175, 250])
        self.tinggi_air['tinggi'] = fuzz.trimf(self.tinggi_air.universe, [200, 300, 300])

        self.curah_hujan['ringan'] = fuzz.trimf(self.curah_hujan.universe, [0, 0, 40])
        self.curah_hujan['sedang'] = fuzz.trimf(self.curah_hujan.universe, [30, 50, 70])
        self.curah_hujan['lebat'] = fuzz.trimf(self.curah_hujan.universe, [60, 100, 100])

        self.laju_naik['lambat'] = fuzz.trimf(self.laju_naik.universe, [0, 0, 4])
        self.laju_naik['cepat'] = fuzz.trimf(self.laju_naik.universe, [2, 5, 8])
        self.laju_naik['sangat_cepat'] = fuzz.trimf(self.laju_naik.universe, [6, 10, 10])

        self.status_siaga['aman'] = fuzz.trimf(self.status_siaga.universe, [0, 0, 40])
        self.status_siaga['waspada'] = fuzz.trimf(self.status_siaga.universe, [30, 50, 70])
        self.status_siaga['bahaya'] = fuzz.trimf(self.status_siaga.universe, [60, 100, 100])

        rule1 = ctrl.Rule(self.tinggi_air['tinggi'] | self.curah_hujan['lebat'] | self.laju_naik['sangat_cepat'], self.status_siaga['bahaya'])
        rule2 = ctrl.Rule(self.tinggi_air['sedang'] & self.curah_hujan['sedang'], self.status_siaga['waspada'])
        rule3 = ctrl.Rule(self.tinggi_air['rendah'] & self.curah_hujan['ringan'] & self.laju_naik['lambat'], self.status_siaga['aman'])
        rule4 = ctrl.Rule(self.tinggi_air['sedang'] & self.laju_naik['cepat'], self.status_siaga['waspada'])
        rule5 = ctrl.Rule(self.tinggi_air['rendah'] & self.curah_hujan['lebat'], self.status_siaga['waspada'])
        
        flood_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5])
        self.flood_sim = ctrl.ControlSystemSimulation(flood_ctrl)

    def setup_ui(self):
        header_frame = tk.Frame(self.root, bg="#21618C", pady=20)
        header_frame.pack(fill=tk.X)
        
        title = tk.Label(header_frame, text="Early Warning System Banjir", 
                         font=("Verdana", 17, "bold"), bg="#21618C", fg="white")
        title.pack()
        
        subtitle = tk.Label(header_frame, text="Prediksi Status Siaga menggunakan Logika Fuzzy Mamdani", 
                            font=("Verdana", 10), bg="#21618C", fg="#D4E6F1")
        subtitle.pack()

        input_frame = tk.Frame(self.root, bg="#EAF2F8", pady=20)
        input_frame.pack(fill=tk.X, padx=30)

        tk.Label(input_frame, text="Tinggi Air (cm) [0 - 300]", bg="#EAF2F8", font=("Verdana", 10, "bold")).pack(anchor=tk.W)
        self.val_tinggi = tk.DoubleVar()
        self.slider_tinggi = tk.Scale(input_frame, from_=0, to=300, orient=tk.HORIZONTAL, 
                                      variable=self.val_tinggi, length=540, bg="#EAF2F8", troughcolor="#AED6F1")
        self.slider_tinggi.pack(pady=(0, 15))

        tk.Label(input_frame, text="Curah Hujan (mm/jam) [0 - 100]", bg="#EAF2F8", font=("Verdana", 10, "bold")).pack(anchor=tk.W)
        self.val_hujan = tk.DoubleVar()
        self.slider_hujan = tk.Scale(input_frame, from_=0, to=100, orient=tk.HORIZONTAL, 
                                     variable=self.val_hujan, length=540, bg="#EAF2F8", troughcolor="#AED6F1")
        self.slider_hujan.pack(pady=(0, 15))

        tk.Label(input_frame, text="Laju Kenaikan Air (cm/menit) [0 - 10]", bg="#EAF2F8", font=("Verdana", 10, "bold")).pack(anchor=tk.W)
        self.val_laju = tk.DoubleVar()
        self.slider_laju = tk.Scale(input_frame, from_=0, to=10, orient=tk.HORIZONTAL, 
                                    variable=self.val_laju, length=540, bg="#EAF2F8", troughcolor="#AED6F1")
        self.slider_laju.pack(pady=(0, 20))

        btn_calc = tk.Button(self.root, text="Hitung Status Siaga 🧮", 
                             font=("Verdana", 12, "bold"), bg="#E67E22", fg="white", 
                             relief=tk.FLAT, cursor="hand2", command=self.calculate_fuzzy, pady=10)
        btn_calc.pack(fill=tk.X, padx=100, pady=10)

        self.result_frame = tk.Frame(self.root, bg="#EAF2F8")
        self.result_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        self.lbl_result = tk.Label(self.result_frame, text="Nilai output akan muncul di sini", 
                                   font=("Verdana", 14), bg="#EAF2F8", fg="#34495E")
        self.lbl_result.pack(pady=10)

        self.lbl_status = tk.Label(self.result_frame, text="-", 
                                   font=("Verdana", 24, "bold"), bg="#EAF2F8", fg="#2C3E50")
        self.lbl_status.pack()

    def calculate_fuzzy(self):
        t = self.val_tinggi.get()
        h = self.val_hujan.get()
        l = self.val_laju.get()

        try:
            self.flood_sim.input['tinggi_air'] = t
            self.flood_sim.input['curah_hujan'] = h
            self.flood_sim.input['laju_naik'] = l
            
            self.flood_sim.compute()
            output_val = self.flood_sim.output['status_siaga']
            
            if output_val < 35:
                status_str = "AMAN 🟢"
                color = "#27AE60"
            elif output_val < 65:
                status_str = "WASPADA 🟡"
                color = "#F39C12"
            else:
                status_str = "BAHAYA / EVAKUASI 🔴"
                color = "#C0392B"

            self.lbl_result.config(text=f"Tingkat Bahaya : {output_val:.2f}%")
            self.lbl_status.config(text=status_str, fg=color)

        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan komputasi: {str(e)}")

    def show_graph(self):
        self.status_siaga.view(sim=self.flood_sim)

if __name__ == "__main__":
    root = tk.Tk()
    app = FuzzyFloodWarningApp(root)
    root.mainloop()
