import streamlit as st
import pandas as pd

# Load keywords
keywords = [
    'Normal/Weird', 'accent', 'age', 'aggressive', 'agreeable', 'anger', 
    'attractive', 'charisma', 'confidence', 'conscientiousness', 'dominance', 
    'emotionally stable', 'empathy', 'extraversion', 'fear', 'funny', 'gender', 
    'happy', 'health', 'height', 'height/size', 'intelligent', 'leadership', 
    'loudness', 'neuroticism', 'openness', 'sad', 'skin', 'socioeconomic', 
    'speech', 'strength', 'surprise', 'trustworthy', 'valence', 'voice'
]

# File upload
uploaded_file = st.file_uploader("Upload your CSV file with descriptions", type=["csv"])

if uploaded_file:
    # Load the CSV
    descriptions_df = pd.read_csv(uploaded_file)
    if 'description' not in descriptions_df.columns:
        st.error("The CSV must have a 'description' column.")
    else:
        st.write("### Descriptions and Associated Keywords")

        # Initialize keywords column if not present
        if 'keywords' not in descriptions_df.columns:
            descriptions_df['keywords'] = ""

        # Interactive keyword assignment
        updated_data = []
        for index, row in descriptions_df.iterrows():
            st.write(f"**Description {index + 1}:** {row['description']}")

            # Display current keywords
            current_keywords = row['semantic_fields'].split(", ") if row['semantic_fields'] else []
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
                "keywords": ", ".join(selected_keywords)
            })

        # Save updated data
        if st.button("Save Updates"):
            updated_df = pd.DataFrame(updated_data)
            updated_df.to_csv("updated_descriptions.csv", index=False)
            st.success("Updated descriptions saved to 'updated_descriptions.csv'!")
            st.dataframe(updated_df)
