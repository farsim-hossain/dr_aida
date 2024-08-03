


from chatbot_logic import chat_with_mistral, extract_name
from disease_prediction import predict_disease, get_drug_recommendations
import pandas as pd

message_history = []
name = None

# Load  drugs dataframe
drugs_df = pd.read_csv('drugs_df_combined.csv')


# Request user's name
message = input("Dr. Aida : Hi, I'm Dr. Aida. May I have your name please? ")

while not name:
    name = extract_name(message)
    if name:
        message_history.append({"role": "user", "content": message})
        print(f"Dr. Aida: Nice to meet you, {name}. How are you feeling today?")
        message = input("User: ")
    else:
        print("Dr. Aida: I'm sorry, I didn't catch your name. Could you please tell me your name?")
        message = input("User: ")

# Collect symptoms
message_history.append({"role": "user", "content": message})

while True:
    response, _ = chat_with_mistral(message, message_history, name)
    print("Dr. Aida: " + response)
    message_history.append({"role": "assistant", "content": response})
    
    message = input("User: ")
    if message.lower() == "no more symptoms":
        break
    message_history.append({"role": "user", "content": message})

# print("Mistral Doctor: Thank you for sharing the information. Let me check my system based on the symptoms you have mentioned and get back to you with more information soon.")
# predicted_disease = predict_disease(message_history)

print("Dr. Aida: Thank you for sharing the information. Let me check my system based on the symptoms you have mentioned and get back to you with more information soon.")
predicted_disease = predict_disease(message_history)

if predicted_disease:
    # Get drug recommendations
    recommended_drugs = get_drug_recommendations(predicted_disease, drugs_df)

    # Prepare the response
    response = f"Dr. Aida: Based on the symptoms, our system has detected that you may have {predicted_disease}."

    if recommended_drugs:
        drug_list = ", ".join(recommended_drugs[:5])  # Limit to 5 drugs to avoid overly long messages
        response += f" You can consider taking these medicines: {drug_list}. However, please consult with a healthcare professional before taking any medication."
    else:
        response += " I couldn't find specific medication recommendations for this condition in my database. Please consult with a healthcare professional for appropriate treatment."
else:
    response = "Dr. Aida: I'm sorry, but I couldn't determine a specific condition based on the symptoms you've described. It's best to consult with a healthcare professional for a proper diagnosis and treatment plan."

response += "\n\n\nYou can also contact our 24/7 appointment desk to get an appointment with our healthcare professionals. Call us at 400-500-SICK for the appointment. Thank you and hope you feel better soon."


print(response)

# print(f"Mistral Doctor: Based on the symptoms, you may have: {predicted_disease}")







