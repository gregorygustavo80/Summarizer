# YouTube Audio Downloader, Converter, Transcriber, and Summarizer

Este projeto Python permite baixar áudio de um vídeo do YouTube, convertê-lo para o formato `.wav`, transcrever o áudio usando um modelo de reconhecimento automático de fala e gerar um resumo do texto transcrito.

## Dependências

Para executar este projeto, você precisará instalar as seguintes bibliotecas:

- [pytubefix](https://pypi.org/project/pytubefix/)
- [ffmpeg-python](https://pypi.org/project/ffmpeg-python/)
- [transformers](https://huggingface.co/transformers/)
- [torch](https://pytorch.org/get-started/locally/)

Instale as dependências com o seguinte comando:

```bash
pip install -r requirements.txt
````

> Além disso, certifique-se de ter o FFmpeg instalado em seu sistema.

## Como usar
+ Baixar o áudio: O script baixa o áudio do vídeo do YouTube fornecido.
+ Converter o áudio: Converte o áudio baixado para o formato .wav com taxa de amostragem de 16kHz.
+ Transcrever o áudio: Utiliza o Whiper para transcrever o conteúdo do áudio.
+ Gerar um resumo: Resuma o texto transcrito utilizando o modelo BART.

Execução
Execute o script com o seguinte comando:

````bash
python summarizer.py
```` 
