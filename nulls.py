import xml.etree.ElementTree as ET

def detectar_huecos(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    errores = []

    for person in root.findall(".//person"):
        raw_name = person.findtext("name")

        if raw_name is None:
            errores.append(("VACÍO", "El campo <name> está ausente"))
            continue

        name = raw_name

        # Check 1: leading/trailing spaces
        if name != name.strip():
            errores.append((raw_name, "Espacios al inicio o al final"))

        # Check 2: multiple spaces inside
        if "  " in name:
            errores.append((raw_name, "Dos o más espacios seguidos"))

        # Check 3: empty or whitespace only
        if name.strip() == "":
            errores.append((raw_name, "Nombre vacío o solo espacios"))

    return errores


# -----------------------------
# EJEMPLO DE USO
# -----------------------------
if __name__ == "__main__":
    xml_files = ["people1.xml", "people2.xml", "people3.xml"]

    for file in xml_files:
        print(f"\nAnalizando {file}...")
        resultado = detectar_huecos(file)

        if not resultado:
            print("✔ No nulls.")
        else:
            print("⚠ Errores detectados:")
            for nombre, descripcion in resultado:
                print(f" - '{nombre}' → {descripcion}")
