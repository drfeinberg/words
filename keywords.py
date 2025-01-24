import streamlit as st
import pandas as pd
import ast  # For safely evaluating list strings

# Load predefined keywords
keywords = [
    'Normal/Weird', 'accent', 'age', 'aggressive', 'agreeable', 'anger', 
    'attractive', 'charisma', 'confidence', 'conscientiousness', 'dominance', 
    'emotionally stable', 'empathy', 'extraversion', 'fear', 'funny', 'gender', 
    'happy', 'health', 'height', 'height/size', 'intelligent', 'leadership', 
    'loudness', 'neuroticism', 'openness', 'sad', 'skin', 'socioeconomic', 
    'speech', 'strength', 'surprise', 'trustworthy', 'valence', 'voice'
]

# File upload
uploaded_file = st.file_uploader("Upload your CSV file with descriptions and semantic fields", type=["csv"])

if uploaded_file:
    # Load the CSV
    descriptions_df = pd.read_csv(uploaded_file)

    if 'description' not in descriptions_df.columns or 'semantic_fields' not in descriptions_df.columns:
        st.error("The CSV must have 'description' and 'semantic_fields' columns.")
    else:
        # Load progress
        if 'progress' not in st.session_state:
            st.session_state.progress = 0
            st.session_state.data = descriptions_df.to_dict('records')

        # Display current progress
        current_index = st.session_state.progress
        total_descriptions = len(st.session_state.data)

        st.write(f"### Reviewing Description {current_index + 1} of {total_descriptions}")

        current_entry = st.session_state.data[current_index]
        st.write(f"**Description:** {current_entry['description']}")

        # Parse existing keywords
        try:
            current_keywords = ast.literal_eval(current_entry['semantic_fields']) if pd.notna(current_entry['semantic_fields']) else []
            if not isinstance(current_keywords, list):
                raise ValueError
        except (ValueError, SyntaxError):
            current_keywords = []
            st.warning(f"Invalid semantic fields format for this description. Defaulting to an empty list.")

        st.write("Current Keywords: ", ", ".join(current_keywords) if current_keywords else "None")

        # Checklist for keywords
        selected_keywords = []
        st.write("Select keywords for this description:")
        for keyword in keywords:
            checked = keyword in current_keywords
            if st.checkbox(keyword, value=checked, key=f"{current_index}_{keyword}"):
                selected_keywords.append(keyword)

        # Save updates and move to the next description
        if st.button("Save and Next"):
            # Update current entry
            st.session_state.data[current_index]['semantic_fields'] = selected_keywords

            # Save progress to a file
            updated_df = pd.DataFrame(st.session_state.data)
            updated_df['semantic_fields'] = updated_df['semantic_fields'].apply(lambda x: str(x))  # Convert lists to strings
            updated_df.to_csv("updated_descriptions.csv", index=False)

            # Move to the next description
            if current_index + 1 < total_descriptions:
                st.session_state.progress += 1
                st.experimental_rerun()
            else:
                st.success("All descriptions reviewed and saved!")
                st.stop()

        # Option to save progress and quit
        if st.button("Save and Quit"):
            updated_df = pd.DataFrame(st.session_state.data)
            updated_df['semantic_fields'] = updated_df['semantic_fields'].apply(lambda x: str(x))
            updated_df.to_csv("updated_descriptions.csv", index=False)
            st.success("Progress saved to 'updated_descriptions.csv'. You can resume later.")
            st.stop()
