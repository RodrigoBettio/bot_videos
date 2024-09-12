import telebot
import openai
import uuid
import os
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from dotenv import load_dotenv

load_dotenv() 
bot = telebot.TeleBot(os.getenv('CHAVE_API'))
openai.api_key = os.getenv('OPENAI_API_KEY')

#Criar Teclado
markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
itembtn1 = KeyboardButton('Resumo Detalhado')
itembtn2 = KeyboardButton('Resumo Rápido')
markup.add(itembtn1, itembtn2)

# Mensagem de Start
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Olá! Sou seu bot de resumo de vídeos. Escolha uma opção:", reply_markup=markup)

# Transcrição do Vídeo
def transcrever_video(video_file):
    try:
        print("Nome do arquivo recebido pela função:", video_file)  # Depuração
        with open(video_file, "rb") as audio_file:
            print("Tentando transcrever o arquivo:", video_file)  # Depuração
            transcript = openai.Audio.translate("whisper-1", audio_file).text
            print("Transcrição:", transcript)  # Depuração - Imprime a transcrição
        return transcript 
    except Exception as e:
        print(f"Erro na função transcrever_video: {e}")  # Depuração - Imprime o erro completo
        return None

# Resumo Detalhado

def resumir_texto(texto, tipo_resumo="detalhado"):
    prompt = f"Por favor, forneça um resumo {tipo_resumo} do seguinte texto:\n\n{texto}"
    response = openai.Completion.create(
        engine="text-davinci-003",  
        prompt=prompt,
        max_tokens=500,  
        temperature=0.7,  # Ajuste para controlar a criatividade
    )
    return response.choices[0].text.strip()

@bot.message_handler(func=lambda message: message.text == 'Resumo Detalhado')
def handle_resumo_detalhado(message):
    bot.send_message(message.chat.id, "Envie o vídeo que deseja resumir detalhadamente.")

    @bot.message_handler(content_types=['video'])
    def process_video_detalhado(message):
        try:
            file_info = bot.get_file(message.video.file_id)
            print("Caminho do arquivo:", file_info.file_path)  # Depuração
            downloaded_file = bot.download_file(file_info.file_path)
            
            # Gera um id para o arquivo
            unique_filename = f"video_{uuid.uuid4()}.mp4"

            with open(unique_filename, 'wb') as new_file:
                new_file.write(downloaded_file)

            transcricao = transcrever_video(unique_filename)

            if transcricao:
                resumo = resumir_texto(transcricao, "detalhado")
                bot.send_message(message.chat.id, resumo)
            else:
                bot.reply_to(message, "Erro ao transcrever o vídeo. Tente novamente.")

            # Remove o arquivo depois de processar
            os.remove(unique_filename)
        except Exception as e:
            bot.reply_to(message, f"Ocorreu um erro ao processar o vídeo: {e}")

bot.polling()
