import streamlit as st

# Predefined list of keywords
keywords = [
    'Normal/Weird', 'accent', 'age', 'aggressive', 'agreeable', 'anger', 
    'attractive', 'charisma', 'confidence', 'conscientiousness', 'dominance', 
    'emotionally stable', 'empathy', 'extraversion', 'fear', 'funny', 'gender', 
    'happy', 'health', 'height', 'height/size', 'intelligent', 'leadership', 
    'loudness', 'neuroticism', 'openness', 'sad', 'skin', 'socioeconomic', 
    'speech', 'strength', 'surprise', 'trustworthy', 'valence', 'voice'
]

# List of descriptions to check against
descriptions = st.text_area("Enter descriptions (one per line):").splitlines()

# Missing keywords identified
missing_keywords = [desc for desc in descriptions if desc not in keywords]

st.header("Keywords Manager")

# Display missing descriptions
if missing_keywords:
    st.subheader("Descriptions not in Keywords:")
    for keyword in missing_keywords:
        st.text(keyword)

    # Add missing keywords interactively
    add_to_keywords = st.multiselect("Select descriptions to add to keywords:", missing_keywords)

    if st.button("Add Selected to Keywords"):
        keywords.extend(add_to_keywords)
        keywords = list(set(keywords))  # Ensure uniqueness
        st.success(f"Added {len(add_to_keywords)} keywords!")
        st.text_area("Updated Keywords List:", "\n".join(sorted(keywords)))
else:
    st.success("All descriptions are already included in the keywords list!")
