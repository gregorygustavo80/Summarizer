import streamlit as st
from pytubefix import YouTube
import ffmpeg
from transformers import pipeline, BartTokenizer, BartForConditionalGeneration
import os 

st.title("Resuma vídeos do YouTube")

video_url = st.text_input("Cole o link do YouTube aqui:")

def limpar():
    file_paths = ["input_audio.mp3", "output_audio.wav"]
    for file_path in file_paths:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"{file_path} foi removido.")
        else:
            print(f"{file_path} não existe.")

def baixar_audio(video_url, progress_bar):
    try:
        yt = YouTube(video_url)
        audio_stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
        audio_stream.download(filename='input_audio.mp3')
        progress_bar.progress(33) 
        st.success("Áudio baixado com sucesso!")
    except Exception as e:
        st.error(f"Erro ao baixar o áudio: {e}")

def converter_audio(progress_bar):
    try:
        input_audio = 'input_audio.mp3'
        output_audio = 'output_audio.wav'
        ffmpeg.input(input_audio).output(output_audio, ar=16000).run()
        progress_bar.progress(66)  
        st.success("Áudio convertido com sucesso!")
    except Exception as e:
        st.error(f"Erro ao converter o áudio: {e}")

def transcrever_audio(progress_bar):
    try:
        asr_model = pipeline("automatic-speech-recognition", model="openai/whisper-large")
        transcription = asr_model('output_audio.wav')
        texto = transcription['text']
        progress_bar.progress(90)  
        st.success("Transcrição concluída com sucesso!")
        return texto
    except Exception as e:
        st.error(f"Erro ao transcrever o áudio: {e}")
        return ""

def resumir(texto, progress_bar):
    try:
        model_name = "facebook/bart-large-xsum"
        tokenizer = BartTokenizer.from_pretrained(model_name)
        model = BartForConditionalGeneration.from_pretrained(model_name)

        inputs = tokenizer(texto, return_tensors="pt", max_length=1024, truncation=True)
        summary_ids = model.generate(inputs["input_ids"], max_length=800, min_length=400, length_penalty=2.0, num_beams=8, early_stopping=True)
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True, clean_up_tokenization_spaces=False)
        
        progress_bar.progress(100) 
        st.success("Resumo gerado com sucesso!")
        return summary
    except Exception as e:
        st.error(f"Erro ao gerar o resumo: {e}")
        return ""

# Botões para iniciar cada processo
if st.button("Resumir vídeo"):
    if video_url:
        limpar()
       
        st.subheader("Processando...")
        progress_bar = st.progress(0)

        baixar_audio(video_url, progress_bar)
        converter_audio(progress_bar)
        texto = transcrever_audio(progress_bar)

        if texto:
            # Subtítulo para o resumo
            st.subheader("Resumo do vídeo")
            resumo = resumir(texto, progress_bar)
            st.write(resumo)
        else:
            st.warning("Não foi possível transcrever o áudio, portanto o resumo não foi gerado.")
    else:
        st.warning("Por favor, insira um link válido do YouTube.")
