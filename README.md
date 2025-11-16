# Map-Reduce from Semistructured Data

This repository contains a workflow for processing semi-structured data using Python, based on a MapReduce approach. The project allows you to clean, process, and generate conclusions from an XML file.

## Main Files

1. **nulls.py**  
    This script cleans the data, removing null or inconsistent values ​​from the input file. It must be run first to prepare the data.

2. **people.py**  
    It processes the cleaned data and counts the people's names. It generates an intermediate file ready for final analysis.

3. **conclusions.py**  
    It takes the file processed by `people.py` and generates statistical conclusions, such as:

      - Total number of unique names.

      - Most frequent name and its number of occurrences.

      - Names that appear only once.

      - Top 10 most frequent names.

   It also includes data visualizations using bar or pie charts.

## Execution guide

1. Run the cleanup script:

```bash
python nulls.py
```
2. Run the processing script:

```bash
python people.py
```

3. Run the conclusions script:

```bash
python conclusions.py
```