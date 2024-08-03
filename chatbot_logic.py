

import os
import requests
import json
from disease_prediction import predict_disease





def chat_with_mistral(message, message_history, name):
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {os.getenv('MISTRAL_API_KEY')}",
        "Content-Type": "application/json"
    }
    
    messages = [
        {
            "role": "system",
            "content": (
                f"The user's name is {name}. "
                "Respond with short sentences and ask one follow-up question at a time to better "
                "understand the user's symptoms. Do not number your questions. "
                "After each question, add: 'If you have no other symptoms, please type \"no more symptoms\".'"
                
            )
        }

        # "After each question, add: 'If you have no other symptoms, please type \"no more symptoms\".'"
    ] + message_history + [
        {"role": "user", "content": message}
    ]
    
    data = {
        "model": "mistral-small",
        "messages": messages
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(data))
    response_message = response.json()["choices"][0]["message"]["content"]
    




    return response_message, True


















def extract_name(message):
    import re
    match = re.search(r"(?:my name is|this is|hi, this is|hello, this is|hey, i'm|i am|i'm|hello, i'm|hello, i am|hi, i am|hi, i'm|hey, this is|it's|it is|hello, my name is|hi, my name is|hey, my name is) (\w+)", message, re.IGNORECASE)
    if match:
        return match.group(1)
    else:
        return None

def handle_symptoms(symptoms):
    if symptoms.lower() == "no more symptoms":
        # Predict disease based on the collected symptoms
        return predict_disease(symptoms)
    else:
        return "Thank you for sharing the information. Let me check my system based on the symptoms you have mentioned and get back to you with more information soon."

