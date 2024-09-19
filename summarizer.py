from pytubefix import YouTube
import ffmpeg
from transformers import pipeline, BartTokenizer, BartForConditionalGeneration
import os

video_url = input('Cole o link do YouTube aqui: ')

def limpar():
    file_paths = ["input_audio.mp3", "output_audio.wav"]
    for file_path in file_paths:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"{file_path} foi removido.")
        else:
            print(f"{file_path} não existe.")

def baixar_audio():
    try:
        yt = YouTube(video_url)
        audio_stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
        audio_stream.download(filename='input_audio.mp3')
        print("Áudio baixado com sucesso!")
    except Exception as e:
        print(f"Erro ao baixar o áudio: {e}")

def converter_audio():
    try:
        input_audio = 'input_audio.mp3'
        output_audio = 'output_audio.wav'
        ffmpeg.input(input_audio).output(output_audio, ar=16000).run()
        print("Áudio convertido com sucesso!")
    except Exception as e:
        print(f"Erro ao converter o áudio: {e}")

def transcrever_audio():
    try:
        asr_model = pipeline("automatic-speech-recognition", model="openai/whisper-tiny")
        transcription = asr_model('output_audio.wav')
        texto = transcription['text']
        print("Transcrição concluída com sucesso!")
        return texto
    except Exception as e:
        print(f"Erro ao transcrever o áudio: {e}")
        return ""

def resumir(texto):
    try:
        model_name = "facebook/bart-base"
        tokenizer = BartTokenizer.from_pretrained(model_name)
        model = BartForConditionalGeneration.from_pretrained(model_name)

        inputs = tokenizer(texto, return_tensors="pt", max_length=1024, truncation=True)
        summary_ids = model.generate(inputs["input_ids"], max_length=800, min_length=400, length_penalty=2.0, num_beams=4, early_stopping=True)
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True, clean_up_tokenization_spaces=False)
        print("Resumo gerado com sucesso!")
        return summary
    except Exception as e:
        print(f"Erro ao gerar o resumo: {e}")
        return ""

def main():
    limpar()
    baixar_audio()
    converter_audio()
    texto = transcrever_audio()
    if texto:
        resumo = resumir(texto)
        print(f'Resumo: {resumo}')
        
    else:
        print("Não foi possível transcrever o áudio, portanto o resumo não foi gerado.")

if __name__ == "__main__":
    main()
