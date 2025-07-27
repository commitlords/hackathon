import os

import numpy as np  # To generate random choice
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from transformers import pipeline

from hack_rest.nlp_pipeline.chatbot import chatbot

# Define categories (must match training labels)
# categories = ["Finance", "Healthcare", "Education", "E-commerce", "Real Estate", "Travel", "Entertainment"]

df = pd.read_excel("./hack_rest/nlp_pipeline/training_data/Hackathon_business.xlsx")

categories = list(df["Business Category"].unique())

# 🔹 Load translators
translate_hi_en = pipeline("translation", model="Helsinki-NLP/opus-mt-hi-en")
translate_en_hi = pipeline("translation", model="Helsinki-NLP/opus-mt-en-hi")

# Load label encoder
le = LabelEncoder()
le.fit(categories)

# 🔹 Detect intent
# def detect_intent(text):
#     keywords = ["invest", "book", "doctor", "school", "flight", "movie", "hotel", "buy"]
#     return "classify" if any(kw in text.lower() for kw in keywords) else "chat"


# 🔹 Translation
def translate_to_english(text):
    return translate_hi_en(text)[0]["translation_text"]


def translate_to_hindi(text):
    return translate_en_hi(text)[0]["translation_text"]


# Load fine-tuned model and tokenizer
MODEL_PATH = "./hack_rest/chatbot/business_classifier"


# Classification function
def classify_top_n_finetuned_old(text, top_n=3):
    classifier = pipeline(
        "text-classification",
        model=MODEL_PATH,
        tokenizer=MODEL_PATH,
        return_all_scores=True,
    )
    results = classifier(text)[0]
    sorted_results = sorted(results, key=lambda x: x["score"], reverse=True)[:top_n]
    transfrm = [
        (
            le.inverse_transform(
                [int(r["label"]) if r["label"].isdigit() else r["label"]]
            )[0],
            round(r["score"] * 100, 2),
        )
        for r in sorted_results
    ]
    return transfrm


def classify_top_n_finetuned(text, top_n=3, threshold=0.2):

    classifier = pipeline(
        "text-classification",
        model=MODEL_PATH,
        tokenizer=MODEL_PATH,
        return_all_scores=True,
    )
    results = classifier(text)[0]
    sorted_results = sorted(results, key=lambda x: x["score"], reverse=True)[:top_n]

    top_matches = []
    for r in sorted_results:
        label_str = r["label"]  # e.g., 'LABEL_5'
        label_index = int(label_str.replace("LABEL_", ""))  # convert to 5
        category = le.inverse_transform([label_index])[0]  # decode to category name
        top_matches.append((category, round(r["score"] * 100, 2)))

    return top_matches


class ChatBot:
    def __init__(self):
        print("----- Warming up -----")

    # Sets Name of chatbot
    def set_name(self, name):
        self.name = name

    # Retuens Name of chatbot
    def get_name(self):
        return self.name

    # Converts Speech to text
    # def speech_to_text(self):
    #     recognizer = sr.Recognizer()
    #     with sr.Microphone() as mic:
    #         print("Currently Listening...")
    #         recognizer.adjust_for_ambient_noise(mic,duration=1)
    #         audio = recognizer.listen(mic,timeout=15)
    #         text = "Error"
    #     try:
    #         text = recognizer.recognize_google(audio)
    #         print("Me -> ", text)
    #         return text
    #     except sr.RequestError as e:
    #         print("404 -> Could not request results; {0}".format(e))
    #         return text

    #     except sr.UnknownValueError:
    #         print("404 -> Unknown error occurred")
    #         return text
    # Converts text to speech
    # def text_to_speech(self,text):
    # print("AI -> ", text)
    # speaker = pyttsx3.init()
    # voice = speaker.getProperty('voices')
    # speaker.setProperty('voice', voice[1].id)
    # speaker.say(text)
    # speaker.runAndWait()
    # Returnes NLP response
    def chat(self, text):
        chat = chatbot(text)
        return chat
