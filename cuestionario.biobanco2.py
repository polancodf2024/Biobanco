import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Lista de estados de la República Mexicana
estados_mexico = [
    'Aguascalientes', 'Baja California', 'Baja California Sur', 'Campeche', 'Chiapas', 'Chihuahua', 'Ciudad de México',
    'Coahuila', 'Colima', 'Durango', 'Estado de México', 'Guanajuato', 'Guerrero', 'Hidalgo', 'Jalisco', 'Michoacán',
    'Morelos', 'Nayarit', 'Nuevo León', 'Oaxaca', 'Puebla', 'Querétaro', 'Quintana Roo', 'San Luis Potosí', 'Sinaloa',
    'Sonora', 'Tabasco', 'Tamaulipas', 'Tlaxcala', 'Veracruz', 'Yucatán', 'Zacatecas'
]

# Lista de enfermedades para la selección única
enfermedades_familiares = [
    'Angina inestable', 'Angina estable', 'Cardiopatía congénita', 'Valvulopatía', 'Cardiopatía pulmonar',
    'Arritmia cardiaca', 'Coágulos sanguíneos', 'Hipertensión sistémica', 'Dislipidemia', 'Diabetes',
    'Hiperuricemia', 'Tabaquismo', 'Sobrepeso', 'Cardiopatía Isquémica'
]

# Mostrar el logo arriba del cuestionario
st.image("escudo_COLOR.jpg", width=100)  # Ajustar el tamaño del logo

# Crear un diccionario para almacenar las respuestas
responses = {}

# Título del cuestionario
st.title('Cuestionario Paciente - BioBanco')

