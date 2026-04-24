from flask import Flask, render_template, request, jsonify
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

app = Flask(__name__)

gejala_karakteristik = {
    "K1": "Mudah terbakar (Flammable) saat didekatkan sumber api/panas?",
    "K2": "Bersifat korosif/dapat membuat material logam berkarat atau luka bakar pada kulit?",
    "K3": "Beracun (Toxic) jika terhirup, tertelan, atau kontak dengan tubuh?",
    "K4": "Mudah meledak (Explosive) pada tekanan atau suhu tertentu?",
    "K5": "Mengandung logam berat (seperti Merkuri, Timbal, Cadmium dll)?",
    "K6": "Berupa cairan kimia pekat / konsentrat keras yang mengeluarkan uap menyengat?",
    "K7": "Berupa barang elektronik mati yang memiliki komponen sirkuit (E-Waste)?"
}

daftar_limbah = {
    "Baterai Bekas": ["K3", "K5"],
    "Lampu Neon/Bohlam": ["K5", "K2"],
    "Oli Bekas / Minyak Pelumas": ["K1", "K3"],
    "Cairan Pembersih Lantai (Kuat)": ["K2", "K6", "K3"],
    "Kemasan Aerosol (Spray/Parfum/Pewangi)": ["K1", "K4"],
    "Sisa Pestisida / Racun Serangga": ["K3", "K6", "K1"],
    "Limbah Elektronik (Kabel/HP Bekas)": ["K7", "K5"]
}

def get_next_pakar_question(possible_waste, asked_characteristics):
    if len(possible_waste) == 0:
        return {"status": "done", "result": "Bukan Limbah B3 Umum / Sampah Organik Biasa"}
    
    if len(possible_waste) == 1:
        waste = possible_waste[0]
        unasked = [sym for sym in daftar_limbah[waste] if sym not in asked_characteristics]
        if not unasked:
            return {"status": "done", "result": waste}

    char_counts = {}
    for waste in possible_waste:
        for c in daftar_limbah[waste]:
            if c not in asked_characteristics:
                char_counts[c] = char_counts.get(c, 0) + 1

    if not char_counts:
        return {"status": "done", "result": "Campuran " + " / ".join(possible_waste)}

    best_char = sorted(char_counts.items(), key=lambda x: (-x[1], x[0]))[0][0]
    return {
        "status": "question",
        "kode": best_char,
        "pertanyaan": gejala_karakteristik[best_char],
        "possible_waste": possible_waste,
        "asked_characteristics": asked_characteristics
    }


tinggi_air = ctrl.Antecedent(np.arange(0, 301, 1), 'tinggi_air')
curah_hujan = ctrl.Antecedent(np.arange(0, 101, 1), 'curah_hujan')
laju_naik = ctrl.Antecedent(np.arange(0, 11, 1), 'laju_naik')
status_siaga = ctrl.Consequent(np.arange(0, 101, 1), 'status_siaga')

tinggi_air['rendah'] = fuzz.trimf(tinggi_air.universe, [0, 0, 150])
tinggi_air['sedang'] = fuzz.trimf(tinggi_air.universe, [100, 175, 250])
tinggi_air['tinggi'] = fuzz.trimf(tinggi_air.universe, [200, 300, 300])

curah_hujan['ringan'] = fuzz.trimf(curah_hujan.universe, [0, 0, 40])
curah_hujan['sedang'] = fuzz.trimf(curah_hujan.universe, [30, 50, 70])
curah_hujan['lebat'] = fuzz.trimf(curah_hujan.universe, [60, 100, 100])

laju_naik['lambat'] = fuzz.trimf(laju_naik.universe, [0, 0, 4])
laju_naik['cepat'] = fuzz.trimf(laju_naik.universe, [2, 5, 8])
laju_naik['sangat_cepat'] = fuzz.trimf(laju_naik.universe, [6, 10, 10])

status_siaga['aman'] = fuzz.trimf(status_siaga.universe, [0, 0, 40])
status_siaga['waspada'] = fuzz.trimf(status_siaga.universe, [30, 50, 70])
status_siaga['bahaya'] = fuzz.trimf(status_siaga.universe, [60, 100, 100])

# Aturan (Mamdani)
rule1 = ctrl.Rule(tinggi_air['tinggi'] | curah_hujan['lebat'] | laju_naik['sangat_cepat'], status_siaga['bahaya'])
rule2 = ctrl.Rule(tinggi_air['sedang'] & curah_hujan['sedang'], status_siaga['waspada'])
rule3 = ctrl.Rule(tinggi_air['rendah'] & curah_hujan['ringan'] & laju_naik['lambat'], status_siaga['aman'])
rule4 = ctrl.Rule(tinggi_air['sedang'] & laju_naik['cepat'], status_siaga['waspada'])
rule5 = ctrl.Rule(tinggi_air['rendah'] & curah_hujan['lebat'], status_siaga['waspada'])

flood_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5])
flood_sim = ctrl.ControlSystemSimulation(flood_ctrl)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/pakar")
def pakar_page():
    return render_template("pakar.html")

@app.route("/fuzzy")
def fuzzy_page():
    return render_template("fuzzy.html")

# API Endpoints
@app.route("/api/pakar", methods=["POST"])
def api_pakar():
    data = request.json
    action = data.get("action")
    
    if action == "start":
        pw = list(daftar_limbah.keys())
        ac = []
        return jsonify(get_next_pakar_question(pw, ac))
    
    elif action == "answer":
        pw = data.get("possible_waste", [])
        ac = data.get("asked_characteristics", [])
        reply = data.get("reply") # 'ya' or 'tidak'
        current_char = data.get("current_char")
        
        ac.append(current_char)
        if reply == "ya":
            pw = [d for d in pw if current_char in daftar_limbah[d]]
        else:
            pw = [d for d in pw if current_char not in daftar_limbah[d]]
            
        return jsonify(get_next_pakar_question(pw, ac))

@app.route("/api/fuzzy", methods=["POST"])
def api_fuzzy():
    try:
        data = request.json
        flood_sim.input['tinggi_air'] = float(data.get("tinggi", 0))
        flood_sim.input['curah_hujan'] = float(data.get("hujan", 0))
        flood_sim.input['laju_naik'] = float(data.get("laju", 0))
        
        flood_sim.compute()
        output_val = flood_sim.output['status_siaga']
        
        if output_val < 35:
            status_text = "Status: AMAN"
            level = 1
        elif output_val < 65:
            status_text = "Status: WASPADA"
            level = 2
        else:
            status_text = "Status: BAHAYA (EVAKUASI)"
            level = 3
            
        return jsonify({
            "success": True,
            "score": round(output_val, 2),
            "status": status_text,
            "level": level
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == "__main__":
    app.run(debug=True, port=8080)
