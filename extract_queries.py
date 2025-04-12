import json
import os

# --- Configuration ---
# *** IMPORTANT: Update this to the JSON file containing the generated answers ***
input_json_file = './extracted/answer_examples_output.json'
output_txt_file = './extracted/extracted_govern_with_answers.txt' # Renamed output to avoid overwriting
fields_to_extract = [
    'title',         # Assuming type/category are not in generated_answers.json
    'queries',       # Renamed from 'query' to match generated_answers.json
    'validator',
    'valid_answers',  # New field
    'invalid_answer', # New field
    'invalid_reason'  # New field
    ]
# ---------------------

def extract_data(input_file, output_file, fields):
    """
    Reads a JSON file containing policy sections enriched with answers,
    extracts specified fields, and writes them to a plain text file.

    Args:
        input_file (str): Path to the input JSON file (e.g., generated_answers.json).
        output_file (str): Path to the output text file.
        fields (list): A list of strings representing the keys to extract.
    """
    print(f"Attempting to read JSON data from: {input_file}")

    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"❌ Error: Input file not found at '{input_file}'")
        return

    try:
        # Read the JSON data from the file
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Ensure the data is a list
        if not isinstance(data, list):
            print(f"❌ Error: Expected a JSON list (array) in '{input_file}', but found {type(data)}.")
            return

        print(f"✅ Successfully read {len(data)} entries from JSON file.")

        # Open the output text file for writing
        with open(output_file, 'w', encoding='utf-8') as outfile:
            print(f"Writing extracted data to: {output_file}")

            # Process each item in the JSON list
            for index, item in enumerate(data):
                outfile.write(f"--- Entry {index + 1} ---\n")

                # Extract and write each specified field
                for field in fields:
                    # Use .get() for safety if a field might be missing in some entries
                    value = item.get(field, 'N/A')

                    # Capitalize the field name for better readability in the output file
                    field_name_capitalized = ' '.join(word.capitalize() for word in field.split('_'))

                    # Special handling for list fields ('queries', 'valid_answers')
                    if field == 'queries' and isinstance(value, list):
                        outfile.write(f"{field_name_capitalized}:\n")
                        if value:
                            for q_idx, query_text in enumerate(value):
                                outfile.write(f"  - Q{q_idx + 1}: {query_text}\n")
                        else:
                           outfile.write("  (No queries listed)\n")
                    elif field == 'valid_answers' and isinstance(value, list):
                        outfile.write(f"{field_name_capitalized}:\n")
                        if value:
                            for va_idx, va_text in enumerate(value):
                                # Indent multi-line answers for better readability
                                formatted_va = "\n    ".join(str(va_text).splitlines()) # Ensure text is string
                                outfile.write(f"  - VA{va_idx + 1}: {formatted_va}\n")
                        else:
                            outfile.write("  (No valid answers listed)\n")
                    else:
                        # Default handling for simple string fields
                        # Indent multi-line strings for validator/reason for better readability
                        if isinstance(value, str) and '\n' in value:
                             formatted_value = "\n    ".join(value.splitlines())
                             outfile.write(f"{field_name_capitalized}:\n    {formatted_value}\n")
                        else:
                             outfile.write(f"{field_name_capitalized}: {value}\n")


                # Add a separator between entries
                outfile.write("\n" + "="*40 + "\n\n")

        print(f"✅ Extraction complete. Data saved to '{output_file}'.")

    except json.JSONDecodeError as e:
        print(f"❌ Error decoding JSON from '{input_file}': {e}")
    except IOError as e:
        print(f"❌ Error reading from '{input_file}' or writing to '{output_file}': {e}")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")

# --- Run the extraction ---
if __name__ == "__main__":
    # Ensure the input file is the one containing the answers
    if not input_json_file.endswith('generated_answers.json'):
         print(f"⚠️ Warning: Input file is set to '{input_json_file}'.")
         print(f"   Make sure this file contains the 'valid_answers', 'invalid_answer', and 'invalid_reason' fields.")
         user_confirm = input("   Continue? (y/n): ")
         if user_confirm.lower() != 'y':
              print("Aborting.")
              exit()

    extract_data(input_json_file, output_txt_file, fields_to_extract)