# Utilizar st.form para evitar que se desplace al enviar el formulario
with st.form(key='cuestionario_form'):
    # Pregunta inicial sobre la fecha de la entrevista
    responses['Fecha de la entrevista'] = st.date_input('Fecha de la entrevista', value=datetime.now())

    # Preguntas del cuestionario
    responses['Procedencia del paciente'] = st.selectbox(
        'Procedencia del paciente', 
        [
            'Consulta externa lado A',
            'Consulta externa lado B',
            'Clínica Arritmias',
            'Clínica Coagulación',
            'Clínica Valvulares',
            'Clínica Hipertensión'
        ]
    )
    responses['Núm. registro INCICh'] = st.text_input('Núm. registro INCICh')
    responses['Nombre del paciente'] = st.text_input('Nombre del paciente')
    responses['Fecha de nacimiento'] = st.date_input(
        'Fecha de nacimiento', 
        min_value=datetime(1920, 1, 1), 
        max_value=datetime.now()
    )
    responses['Edad actual (años)'] = st.number_input('Edad actual (años)', step=1)
    responses['Género'] = st.selectbox('Género', ['Masculino', 'Femenino', 'Otro'])
    responses['Peso (Kg)'] = st.number_input('Peso (Kg)', step=0.1)
    responses['Estatura (m)'] = st.number_input('Estatura (m)', step=0.01)
    responses['Índice de masa corporal (IMC)'] = st.number_input('Índice de masa corporal (IMC)', step=0.1)
    responses['Circunferencia de cintura (cm)'] = st.number_input('Circunferencia de cintura (cm)', step=0.1)
    responses['Tensión arterial Sistólica (mmHg)'] = st.number_input('Tensión arterial Sistólica (mmHg)', step=1)
    responses['Tensión arterial Diastólica (mmHg)'] = st.number_input('Tensión arterial Diastólica (mmHg)', step=1)
    responses['Frecuencia cardiaca (lpm)'] = st.number_input('Frecuencia cardiaca (lpm)', step=1)
    responses['Grupo étnico al que pertenece'] = st.selectbox(
        'Grupo étnico al que pertenece', 
        ['Mestizo', 'Pueblo indígena', 'Caucásico', 'Afrodescendiente']
    )
    responses['¿Dónde nacieron sus abuelos Maternos?'] = st.selectbox(
        '¿Dónde nacieron sus abuelos Maternos?', estados_mexico
    )
    responses['¿Dónde nacieron sus abuelos Paternos?'] = st.selectbox(
        '¿Dónde nacieron sus abuelos Paternos?', estados_mexico
    )
    responses['¿Dónde nacieron sus padres?'] = st.selectbox(
        '¿Dónde nacieron sus padres?', estados_mexico
    )
    responses['¿Dónde nació usted?'] = st.selectbox(
        '¿Dónde nació usted?', estados_mexico
    )
    responses['¿Tuvo o tiene familiar con alguna de las siguientes enfermedades?'] = st.selectbox(
        '¿Tuvo o tiene familiar con alguna de las siguientes enfermedades?', enfermedades_familiares
    )

    # Nueva pregunta con las opciones proporcionadas
    responses['¿Quién?'] = st.selectbox(
        '¿Quién?', 
        ['Madre', 'Padre', 'Ambos', 'Hermano(a)', 'Ninguno']
    )

    # Preguntas con opciones: Sí, No, No sabe
    options_si_no_nosabe = ['Sí', 'No', 'No sabe']

    responses['¿Fuma actualmente?'] = st.selectbox('¿Fuma actualmente?', options_si_no_nosabe)
    responses['En los últimos 3 meses ¿ha consumido alguna bebida que contenga alcohol?'] = st.selectbox(
        'En los últimos 3 meses ¿ha consumido alguna bebida que contenga alcohol?', options_si_no_nosabe
    )
    responses['¿El paciente tiene exceso de peso?'] = st.selectbox('¿El paciente tiene exceso de peso?', options_si_no_nosabe)
    responses['El paciente tiene diabetes'] = st.selectbox('El paciente tiene diabetes', options_si_no_nosabe)
    responses['¿Le han indicado medicamento(s) para controlar su diabetes?'] = st.selectbox(
        '¿Le han indicado medicamento(s) para controlar su diabetes?', options_si_no_nosabe
    )
    responses['El paciente tiene hipertensión arterial.'] = st.selectbox('El paciente tiene hipertensión arterial.', options_si_no_nosabe)
    responses['¿Le han indicado medicamentos para controlar la presión?'] = st.selectbox(
        '¿Le han indicado medicamentos para controlar la presión?', options_si_no_nosabe
    )
    responses['¿Consume algún medicamento para otra condición?'] = st.selectbox(
        '¿Consume algún medicamento para otra condición?', options_si_no_nosabe
    )
    responses['¿Tiene alguna alergia conocida?'] = st.selectbox(
        '¿Tiene alguna alergia conocida?', options_si_no_nosabe
    )
    responses['Observaciones adicionales'] = st.text_area('Observaciones adicionales')

    # Pregunta final para pedir el correo electrónico
    email = st.text_input('Si desea una copia del cuestionario, por favor proporcione su correo electrónico:')

    # Botón para enviar las respuestas
    submit_button = st.form_submit_button(label='Guardar Respuestas')

# Al hacer clic en "Guardar Respuestas"
if submit_button:
    # Convertir las respuestas a un DataFrame
    responses_df = pd.DataFrame([responses])
    
    # Archivo Excel donde se acumularán las respuestas
    excel_file = 'respuestas_cuestionario.xlsx'
    
    # Verificar si ya existe el archivo
    if os.path.exists(excel_file):
        # Cargar el archivo existente y agregar las nuevas respuestas
        existing_data = pd.read_excel(excel_file)
        new_data = pd.concat([existing_data, responses_df], ignore_index=True)
    else:
        # Si no existe, usar las nuevas respuestas como base
        new_data = responses_df
    
    # Guardar las respuestas en el archivo Excel
    new_data.to_excel(excel_file, index=False)
    st.success('Las respuestas han sido guardadas exitosamente.')

    # Mostrar el botón de "Extraer archivos" si el correo electrónico es "polanco@unam.mx"
    if email.strip().lower() == 'polanco@unam.mx':
        st.success('Correo electrónico validado: polanco@unam.mx')
        with open(excel_file, 'rb') as file:
            st.download_button(
                label='Descargar archivo Excel',
                data=file,
                file_name='respuestas_cuestionario.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )

