import streamlit as st
import pandas as pd
import ast  # For safely evaluating list strings
import os  # To check file existence

# Load predefined keywords (sorted alphabetically)
keywords = sorted([
    'Normal/Weird', 'accent', 'age', 'aggressive', 'agreeable', 'anger', 
    'attractive', 'charisma', 'confidence', 'conscientiousness', 'dominance', 
    'emotionally stable', 'empathy', 'extraversion', 'fear', 'funny', 'gender', 
    'happy', 'health', 'height', 'height/size', 'intelligent', 'leadership', 
    'loudness', 'neuroticism', 'openness', 'sad', 'skin', 'socioeconomic', 
    'speech', 'strength', 'surprise', 'trustworthy', 'valence', 'voice'
])

# File paths for saving progress
PROGRESS_FILE = "progress.csv"

# Function to safely evaluate `semantic_fields` values
def safe_literal_eval(val):
    try:
        if pd.notna(val):
            if val.startswith("[") and val.endswith("]"):
                return ast.literal_eval(val)
            else:
                return [val]  # Wrap single strings in a list
        return []
    except (ValueError, SyntaxError):
        st.warning(f"Skipping invalid value in semantic_fields: {val}")
        return []

# File upload
uploaded_file = st.file_uploader("Upload your CSV file with descriptions and semantic fields", type=["csv"])

if uploaded_file:
    # Load the uploaded CSV
    original_df = pd.read_csv(uploaded_file)

    if 'description' not in original_df.columns or 'semantic_fields' not in original_df.columns:
        st.error("The CSV must have 'description' and 'semantic_fields' columns.")
    else:
        # Check if progress file exists and merge progress
        if os.path.exists(PROGRESS_FILE):
            saved_df = pd.read_csv(PROGRESS_FILE)
            saved_df['semantic_fields'] = saved_df['semantic_fields'].apply(safe_literal_eval)
            descriptions_df = pd.merge(original_df, saved_df, on='description', how='left')
            descriptions_df['semantic_fields'] = descriptions_df['semantic_fields_y'].combine_first(descriptions_df['semantic_fields_x'])
            descriptions_df = descriptions_df.drop(columns=['semantic_fields_x', 'semantic_fields_y'])
        else:
            descriptions_df = original_df.copy()
            descriptions_df['semantic_fields'] = descriptions_df['semantic_fields'].apply(safe_literal_eval)

        # Initialize session state for progress
        if 'progress' not in st.session_state:
            st.session_state.progress = 0

        current_index = st.session_state.progress
        total_descriptions = len(descriptions_df)

        # Resume progress
        st.write(f"### Reviewing Description {current_index + 1} of {total_descriptions}")

        current_entry = descriptions_df.iloc[current_index]
        st.write(f"**Description:** {current_entry['description']}")

        # Parse existing keywords
        current_keywords = current_entry['semantic_fields']

        st.write("Current Keywords: ", ", ".join(current_keywords) if current_keywords else "None")

        # Checklist for keywords in a grid layout (vertical sorting)
        st.write("Select keywords for this description:")
        selected_keywords = []
        num_columns = 4  # Adjust this number to control the grid layout

        # Divide the keywords into vertical chunks for each column
        rows_per_column = -(-len(keywords) // num_columns)  # Ceiling division
        keyword_chunks = [keywords[i:i + rows_per_column] for i in range(0, len(keywords), rows_per_column)]
        columns = st.columns(num_columns)

        for col_idx, column in enumerate(columns):
            with column:
                for keyword in keyword_chunks[col_idx]:
                    checked = keyword in current_keywords
                    if st.checkbox(keyword, value=checked, key=f"{current_index}_{keyword}"):
                        selected_keywords.append(keyword)

        # Save updates and move to the next description
        if st.button("Save and Next"):
            # Update the DataFrame
            descriptions_df.at[current_index, 'semantic_fields'] = selected_keywords

            # Save progress to file
            descriptions_df['semantic_fields'] = descriptions_df['semantic_fields'].apply(lambda x: str(x))
            descriptions_df.to_csv(PROGRESS_FILE, index=False)

            # Move to the next description
            if current_index + 1 < total_descriptions:
                st.session_state.progress += 1
                st.experimental_rerun()  # Safely refresh the app
            else:
                st.success("All descriptions reviewed and saved!")
                st.stop()

        # Option to save progress and quit
        if st.button("Save and Quit"):
            descriptions_df['semantic_fields'] = descriptions_df['semantic_fields'].apply(lambda x: str(x))
            descriptions_df.to_csv(PROGRESS_FILE, index=False)
            st.success(f"Progress saved to '{PROGRESS_FILE}'. You can resume later.")
            st.stop()
