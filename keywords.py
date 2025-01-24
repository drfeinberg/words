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
        st.write("### Descriptions and Associated Keywords")

        # Interactive keyword assignment
        updated_data = []
        for index, row in descriptions_df.iterrows():
            st.write(f"**Description {index + 1}:** {row['description']}")

            # Load current keywords from 'semantic_fields'
            try:
                current_keywords = ast.literal_eval(row['semantic_fields']) if pd.notna(row['semantic_fields']) else []
                if not isinstance(current_keywords, list):
                    raise ValueError
            except (ValueError, SyntaxError):
                current_keywords = []
                st.warning(f"Invalid semantic fields format for description {index + 1}. Defaulting to empty list.")

            st.write("Current Keywords: ", ", ".join(current_keywords) if current_keywords else "None")

            # Checklist for keywords
            selected_keywords = st.multiselect(
                f"Select keywords for description {index + 1}",
                options=keywords,
                default=current_keywords,
                key=f"keywords_{index}"
            )

            # Update data
            updated_data.append({
                "description": row['description'],
                "semantic_fields": selected_keywords  # Store updated list
            })

        # Save updated data
        if st.button("Save Updates"):
            updated_df = pd.DataFrame(updated_data)
            updated_df['semantic_fields'] = updated_df['semantic_fields'].apply(lambda x: str(x))  # Convert lists to strings
            updated_df.to_csv("updated_descriptions.csv", index=False)
            st.success("Updated descriptions saved to 'updated_descriptions.csv'!")
            st.dataframe(updated_df)
