import pandas as pd
import streamlit as st

# Configure the Streamlit app page with a title and layout settings
st.set_page_config(page_title="Data Exploration App", layout="wide")

# Import necessary functions from pandas for data type checks
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)

# Set up the title and subtitle for the app
st.title("Interactive Data Exploration Tool")
st.subheader("Explore and filter the Question-Answer dataset")


# Define a caching mechanism to load data only once and reuse it, enhancing performance
@st.cache_data
def load_data():
    """
    Load the dataset from the output CSV file into a pandas DataFrame.
    The data is read with low memory usage settings.

    Returns:
        pd.DataFrame: A DataFrame containing the dataset.
    """
    return pd.read_csv('output.csv', low_memory=False)


def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds a user interface on top of a DataFrame allowing users to apply various filters.
    Supports filtering for different data types including categorical, numeric, datetime, and text.

    Args:
        df (pd.DataFrame): The original DataFrame to be filtered.

    Returns:
        pd.DataFrame: The filtered DataFrame based on user inputs.
    """
    modify = st.checkbox("Add filters")

    if not modify:
        return df

    df = df.copy()

    # Convert object datatypes to datetime if possible for better filtering
    for col in df.columns:
        if is_object_dtype(df[col]):
            try:
                df[col] = pd.to_datetime(df[col])
            except Exception:
                pass

        if is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.tz_localize(None)

    modification_container = st.container()

    with modification_container:
        to_filter_columns = st.multiselect("Filter dataframe on", df.columns)
        for column in to_filter_columns:
            left, right = st.columns((1, 20))
            # UI element setup based on column data type
            if is_categorical_dtype(df[column]) or df[column].nunique() < 10:
                # Filtering logic for categorical data
                user_cat_input = right.multiselect(
                    f"Values for {column}",
                    df[column].unique(),
                    default=list(df[column].unique()),
                )
                df = df[df[column].isin(user_cat_input)]
            elif is_numeric_dtype(df[column]):
                # Filtering logic for numeric data
                _min = float(df[column].min())
                _max = float(df[column].max())
                step = (_max - _min) / 100
                user_num_input = right.slider(
                    f"Values for {column}",
                    min_value=_min,
                    max_value=_max,
                    value=(_min, _max),
                    step=step,
                )
                df = df[df[column].between(*user_num_input)]
            elif is_datetime64_any_dtype(df[column]):
                # Filtering logic for datetime data
                user_date_input = right.date_input(
                    f"Values for {column}",
                    value=(
                        df[column].min(),
                        df[column].max(),
                    ),
                )
                if len(user_date_input) == 2:
                    user_date_input = tuple(map(pd.to_datetime, user_date_input))
                    start_date, end_date = user_date_input
                    df = df.loc[df[column].between(start_date, end_date)]
            else:
                # Filtering logic for text data
                user_text_input = right.text_input(
                    f"Substring or regex in {column}",
                )
                if user_text_input:
                    df = df[df[column].astype(str).str.contains(user_text_input)]
    return df


# Load the dataset and prepare for display
df = load_data()
# Get column names that start with 'short_answer'
short_answer_columns = [col for col in df.columns if col.startswith('short_answer')]
# Filter out rows where 'yes_no_answer' is 'NONE' and all 'short_answer' columns are empty
df = df[~((df['yes_no_answer'] == 'NONE') & (df[short_answer_columns].fillna('').sum(axis=1) == ''))]
# Display the filtered DataFrame in the Streamlit app
st.dataframe(filter_dataframe(df))
