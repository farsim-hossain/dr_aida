# Intelligent Medical Diagnosis and Drug Recommendation System
Steps to run in your local ; 
- Create an account in Mistral AI : https://auth.mistral.ai/ui/registration?flow=a40197cc-ed5a-4d19-a2f9-4d7268d1e4c7
- Creeate an API Key : https://console.mistral.ai/api-keys/
- Copy the API Key and save it somewhere
- Clone the repository in your local
- go to the cloned repository folder with your terminal
- Create a file called '.env'
- In the .env file create a new variable called `MISTRAL_API_KEY` and paste your Mistral API key. Like this : MISTRAL_API_KEY = your api key here. - Save the file
- run `pip install -r requirements.txt`
- run `streamlit run app.py`
Your app should be running 
