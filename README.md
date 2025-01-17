# Skin Ontology Tool

## Overview
The **Skin Ontology Tool** is a utility tool designed to assist in translating dermatology datasets to ICD-10 and ICD-11 codes. The tool processes input data, matches labels to their corresponding ICD codes, and allows users to specify different levels of granularity for the output. It is particularly useful for standardizing dermatology datasets, ensuring compatibility with ICD-based systems and combining existing datasets together.

## Features
- **ICD Code Translation**:
  - Map dataset labels to ICD-10 and ICD-11 codes.
  - Support for hierarchical ICD-10 ontology structure.
- **Granularity Levels**:
  - Level 1: Broad category range (e.g., `L00-L08`).
  - Level 2: Specific category (e.g., `L01`).
  - Level 3: Detailed subcategory (e.g., `L01.1`).
- **Unmatched Label Tracking**:
  - Identify and log unmatched dataset labels.
- **Customizable Processing**:
  - Option to process only unmatched rows with missing or placeholder (`tbd`) ICD values.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/skin_ontology_tool.git
   cd skin_ontology_tool
   ```
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
The tool is executed via the command line and supports several options:

### Command-Line Arguments
- `--input` (required): Path to the input CSV file containing the dataset.
- `--data` (required): Path to the folder containing ICD mapping datasets (JSON or CSV).
- `--output` (required): Path to the folder where the translated dataset will be saved.
- `--granularity`: Level of granularity for ICD codes (1: range, 2: category, 3: subcategory).
- `--only-unmatched`: Process only rows with missing or placeholder (`tbd`) ICD values.

### Example Command
```bash
python skin_ontology_tool.py --input datasets/dermatology.csv \
                             --data icd_mappings/ \
                             --output results/ \
                             --granularity 2 \
                             --only-unmatched
```

### Input File Format
The input CSV file must contain a column named `label_to_icd` with labels to be matched to ICD codes. Example:

| label_to_icd            | icd10  | icd11  |
|-------------------------|--------|--------|
| Impetigo               | tbd    | tbd    |
| Cutaneous abscess      | L02    | NA     |

### Output Files
1. **Translated CSV**: The input dataset with added ICD-10 and ICD-11 columns populated.
2. **Unmatched Labels**: A text file listing labels that could not be matched.

### Example Output
**Translated CSV**:
| label_to_icd            | icd10  | icd11  |
|-------------------------|--------|--------|
| Impetigo               | L01    | L01.0  |
| Cutaneous abscess      | L02    | NA     |

**Unmatched Labels**:
```
Unmatched labels saved to results/unmatched_labels.txt
```

## Developer Guide

### Hierarchical Parsing
The tool supports ICD-10 ontology in JSON format. Example structure:
```json
{
  "code": "L00-L08",
  "description": "Infections of the skin and subcutaneous tissue",
  "subcategory": [
    {
      "code": "L01",
      "description": "Impetigo",
      "subcategory": [
        {
          "code": "L01.1",
          "description": "Impetiginization of other dermatoses"
        }
      ]
    }
  ]
}
```
A json containing dermatology related icd code is provided in the data folder. 

### Adding New Data
Place new ICD mapping files in the specified `--data` folder. Supported formats:
- **JSON**: For hierarchical ontologies.
- **CSV**: For flat mappings (must include `label`, `icd10`, and `icd11` columns).

## Future Features
- **ICD-11 Hierarchical Support**: Extend hierarchical parsing to ICD-11 ontology.
- **Python package**

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature/fix.
3. Submit a pull request.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

