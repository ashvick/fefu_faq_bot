import telebot
from sentence_transformers import SentenceTransformer
from scipy import spatial
import pandas as pd
import numpy as np
import logging

logging.basicConfig(filename="savior.log", level=logging.INFO, format='%(asctime)s  %(name)s  %(levelname)s: %(message)s')

model = SentenceTransformer('distiluse-base-multilingual-cased')

data = pd.read_csv('data.csv')
questions = data["questions"]
answers = data["answers"]

question_embeddings = model.encode(questions)
hello_embedding = model.encode('здравствуйте')

def get_answer(q):
    query = q
    query_embedding = model.encode(query)

    hello_score = 1 - spatial.distance.cdist(query_embedding, hello_embedding, "cosine")[0]

    if hello_score > 0.5:
        return 'Привет! Чтобы узнать, с чем я могу вам помочь, введите команду /help'
    else:
        distances = spatial.distance.cdist(query_embedding, question_embeddings, "cosine")[0]
        idx = np.argmin(distances)
        distance = distances[idx]
        print("\n======================\n")
        print("Query:", query)
        print("\nThe most similar sentence in corpus:")

        cos_score = 1 - distance
        print(answers[idx], "(Cosine Score: %.4f)" % (1 - distance))

        if cos_score < 0.25:
            return 'Пожалуйста, переформулируйте вопрос'
        else:
            return answers[idx]

    # print("\n\n======================\n\n")
    # print("Query:", query)
    # print("\nTop 5 most similar sentences in corpus:")

    # for idx, distance in results[0:3]:
    #     print(answers[idx].strip(), "(Cosine Score: %.4f)" % (1 - distance))

bot = telebot.TeleBot('1142344496:AAHBr4X2IwVD2E1JMShyNLxr6d_IYZFQSso')

@bot.message_handler(commands=['start', 'help'])
def start(message):
    try:
        bot.send_message(message.chat.id, 'Список вопросов, на которые я знаю ответ: \n• ' + '\n• '.join(questions))
    except Exception as e:
        logging.error('Error while sending /help', exc_info=e)

# @bot.message_handler(commands=['add_questions'])
# def add_questions(message):
#     bot.send_message(message.chat.id, 'Дорогой %(username)s, выбери csv файл')

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    try:
        bot.send_message(message.from_user.id, get_answer(message.text))
    except Exception as e:
        logging.error('Error while sending text', exc_info=e)

bot.polling()