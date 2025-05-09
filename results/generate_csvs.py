import csv
import os
import argparse


def generate_csvs_from_text_file(input_file, output_prefix, output_dir="."):
    # Ensure the output directory exists
    if output_dir != ".":
        os.makedirs(output_dir, exist_ok=True)

    with open(input_file, "r") as file:
        current_header = None
        current_data = []
        csv_file_suffix = None
        suffix_count = {}  # Dictionary to keep track of suffix counts

        for line in file:
            line = line.strip()
            if line.startswith("BENCHMARK TABLE:"):
                # If we have a current header and data, write the previous data to a CSV
                if current_header is not None and current_data:
                    write_to_csv(
                        current_header,
                        current_data,
                        output_dir,
                        output_prefix,
                        csv_file_suffix,
                    )

                # Extract the filename suffix from the first line and replace spaces
                # with underscores
                csv_file_suffix = (
                    line.replace("BENCHMARK TABLE:", "").strip().replace(" ", "_")
                )
                # Initialize the count for this suffix if it hasn't been seen before
                if csv_file_suffix not in suffix_count:
                    suffix_count[csv_file_suffix] = 0
                else:
                    suffix_count[csv_file_suffix] += 1
                    csv_file_suffix = csv_file_suffix + str(
                        suffix_count[csv_file_suffix]
                    )

                current_header = None  # Reset header for the new table
                current_data = []  # Reset data for the new table
                continue  # Move to the next line

            if line.startswith("BENCHMARK HEADER:"):
                # Start a new header
                current_header = line.replace("BENCHMARK HEADER:", "").strip()

            elif line.startswith("BENCHMARK:") and current_header is not None:
                # Collect data lines under the current header
                data_line = line.replace("BENCHMARK:", "").strip()
                current_data.append(
                    data_line.split(",")
                )  # Assuming comma-separated values

        # Write the last header's data to a CSV if it exists
        if current_header is not None and current_data:
            write_to_csv(
                current_header, current_data, output_dir, output_prefix, csv_file_suffix
            )


def write_to_csv(header, data, output_dir, output_prefix, csv_file_suffix):
    # Extract column headers from the header line
    column_headers = header.split(",")  # Assuming the header is comma-separated
    num_columns = len(column_headers)

    # Check if data rows match the number of columns
    for row in data[:]:  # Use a copy of the list to avoid modifying while iterating
        if len(row) != num_columns:
            print(
                f"""Warning: Row {row} does not match the number of columns in header
                '{header}'. Skipping this row."""
            )
            data.remove(row)

    # Create a CSV file name based on the prefix and suffix
    csv_file_name = (
        f"{output_prefix}_{csv_file_suffix}.csv"
        if output_prefix
        else f"{csv_file_suffix}.csv"
    )
    csv_file_path = os.path.join(output_dir, csv_file_name)

    # Write data to the CSV file
    with open(csv_file_path, "w", newline="") as csvfile:
        csv_writer = csv.writer(csvfile)
        # Write the column headers as the first row
        csv_writer.writerow(column_headers)
        # Write the data rows
        csv_writer.writerows(data)

    print(f"Created CSV: {csv_file_path}")


if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(
        description="Generate CSV files from a text file with benchmark data."
    )
    parser.add_argument(
        "input_file", type=str, help="The input text file containing benchmark data."
    )
    parser.add_argument(
        "--output_prefix", type=str, help="Optional prefix for output CSV filenames."
    )

    args = parser.parse_args()

    generate_csvs_from_text_file(args.input_file, args.output_prefix)
