import os
import csv
from skin_ontology_tool.translator import translate_dataset, load_icd_mappings

def test_translation():
    # Setup test environment
    test_input = 'test_input.csv'
    test_data = 'test_data'
    test_output = 'test_output'

    os.makedirs(test_data, exist_ok=True)
    os.makedirs(test_output, exist_ok=True)

    # Create a sample input CSV
    with open(test_input, 'w', newline='') as infile:
        writer = csv.DictWriter(infile, fieldnames=['label_to_icd', 'other_field'])
        writer.writeheader()
        writer.writerows([
            {'label_to_icd': 'eczema', 'other_field': 'value1'},
            {'label_to_icd': 'psoriasis', 'other_field': 'value2'},
        ])

    # Create a sample ICD mapping CSV
    with open(os.path.join(test_data, 'icd_mappings.csv'), 'w', newline='') as datafile:
        writer = csv.DictWriter(datafile, fieldnames=['label', 'icd10', 'icd11'])
        writer.writeheader()
        writer.writerows([
            {'label': 'eczema', 'icd10': 'L20', 'icd11': 'EA80'},
        ])

    # Run the translator
    translate_dataset(test_input, test_data, test_output)

    # Check output files
    translated_file = os.path.join(test_output, 'translated_' + os.path.basename(test_input))
    assert os.path.exists(translated_file)

    with open(translated_file, 'r') as outfile:
        rows = list(csv.DictReader(outfile))
        assert rows[0]['icd10'] == 'L20'
        assert rows[1]['icd10'] == 'tbd'

    unmatched_file = os.path.join(test_output, 'unmatched_labels.txt')
    assert os.path.exists(unmatched_file)

    with open(unmatched_file, 'r') as unmatched:
        assert unmatched.read().strip() == 'psoriasis'

    # Cleanup
    os.remove(test_input)
    os.remove(os.path.join(test_data, 'icd_mappings.csv'))
    os.rmdir(test_data)
    for file in os.listdir(test_output):
        os.remove(os.path.join(test_output, file))
    os.rmdir(test_output)

if __name__ == '__main__':
    test_translation()