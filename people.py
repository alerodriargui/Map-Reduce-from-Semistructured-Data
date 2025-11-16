import os
import xml.etree.ElementTree as ET
from collections import defaultdict

# ----------------------
# MAP FUNCTION
# ----------------------
def map_names(xml_file):
    """
    Reads an XML file with <person><name>...</name></person> elements
    and emits (name, 1) for each person.
    Returns a list of tuples (name, 1).
    """
    tree = ET.parse(xml_file)
    root = tree.getroot()

    results = []
    for person in root.findall(".//person"):
        name = person.findtext("name")
        if name:
            results.append((name.strip(), 1))

    return results


# ----------------------
# SHUFFLE FUNCTION
# ----------------------
def shuffle(mapped_data):
    """
    Groups the mapped results by key (name).
    Input: list of (name, 1)
    Output: dict { name: [1,1,1...] }
    """
    grouped = defaultdict(list)
    for key, value in mapped_data:
        grouped[key].append(value)
    return grouped


# ----------------------
# REDUCE FUNCTION
# ----------------------
def reduce_counts(grouped_data):
    """
    Sums all counts for each name.
    Input: dict { name: [1,1,1] }
    Output: dict { name: total }
    """
    reduced = {}
    for name, values in grouped_data.items():
        reduced[name] = sum(values)
    return reduced


# ----------------------
# PIPELINE FOR ONE FILE
# ----------------------
def process_file(xml_file):
    """
    Executes Map → Shuffle → Reduce for a single XML file.
    Returns the reduced output.
    """
    print(f"Processing {xml_file}...")

    mapped = map_names(xml_file)
    grouped = shuffle(mapped)
    reduced = reduce_counts(grouped)

    return mapped, grouped, reduced


# ----------------------
# MAIN PIPELINE
# ----------------------
def process_all_files(xml_files):
    all_reduced = []

    for xml_file in xml_files:
        mapped, grouped, reduced = process_file(xml_file)

        print(f"\n--- MAP OUTPUT for {xml_file} ---")
        print(mapped)

        print(f"\n--- GROUPED (SHUFFLE) OUTPUT---")
        print(grouped)

        print(f"\n--- REDUCE OUTPUT ---")
        print(reduced)

        all_reduced.append(reduced)

    # FINAL MERGE OF ALL REDUCERS
    final_counts = defaultdict(int)
    for reduced_dict in all_reduced:
        for name, count in reduced_dict.items():
            final_counts[name] += count

    return final_counts


# ----------------------
# EXECUTION
# ----------------------
if __name__ == "__main__":

    xml_files = ["people1.xml", "people2.xml", "people3.xml"]

    final_result = process_all_files(xml_files)

    print("\n======================")
    print("FINAL MERGED COUNTS")
    print("======================")
    for name, count in final_result.items():
        print(f"{name}: {count}")
