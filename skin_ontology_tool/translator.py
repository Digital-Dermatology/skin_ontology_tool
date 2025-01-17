import csv
import os
import pandas as pd
import json

def translate_dataset(input_csv, data_folder, output_folder, granularity_level=None, only_unmatched=False):
    """
    Translate an input dataset to include ICD-10 and ICD-11 mappings with specified granularity.

    Args:
        input_csv (str): Path to the input CSV file.
        data_folder (str): Path to the folder containing existing ICD mapping datasets or JSON.
        output_folder (str): Path to the output folder to save results.
        granularity_level (int): Level of granularity for ICD-10 codes (e.g., 1 for "L00-L08", 2 for "L01", 3 for "L01.1").
        only_unmatched (bool): If True, only process rows with 'tbd', NaN, or None in ICD columns.
    """
    icd_mapping = load_icd_mappings(data_folder)
    unmatched_labels = []

    # Load input CSV into a DataFrame for easier processing
    df = pd.read_csv(input_csv)

    # If processing only unmatched rows, filter for rows where ICD columns are missing or "tbd"
    if only_unmatched:
        condition = (df['icd10'].isna() | df['icd11'].isna() | (df['icd10'] == 'tbd') | (df['icd11'] == 'tbd'))
        rows_to_process = df[condition]
    else:
        rows_to_process = df

    # Process each row to find ICD mappings
    for idx, row in rows_to_process.iterrows():
        label = row.get('label_to_icd', '').strip()
        if label in icd_mapping:
            icd10 = apply_granularity(icd_mapping[label], granularity_level)
            df.at[idx, 'icd10'] = icd10
        else:
            df.at[idx, 'icd10'] = 'tbd'
            unmatched_labels.append(label)

    # Write the translated output file
    output_csv = os.path.join(output_folder, 'translated_' + os.path.basename(input_csv))
    df.to_csv(output_csv, index=False)

    # Write the unmatched labels to a text file
    unmatched_txt = os.path.join(output_folder, 'unmatched_labels.txt')
    with open(unmatched_txt, 'w') as txtfile:
        for label in unmatched_labels:
            txtfile.write(label + '\n')

    print(f"Translation complete. Output saved to {output_csv}. Unmatched labels saved to {unmatched_txt}.")


def load_icd_mappings(data_folder):
    """
    Load existing ICD mappings from the data folder or JSON.

    Args:
        data_folder (str): Path to the folder containing ICD mappings.

    Returns:
        dict: A dictionary mapping labels to a list of hierarchical ICD codes.
    """
    icd_mapping = {}

    # Process JSON files for hierarchical ICD structure
    for file in os.listdir(data_folder):
        if file.endswith('.json'):
            with open(os.path.join(data_folder, file), 'r') as jsonfile:
                ontology = json.load(jsonfile)
                parse_icd_json(ontology, icd_mapping)

    return icd_mapping


def parse_icd_json(node, icd_mapping, parent_codes=[]):
    """
    Recursively parse an ICD JSON structure to extract hierarchical mappings.

    Args:
        node (dict): Current node of the JSON tree.
        icd_mapping (dict): Dictionary to store mappings.
        parent_codes (list): List of codes from the parent nodes.
    """
    current_code = node.get("code", "")
    description = node.get("description", "")
    subcategories = node.get("subcategory", [])

    if description:
        # Store the hierarchy of codes for this description
        full_hierarchy = parent_codes + [current_code]
        icd_mapping[description] = full_hierarchy

    # Recurse into subcategories
    for subcategory in subcategories:
        parse_icd_json(subcategory, icd_mapping, parent_codes + [current_code])


def apply_granularity(hierarchy, granularity_level):
    """
    Adjust ICD code output to the specified granularity level.

    Args:
        hierarchy (list): Hierarchical list of ICD codes for a description.
        granularity_level (int): Desired granularity level (e.g., 1, 2, 3).

    Returns:
        str: ICD code truncated to the desired granularity level.
    """
    if granularity_level is None:
        return '-'.join(hierarchy)  # Default to the full hierarchy
    if granularity_level <= len(hierarchy):
        return '-'.join(hierarchy[:granularity_level])
    return '-'.join(hierarchy)  # If granularity exceeds depth, return the deepest level