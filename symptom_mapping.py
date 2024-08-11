import spacy
import re

# Load the NER model
nlp = spacy.load("disease_ner_model")

# Define symptom keywords
keywords_new = {
    "itching": ["itching", "itch"],
    "skin_rash": ["skin", "skin rash", "rash"],
    "nodal_skin_eruptions": ["nodal", "skin", "eruptions"],
    "continuous_sneezing": ["non stop sneezing", "sneezing"],
    "shivering": ["shivering", "chills", "feel cold", "feling cold"],
    "chills": ["chills", "fever"],
    "joint_pain": ["joint pain", "arthritis", "bone pain", "pain", "joint"],
    "stomach_pain": ["stomach pain", "abdominal pain", "belly", "stomach", "abdominal"],
    "acidity": ["acidity", "heartburn", "bitterness", "acid", "gas"],
    "ulcers_on_tongue": ["ulcers on tongue", "mouth sores", "ulcer", "mouth ulcer"],
    "muscle_wasting": ["muscle wasting", "muscle weakness", "muscle pain", "muscle"],
    "vomiting": ["vomiting", "nausea", "vomit"],
    "burning_micturition": ["burning micturition", "painful urination"],
    "spotting_urination": ["spotting urination", "frequent urination", "dysuria", "pain while urinating"],
    "fatigue": ["fatigue", "tiredness", "tired", "weak"],
    "weight_gain": ["weight gain", "obesity", "fat"],
    "anxiety": ["anxiety", "stress", "anxious", "nervousness", "nervous"],
    "cold_hands_and_feets": ["cold hands and feet", "poor circulation", "blood circulation", "circulation", "cold hand", "cold feet"],
    "mood_swings": ["mood swing", "irritability", "mood"],
    "weight_loss": ["weight loss", "slimming", "losing weight"],
    "restlessness": ["restlessness", "insomnia", "restless"],
    "lethargy": ["lethargy", "apathy", "lethargic"],
    "patches_in_throat": ["patches in throat", "throat", "patches", "sore throat"],
    "irregular_sugar_level": ["irregular sugar level", "diabetes", "sugar"],
    "cough": ["cough", "respiratory issues", "bad cough"],
    "high_fever": ["high fever", "temperature elevation", "fever", "high temperature", "temperature"],
    "sunken_eyes": ["sunken eyes", "fatigue", "eyes"],
    "breathlessness": ["breathlessness", "shortness of breath", "breath"],
    "sweating": ["sweating", "perspiration", "sweat"],
    "dehydration": ["dehydration", "water loss", "thirsty"],
    "indigestion": ["indigestion", "heartburn", "bad stomach", "stomach"],
    "headache": ["headache", "migraine", "bad headache"],
    "yellowish_skin": ["yellowish skin", "jaundice", "pale skin", "pale"],
    "dark_urine": ["dark urine", "kidney issues", "red urine"],
    "nausea": ["nausea", "vomiting", "retching"],
    "loss_of_appetite": ["loss of appetite", "decreased hunger", "appetite"],
    "pain_behind_the_eyes": ["pain behind the eyes", "eye strain", "pain", "eye", "eyes"],
    "back_pain": ["back pain", "muscle strain", "back"],
    "constipation": ["constipation", "bowel issues", "hard stool"],
    "abdominal_pain": ["abdominal pain", "stomach cramps", "cramps"],
    "diarrhoea": ["diarrhoea", "frequent bowel movements"],
    "mild_fever": ["mild fever", "low-grade temperature", "low temperature"],
    "yellow_urine": ["yellow urine", "urine color change", "urine color"],
    "yellowing_of_eyes": ["yellowing of eyes", "jaundice", "yellow eye", "yellow eyes"],
    "acute_liver_failure": ["acute liver failure", "liver dysfunction", "liver"],
    "fluid_overload": ["fluid overload", "edema", "fluid"],
    "swelling_of_stomach": ["swelling of stomach", "abdominal distension", "swelling stomach", "swelling abdomen"],
    "swelled_lymph_nodes": ["swelled lymph nodes", "enlarged lymph nodes"],
    "malaise": ["malaise", "general discomfort"],
    "blurred_and_distorted_vision": ["blurred and distorted vision", "eye problems", "blurred vision", "unclear vision", "not seeing clearly"],
    "phlegm": ["phlegm", "mucus"],
    "throat_irritation": ["throat irritation", "sore throat", "throat"],
    "redness_of_eyes": ["redness of eyes", "eye irritation"],
    "sinus_pressure": ["sinus pressure", "congestion", "sinus"],
    "runny_nose": ["runny nose", "rhinorrhea"],
    "congestion": ["congestion", "stuffy nose"],
    "chest_pain": ["chest pain", "cardiac issues", "heart"],
    "weakness_in_limbs": ["weakness in limbs", "muscle weakness"],
    "fast_heart_rate": ["fast heart rate", "tachycardia", "fast heartbeat"],
    "pain_during_bowel_movements": ["pain during bowel movements", "rectal pain"],
    "pain_in_anal_region": ["pain in anal region", "anal pain"],
    "bloody_stool": ["bloody stool", "hematochezia"],
    "irritation_in_anus": ["irritation in anus", "anal itching"],
    "neck_pain": ["neck pain", "cervical pain"],
    "dizziness": ["dizziness", "lightheadedness", "dizzy"],
    "cramps": ["cramps", "muscle spasms"],
    "bruising": ["bruising", "ecchymosis"],
    "obesity": ["obesity", "overweight", "fat"],
    "swollen_legs": ["swollen legs", "edema", "legs"],
    "swollen_blood_vessels": ["swollen blood vessels", "vasculitis"],
    "puffy_face_and_eyes": ["puffy face and eyes", "edema"],
    "enlarged_thyroid": ["enlarged thyroid", "goiter", "thyroid"],
    "brittle_nails": ["brittle nails", "nail fragility"],
    "swollen_extremeties": ["swollen extremeties", "edema"],
    "excessive_hunger": ["excessive hunger", "polyphagia", "hunger"],
    "extra_marital_contacts": ["extra marital contacts", "infidelity"],
    "drying_and_tingling_lips": ["drying and tingling lips", "cheilitis", "dry lip", "dry lips"],
    "slurred_speech": ["slurred speech", "dysarthria"],
    "knee_pain": ["knee pain", "knee joint pain"],
    "hip_joint_pain": ["hip joint pain", "hip arthritis", "hip pain"],
    "muscle_weakness": ["muscle weakness", "muscle atrophy"],
    "stiff_neck": ["stiff neck", "cervical stiffness"],
    "swelling_joints": ["swelling joints", "joint swelling"],
    "movement_stiffness": ["movement stiffness", "muscle rigidity", "cant move", "not able to move"],
    "spinning_movements": ["spinning movements", "vertigo"],
    "loss_of_balance": ["loss of balance", "ataxia"],
    "unsteadiness": ["unsteadiness", "lightheadedness", "unsteady"],
    "weakness_of_one_body_side": ["weakness of one body side", "hemiparesis", "weakness"],
    "loss_of_smell": ["loss of smell", "anosmia", "cant smell"],
    "bladder_discomfort": ["bladder discomfort", "urinary issues"],
    "foul_smell_of_urine": ["foul smell of urine", "urinary tract infection"],
    "continuous_feel_of_urine": ["continuous feel of urine", "urinary frequency"],
    "passage_of_gases": ["passage of gases", "flatulence"],
    "internal_itching": ["internal itching", "pruritus"],
    "toxic_look_typhos": ["toxic look typhos", "typhoid fever", "typhoid"],
    "depression": ["depression", "mental health disorders"],
    "irritability": ["irritability", "mood swings"],
    "muscle_pain": ["muscle pain", "myalgia"],
    "altered_sensorium": ["altered sensorium", "confusion"],
    "red_spots_over_body": ["red spots over body", "petechiae", "spots", "red spots"],
    "belly_pain": ["belly pain", "abdominal pain"],
    "abnormal_menstruation": ["abnormal menstruation", "menstrual irregularities"],
    "dischromic_patches": ["dischromic patches", "skin discoloration"],
    "watering_from_eyes": ["watering from eyes", "lacrimation"],
    "increased_appetite": ["increased appetite", "polyphagia", "hungry"],
    "polyuria": ["polyuria", "frequent urination"],
    "family_history": ["family history", "genetic disorders"],
    "mucoid_sputum": ["mucoid sputum", "respiratory issues"],
    "rusty_sputum": ["rusty sputum", "hemoptysis"],
    "lack_of_concentration": ["lack of concentration", "attention deficit", "concentration"],
    "visual_disturbances": ["visual disturbances", "blurred vision"],
    "receiving_blood_transfusion": ["receiving blood transfusion", "blood transfusion"],
    "receiving_unsterile_injections": ["receiving unsterile injections", "unsterile injections"],
    "coma": ["coma", "unconsciousness"],
    "stomach_bleeding": ["stomach bleeding", "gastrointestinal bleeding"],
    "distention_of_abdomen": ["distention of abdomen", "abdominal swelling"],
    "history_of_alcohol_consumption": ["history of alcohol consumption", "alcoholism"],
    "fluid_overload": ["fluid overload", "edema"],
    "blood_in_sputum": ["blood in sputum", "hemoptysis"],
    "prominent_veins_on_calf": ["prominent veins on calf", "varicose veins"],
    "palpitations": ["palpitations", "heart palpitations"],
    "painful_walking": ["painful walking", "foot pain"],
    "pus_filled_pimples": ["pus filled pimples", "acne"],
    "blackheads": ["blackheads", "comedones"],
    "scurring": ["scurring", "scarring"],
    "skin_peeling": ["skin peeling", "exfoliation"],
    "silver_like_dusting": ["silver like dusting", "skin discoloration"],
    "small_dents_in_nails": ["small dents in nails", "nail abnormalities"],
    "inflammatory_nails": ["inflammatory nails", "nail inflammation"],
    "blister": ["blister", "fluid-filled bumps"],
    "red_sore_around_nose": ["red sore around nose", "nasal irritation"],
    "yellow_crust_ooze": ["yellow crust ooze", "pus-filled crust"],
    "difficulty_breathing": ["difficulty breathing", "breathing","shortness of breath", "breathlessness", "labored breathing", "dyspnea", "breath"],
    "blood_pressure": ["blood pressure", "hypertension", "high BP", "high blood pressure", "high pressure"],
    "cholesterol_level": ["cholesterol", "high cholesterol" , "high lipid levels" , "LDL"]
}

# Function to map entities to prediction model columns
def map_entities_to_columns(text, symptom_keywords):
    mapping = {symptom: 0 for symptom in symptom_keywords.keys()}
    doc = nlp(text)
    for ent in doc.ents:
        symptom = ent.label_.lower()
        if symptom in mapping:
            mapping[symptom] = 1
    return mapping

# Function to map keywords to prediction model columns
def map_keywords_to_columns(text, symptom_keywords):
    mapping = {symptom: 0 for symptom in symptom_keywords.keys()}
    for symptom, keys in symptom_keywords.items():
        pattern = re.compile(r'\b(' + '|'.join(keys) + r')\b', re.IGNORECASE)
        matches = pattern.findall(text)
        if matches:
            mapping[symptom] = 1
    return mapping

def map_symptoms(text):
    mapping = map_entities_to_columns(text, keywords_new)
    keyword_mapping = map_keywords_to_columns(text, keywords_new)
    for symptom in mapping.keys():
        if mapping[symptom] == 0 and keyword_mapping[symptom] == 1:
            mapping[symptom] = 1
    return mapping
