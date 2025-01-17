import argparse
from .translator import translate_dataset
from .utils import create_folder_if_not_exists

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Translate skin datasets to ICD-10 with granularity.")
    parser.add_argument('--input', required=True, help="Path to the input CSV file.")
    parser.add_argument('--data', required=True, help="Path to the folder containing ICD mapping datasets.")
    parser.add_argument('--output', required=True, help="Path to the output folder.")
    parser.add_argument('--granularity', type=int, help="Level of granularity for ICD codes (1: range, 2: category, 3: subcategory).")
    parser.add_argument('--only-unmatched', action='store_true', help="Only process rows with missing or 'tbd' ICD values.")
    args = parser.parse_args()

    create_folder_if_not_exists(args.output)
    translate_dataset(args.input, args.data, args.output, args.granularity, args.only_unmatched)


if __name__ == '__main__':
    main()