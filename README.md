# Question-Answer Dataset Exploration and Analysis

This project is focused on cleaning, processing, and exploring a large question-and-answer dataset. It includes scripts for data exploration, processing large JSONL files into a more accessible CSV format, and a Streamlit application for interactive data exploration.

## Installation and Setup

To get started, follow these steps to set up your environment:

1. **Install Python**: Ensure that you have Python installed on your system. This project is developed using Python 3.8 or later. You can download Python from [here](https://www.python.org/downloads/).

2. **Clone Repository**: Clone this repository to your local machine using `git clone`.

3. **Install Dependencies**: Install the required Python libraries using the following command:

   ```bash
   pip install -r requirements.txt
   ```

4. **Download Dataset**:
- Download the dataset from [this link](https://saksglobal-my.sharepoint.com/personal/ammar_fahmy_veracitygp_com/_layouts/15/download.aspx?SourceUrl=%2Fpersonal%2Fammar%5Ffahmy%5Fveracitygp%5Fcom%2FDocuments%2FVeracityGP%5Ftech%5Finterview%5Fdatasets%2Ftrain%2Ejsonl).
- Place the downloaded `train.jsonl` file in the `data` directory within the project folder.

## Running the Scripts

### Data Exploration (`eda.ipynb`)

- This Jupyter notebook is used for initial exploration of the dataset.
- Open the notebook in Jupyter Lab or similar and run the cells to explore the dataset.

### Data Processing (`process_chunks.py`)

- This script processes the JSONL file and converts it into a CSV file for easier access.
- Run the script using the following command:
  ```bash
  python process_chunks.py
  ```
- The script will create an `output.csv` file with processed data.

### Streamlit App (`streamlit_app.py`)

- This Streamlit app provides an interactive interface to explore the processed dataset.
- Run the app using the following command:
  ```bash
  streamlit run streamlit_app.py
  ```
- The app will start in your default web browser.

## Using the Streamlit App

- Once the app is running, you can:
- View the dataset in a tabular format.
- Apply filters to explore specific aspects of the data.
- Interact with various UI elements to customize the data view.

## Live Demo

- Live demo is available, you can access it at [Live Demo URL](https://qna-dataset-explorer.streamlit.app/).

