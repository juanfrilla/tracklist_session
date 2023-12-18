import streamlit as st
from pydub import AudioSegment
import io
from theadwithresult import ThreadWithReturnValue
from utils import process_audio_async


def main():
    st.title("Identificador de canciones")

    uploaded_file = st.file_uploader("Elige un archivo MP3", type=["mp3"])

    if uploaded_file is not None:
        st.write("Detalles del archivo:")
        file_details = {
            "Nombre": uploaded_file.name,
            "Tipo": uploaded_file.type,
            "Tamaño": uploaded_file.size,
        }
        st.write(file_details)

        audio_content = uploaded_file.read()

        audio = AudioSegment.from_file(io.BytesIO(audio_content), format="mp3")
        st.write("Duración del audio:", len(audio) / 1000, "seconds")

        with st.spinner("Identificando canciones del audio..."):
            thread = ThreadWithReturnValue(target=process_audio_async, args=(audio,))
            thread.start()
            result = thread.join()

        st.write(result)

        st.success("Procesamiento de audio completado")
        st.audio(audio_content, format="audio/mp3")


if __name__ == "__main__":
    main()
