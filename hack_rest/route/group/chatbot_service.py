import logging
import time
from http import HTTPStatus

from flask import jsonify, request
from flask_restx import Namespace, Resource
from langdetect import detect

from hack_rest.chatbot.bot import (
    ChatBot,
    classify_top_n_finetuned,
    translate_to_english,
    translate_to_hindi,
)
from hack_rest.chatbot.train import train_classification_ai_model
from hack_rest.nlp_pipeline.train import train_ai_model
from hack_rest.nltk_setup import nltk_lib_download
from hack_rest.route.group.models.group_register_model import (
    CHATBOT_USER_INTRACTION_MODEL,
)

# from hack_rest.nlp_pipeline.translation import translate_to_english, translate_to_hindi

BOT_NS = Namespace("chatbot", description="Chatbot related operations")

logging = logging.getLogger(__name__)

BOT_NS.models[CHATBOT_USER_INTRACTION_MODEL.name] = CHATBOT_USER_INTRACTION_MODEL


def detect_intent(user_input):
    # keywords = ["invest", "buy", "book", "school", "doctor", "flight", "movie", "hotel"]
    # if any(kw in user_input.lower() for kw in keywords):
    #     return "classify"
    # return "chat"

    if "suggest" in user_input.lower():
        return "classify"
    return "chat"


@BOT_NS.route("/interact")
class ChatBotResponse(Resource):
    """interact chatbot"""

    @BOT_NS.expect(CHATBOT_USER_INTRACTION_MODEL)
    def post(self):
        """register a group"""
        data = request.json
        user_input = data.get("sentance", "")
        if not user_input:
            return jsonify({"error": "No input text provided"}), HTTPStatus.NO_CONTENT

        try:

            lang = detect(user_input)
            if lang == "hi":
                user_input = translate_to_english(user_input)

            intent = detect_intent(user_input)

            if intent == "classify":
                top_matches = classify_top_n_finetuned(user_input)
                if not top_matches:
                    response_en = "Sorry, I couldn't confidently detect your interest."
                    response_hi = (
                        translate_to_hindi(response_en) if lang == "hi" else response_en
                    )
                    return jsonify({"response": response_hi, "top_matches": []})

                result_text = "Here’s what I think you're interested in: \n "
                for cat, score in top_matches:
                    result_text += f"- {cat} ({score}%)\n"

                reply = translate_to_hindi(result_text) if lang == "hi" else result_text
                return jsonify({"response": reply, "top_matches": top_matches})

            # chat_reply = casual_chat(user_input)

            ai = ChatBot()
            chat_reply = ai.chat(user_input)
            # return {"message": output}, 200
            chat_reply = (
                translate_to_hindi(chat_reply) if lang == "hi" else chat_reply
            )

            return jsonify({"response": chat_reply})

        except Exception as e:
            logging.error(f"Chatbot error: {str(e)}")
            return jsonify({"error": "An error occurred while processing your request"}), HTTPStatus.FORBIDDEN


@BOT_NS.route("/train", endpoint="chatbot_train")
class ChatBotTraining(Resource):
    """Train Chat Bot"""

    @staticmethod
    def get():
        """Train AI bot"""
        train_ai_model()
        time.sleep(2)
        train_classification_ai_model()
        time.sleep(2)
        nltk_lib_download()
        logging.info("Chatbot training completed...!!!")
        return {"message": "model training completed"}, HTTPStatus.OK
