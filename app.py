import streamlit as st
from chatbot_logic import chat_with_mistral
from disease_prediction import predict_disease, get_drug_recommendations
import pandas as pd

# Load your drugs dataframe
drugs_df = pd.read_csv('drugs_df_combined.csv')  # Replace with actual path

# Initialize session state variables
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'name' not in st.session_state:
    st.session_state.name = None

st.title("Intelligent Medical Diagnosis and Drug Recommendation")

# Get user's name if not already provided
if not st.session_state.name:
    st.session_state.name = st.text_input("Please enter your name:")
    if st.session_state.name:
        st.session_state.messages.append({"role": "assistant", "content": f"Nice to meet you, {st.session_state.name}. How are you feeling today?"})

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
# Chat input
if st.session_state.name:
    user_input = st.chat_input("Type your symptoms here...")
    
    if user_input:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        if user_input.lower() == "no more symptoms":
            # Predict disease
            predicted_disease = predict_disease(st.session_state.messages)
            
            if predicted_disease:
                # Get drug recommendations
                recommended_drugs = get_drug_recommendations(predicted_disease, drugs_df)
                
                # Prepare the response
                final_response = f"Based on the symptoms you've described, you may have {predicted_disease}."
                
                if recommended_drugs:
                    drug_list = ", ".join(recommended_drugs[:5])
                    final_response += f" You can consider taking these medicines: {drug_list}. However, please consult with a healthcare professional before taking any medication."
                else:
                    final_response += " I couldn't find specific medication recommendations for this condition in my database. Please consult with a healthcare professional for appropriate treatment."
                
                final_response += "\n\n\nYou can also contact our 24/7 appointment desk to get an appointment with our healthcare professionals. Call us at 400-500-SICK for the appointment. Thank you and hope you feel better soon."
                
                # Add final response to chat history
                st.session_state.messages.append({"role": "assistant", "content": final_response})
            else:
                st.session_state.messages.append({"role": "assistant", "content": "I'm sorry, but I couldn't determine a specific condition based on the symptoms you've described. It's best to consult with a healthcare professional for a proper diagnosis and treatment plan."})
        else:
            # Get chatbot response for ongoing symptom description
            response, _ = chat_with_mistral(user_input, st.session_state.messages, st.session_state.name)
            
            # Add assistant message to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Rerun the app to display the new messages
        st.rerun()


# Add a disclaimer at the bottom of the page
st.markdown("---")
st.markdown("**Disclaimer:** This AI health assistant is for informational purposes only and is not a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition.")
