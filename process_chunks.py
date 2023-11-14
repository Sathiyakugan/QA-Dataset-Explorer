import json
import pandas as pd
import csv


def extract_document_title(document_text):
    """
    Extracts the document title from the document text.

    The title is assumed to be within the first <H1> tag in the document text.

    :param document_text: Document text containing HTML-like tags.
    :return: Extracted document title or "Unknown Title" if not found.
    """
    try:
        first_heading = document_text.split('<H1>')[1].split('</H1>')[0].strip()
        return first_heading
    except IndexError:
        return "Unknown Title"


def process_chunk(chunk, output_csv, mode, header, max_short_answers):
    """
    Processes a chunk of data and writes it to a CSV file.

    Each line in the chunk is parsed as JSON, and relevant fields are extracted
    and formatted. The data is then written to a CSV file.

    :param chunk: List of JSON strings representing the data chunk.
    :param output_csv: File path for the output CSV file.
    :param mode: File mode for writing - 'w' for write, 'a' for append.
    :param header: Boolean indicating if the header should be written to the CSV.
    :param max_short_answers: Maximum number of short answers to accommodate in the CSV.
    :return: None
    """

    rows = []

    for line in chunk:
        data = json.loads(line.strip())

        # Extracting and formatting data
        document_text = data['document_text']
        document_title = extract_document_title(document_text)
        question_text = data['question_text']
        yes_no_answer = data['annotations'][0]['yes_no_answer']

        # Extracting and formatting short answers
        short_answers = data['annotations'][0]['short_answers']
        document_text = document_text.split()
        short_answers_text = [
            '"{}"'.format(" ".join(document_text[ann['start_token']:ann['end_token']]).replace('"', '""')) for ann in
            short_answers]
        short_answers_text += [''] * (max_short_answers - len(short_answers_text))  # Padding with empty strings

        # Creating a row for CSV
        row = [document_title, question_text] + short_answers_text + [yes_no_answer]
        rows.append(row)

    df = pd.DataFrame(rows, columns=['document_title', 'question_text'] + [f'short_answer{i + 1}' for i in
                                                                           range(max_short_answers)] + [
                                        'yes_no_answer'])
    df = df.fillna('')

    # Append to CSV
    with open(output_csv, mode, newline='', encoding='utf-8') as f:
        df.to_csv(f, header=header, index=False, quoting=csv.QUOTE_NONNUMERIC)


def find_max_short_answers(file_path):
    """
    Determines the maximum number of short answers in any record within the JSONL file.

    This is used to create an appropriate number of columns in the CSV file.

    :param file_path: File path to the JSONL file.
    :return: Integer representing the maximum number of short answers.
    """
    max_short_answers = 0
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            data = json.loads(line.strip())
            short_answers = data['annotations'][0]['short_answers']
            max_short_answers = max(max_short_answers, len(short_answers))
    return max_short_answers


def process_file(file_path, output_csv, chunk_size=1000):
    """
    Processes the entire JSONL file in chunks and writes to a CSV file.

    This function breaks the large file into manageable chunks, processes each chunk,
    and then writes it to a CSV file.

    :param file_path: File path to the JSONL file.
    :param output_csv: File path to the output CSV file.
    :param chunk_size: Number of lines to process in each chunk.
    :return: None
    """
    max_short_answers = find_max_short_answers(file_path)

    with open(file_path, 'r', encoding='utf-8') as file:
        chunk = []
        for i, line in enumerate(file):
            chunk.append(line)
            if (i + 1) % chunk_size == 0:
                mode = 'w' if i == chunk_size - 1 else 'a'
                header = i == chunk_size - 1
                process_chunk(chunk, output_csv, mode, header, max_short_answers)
                chunk = []

        if chunk:
            mode = 'a' if i >= chunk_size else 'w'
            header = i < chunk_size
            process_chunk(chunk, output_csv, mode, header, max_short_answers)


#  Usage
file_path = 'data/train.jsonl'  # Replace with your file path
output_csv = 'output.csv'
process_file(file_path, output_csv, chunk_size=1000)  # You can adjust the chunk size
