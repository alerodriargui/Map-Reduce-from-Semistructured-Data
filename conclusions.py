import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt

def load_final_reduce(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    counts = {}
    for item in root.findall("item"):
        name = item.findtext("name")
        value = int(item.findtext("value"))
        counts[name] = value

    return counts

def conclusions(counts):
    total_unique = len(counts)
    most_frequent_name = max(counts, key=counts.get)
    most_frequent_value = counts[most_frequent_name]

    # Nombres que aparecen solo 1 vez
    rare_names = [name for name, v in counts.items() if v == 1]

    # Filtrar nombres que aparecen más de 1 vez
    filtered_counts = {name: v for name, v in counts.items() if v > 1}

    # Ordenar por frecuencia
    sorted_counts = dict(sorted(filtered_counts.items(), key=lambda x: x[1], reverse=True))

    # Preparar datos para el gráfico
    labels = list(sorted_counts.keys()) + ["1-time names"]
    values = list(sorted_counts.values()) + [len(rare_names)]

    # ======= PLOT BAR CHART =======
    plt.figure(figsize=(12,6))
    plt.bar(labels, values, color='skyblue')
    plt.xticks(rotation=45, ha='right')
    plt.ylabel("Occurrences")
    plt.title("Name Frequencies (including single occurrences as last column)")
    plt.tight_layout()
    plt.show()

    # ======= PRINT SUMMARY =======
    print("\n==============================")
    print("        CONCLUSIONS")
    print("==============================\n")
    print(f"✔ Total unique names: {total_unique}")
    print(f"✔ Most frequent name: {most_frequent_name} ({most_frequent_value} occurrences)")
    print(f"✔ Names that appear only once: {len(rare_names)}")
    print("\nTop 10 most frequent names:")
    top_10 = list(sorted_counts.items())[:10]
    for name, value in top_10:
        print(f"  - {name}: {value}")


if __name__ == "__main__":
    final_file = "final_reduce.xml"
    counts = load_final_reduce(final_file)
    conclusions(counts)
