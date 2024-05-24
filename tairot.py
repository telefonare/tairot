import streamlit as st
import os
from groq import Groq
import random
from kerykeion import AstrologicalSubject,KerykeionChartSVG,Report
import sys
import io
import pandas as pd

def f_preguntar():
    pass #st.title("####1")
    

def main():
    """
    This function is the main entry point of the application. It sets up the Groq client, the Streamlit interface, and handles the chat interaction.
    """
    
    # Get Groq API key
    groq_api_key = os.environ['GROQ_API_KEY']

    # Display the Groq logo
    spacer, col = st.columns([5, 1])  
    #with col:  
    #    st.image('groqcloud_darkmode.png')


    client = Groq(
        api_key=groq_api_key
    )
    # The title and greeting message of the Streamlit application
    st.title("Chatea con el gran astrologo Tairot!")
    st.write("Saludos consultante, Soy el Gran Tairot, un astrologo visionario que puede responder preguntas profundas de tu vida interpretando tu carta natal.")
    st.write("<- Completa tus datos de nacimiento primero!")

    # Add customization options to the sidebar
    st.sidebar.title('Customization')
    consultante = st.sidebar.text_input("Nombre del consultante:")
    fecha_cons = st.sidebar.date_input("Fecha de Nacimiento:", value="default_value_today", format ="DD/MM/YYYY",min_value=pd.to_datetime("1930-01-01", format="%Y-%m-%d"))
    hora_cons = st.sidebar.time_input("Hora de nacimiento:", value="now")
    lugar = st.sidebar.selectbox(
        'Lugar',
        ['Buenos Aires']
    )

    if consultante:
       st.session_state.consultante = consultante

    if fecha_cons:
        st.session_state.fecha_cons = fecha_cons
    #conversational_memory_length = st.sidebar.slider('Conversational memory length:', 1, 10, value = 5)

    #memory = ConversationBufferWindowMemory(k=conversational_memory_length, memory_key="chat_history", return_messages=True)
    message = None
    if 'userq' in st.session_state:
        print("#2")
        message = st.session_state.userq
        st.session_state.userq = ""

    print("#3",type(fecha_cons))
    user_question = st.text_input("Que quieres preguntar?:",on_change=f_preguntar,key = "userq")
    #print("#4",user_question)
    #message = user_question
    


    if message:
        st.session_state.chat_history.append(message)

        # Create a kerykeion instance:
        # Args: Name, year, month, day, hour, minuts, city, nation(optional)
        anio = fecha_cons.year
        mes = fecha_cons.month
        dia = fecha_cons.day
        hora = hora_cons.hour
        minutos = hora_cons.minute
        print("#6",anio,mes,dia,hora,minutos)
        carta = AstrologicalSubject(consultante, anio, mes, dia, hora, minutos,lng=-34, lat = -58, city ="Buenos Aires", nation = "Argentina")
        report = Report(carta)

        original_stdout = sys.stdout
        sys.stdout = io.StringIO()

        report.print_report()

        # Obtiene la salida como un string
        salida_como_string = sys.stdout.getvalue()

        # Restaura la salida estándar original
        sys.stdout = original_stdout

        reporte = salida_como_string
        print("#1", reporte)

        messages = [
    {"role": "system", "content": """You are an agent with the role of playing as a character in a fantasy RPG game. 
    You are the great Tairot, a mystical astrologer who can answer questions to consultants using a given astrological birth chart, don´t make calculations just use the provided chart report.
    """},
 
        ]
        for i,msg in enumerate(st.session_state.chat_history):
            role = "user" if i % 2 == 0 else "assistant"
            if role == "user":
                contenido = f""" {msg} .justify your answer and use the data from the report to reason your answer, don't do calculations.
                    my astrology birth chart:
                    {reporte}
                     (answer in spanish)"""
            else:
                contenido = msg
            
            messages.append({"role": role, "content": contenido})


        #st.title("####2")
        chat_completion = client.chat.completions.create(
            messages=messages,
            model="llama3-70b-8192",
            temperature=0.9,

            # The maximum number of tokens to generate. Requests can use up to
            # 32,768 tokens shared between prompt and completion.
            max_tokens=1024,
        )

        
        st.session_state.chat_history.append(chat_completion.choices[0].message.content)
        
    # session state variable
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history=[]
    else:
        for message in st.session_state.chat_history:
            st.write(message)



if __name__ == "__main__":
    main()





