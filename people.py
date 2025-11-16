import os
import xml.etree.ElementTree as ET
from collections import defaultdict

# --------------------------------------------------------
# MAP: Extract names from input XML
# --------------------------------------------------------
def map_names(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    result = []
    for person in root.findall(".//person"):
        name = person.findtext("name")
        if name:
            result.append((name.strip(), 1))
    return result


# --------------------------------------------------------
# WRITE MAP OUTPUT AS XML FILE
# --------------------------------------------------------
def write_map_xml(output_file, mapped_list):
    root = ET.Element("map")

    for name, value in mapped_list:
        item = ET.SubElement(root, "item")
        name_el = ET.SubElement(item, "name")
        name_el.text = name
        value_el = ET.SubElement(item, "value")
        value_el.text = str(value)

    ET.ElementTree(root).write(output_file, encoding="utf-8", xml_declaration=True)


# --------------------------------------------------------
# SHUFFLE / GROUP
# --------------------------------------------------------
def shuffle(mapped_list):
    grouped = defaultdict(list)
    for name, value in mapped_list:
        grouped[name].append(value)
    return grouped


# --------------------------------------------------------
# REDUCE
# --------------------------------------------------------
def reduce_counts(grouped_data):
    return {name: sum(values) for name, values in grouped_data.items()}


# --------------------------------------------------------
# WRITE REDUCE OUTPUT AS XML FILE
# (Same structure as your screenshot)
# --------------------------------------------------------
def write_reduce_xml(output_file, reduced_dict):
    root = ET.Element("reduce")

    for name, value in reduced_dict.items():
        item = ET.SubElement(root, "item")
        name_el = ET.SubElement(item, "name")
        name_el.text = name
        value_el = ET.SubElement(item, "value")
        value_el.text = str(value)

    ET.ElementTree(root).write(output_file, encoding="utf-8", xml_declaration=True)


# --------------------------------------------------------
# PROCESS ONE FILE (Map → Shuffle → Reduce → XML)
# --------------------------------------------------------
def process_file(xml_file):
    base = os.path.splitext(xml_file)[0]

    mapped = map_names(xml_file)
    write_map_xml(f"map_{base}.xml", mapped)

    grouped = shuffle(mapped)
    reduced = reduce_counts(grouped)

    write_reduce_xml(f"reduce_{base}.xml", reduced)

    return reduced


# --------------------------------------------------------
# MAIN PROCESSING OF ALL FILES
# --------------------------------------------------------
if __name__ == "__main__":
    xml_files = ["people1.xml", "people2.xml", "people3.xml"]

    print("Processing XML files...")

    all_reduced = []

    # Process each file separately
    for file in xml_files:
        reduced_dict = process_file(file)
        all_reduced.append(reduced_dict)

    # MERGE REDUCES
    final_counts = defaultdict(int)
    for rd in all_reduced:
        for name, count in rd.items():
            final_counts[name] += count

    # WRITE FINAL MERGED XML
    write_reduce_xml("final_reduce.xml", final_counts)

    print("All XML files generated:")
    print(" - map_people1.xml / map_people2.xml / map_people3.xml")
    print(" - reduce_people1.xml / reduce_people2.xml / reduce_people3.xml")
    print(" - final_reduce.xml")
