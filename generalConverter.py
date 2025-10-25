import sys
import os
import FreeCAD
import Part
import Mesh

# --- Validazione Input ---
if len(sys.argv) < 4:
    print("Errore: mancano gli argomenti.")
    # MODIFICA: Testo d'aiuto reso generico
    print("Uso: freecadcmd <script.py> <file_input_cad> <file_output.obj> [tolleranza]")
    sys.exit(1)

input_file = sys.argv[2]
output_file = sys.argv[3]

# --- Parametro Opzionale: Tolleranza ---
tolerance = 0.1
if len(sys.argv) > 4:
    try:
        tolerance = float(sys.argv[4])
    except ValueError:
        print(f"Errore: la tolleranza '{sys.argv[4]}' non è un numero valido.")
        sys.exit(1)

print(f"Avvio conversione...")
print(f"  File Input: {input_file}")
print(f"  File Output: {output_file}")
print(f"  Tolleranza (deviazione): {tolerance} mm")

# --- 1. Caricamento del file CAD ---
# Part.read() supporta .step, .iges, .brep e altri.
try:
    shape = Part.read(input_file)
    if shape.isNull():
        print("\nErrore: Il file è stato letto, ma la forma caricata è 'nulla'.")
        print("Il file potrebbe essere corrotto o non supportato.")
        sys.exit(1)
except Exception as e:
    print(f"Errore critico durante la lettura del file CAD: {e}")
    sys.exit(1)

# --- 2. Tessellazione (Conversione da CAD a Mesh) ---
mesh = Mesh.Mesh()
try:
    mesh.addFacets(shape.tessellate(tolerance))
except Exception as e:
    print(f"Errore critico durante la tessellazione (calcolo mesh): {e}")
    sys.exit(1)

# --- CONTROLLO DI SICUREZZA ---
if mesh.CountFacets == 0:
    print("\nErrore: La mesh generata è vuota (0 triangoli).")
    print("Possibili cause:")
    print("  1. Il file di input è vuoto o contiene solo elementi 2D/wireframe.")
    print("  2. La geometria nel file di input è corrotta o non valida.")
    sys.exit(1)
else:
    # Messaggio spostato nel riepilogo finale
    pass

# --- 3. Esportazione in .obj ---
try:
    mesh.write(output_file, "OBJ")
    
    print("\nSuccesso!")
    print(f"File convertito e salvato in: {output_file}")

    # --- MODIFICA: Aggiunto riepilogo (con estensione file dinamica) ---
    input_ext = os.path.splitext(input_file)[1] # Estrae l'estensione (es: .step)
    
    print("\n--- Riepilogo della Conversione ---")
    print(f"  Modello Input ({input_ext}):  Matematico (B-Rep)")
    print(f"  Modello Output (.obj):  Mesh Poligonale")
    print("-----------------------------------")
    print(f"  Poligoni (triangoli) creati: {mesh.CountFacets}")
    print(f"  Vertici creati:              {mesh.CountPoints}")
    print("-----------------------------------")

except Exception as e:
    print(f"Errore critico durante l'esportazione del file OBJ: {e}")
    sys.exit(1)

sys.exit(0)

