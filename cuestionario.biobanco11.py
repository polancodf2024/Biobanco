import streamlit as st
import pandas as pd
import os
from datetime import datetime
from filelock import FileLock

# Mostrar el logo
st.image("escudo_COLOR.jpg", width=100)

# Archivo Excel donde se acumularán todas las respuestas
acumulado_excel_file = 'respuestas_cuestionario_acumulado.xlsx'
lock_file = 'acumulado_excel_file.lock'

# Lista de estados de la República Mexicana
estados_mexico = [
    'Otro', 'Aguascalientes', 'Baja California', 'Baja California Sur', 'Campeche', 'Chiapas', 'Chihuahua', 'Ciudad de Mexico',
    'Coahuila', 'Colima', 'Durango', 'Estado de Mexico', 'Guanajuato', 'Guerrero', 'Hidalgo', 'Jalisco', 'Michoacan',
    'Morelos', 'Nayarit', 'Nuevo Leon', 'Oaxaca', 'Puebla', 'Queretaro', 'Quintana Roo', 'San Luis Potosi', 'Sinaloa',
    'Sonora', 'Tabasco', 'Tamaulipas', 'Tlaxcala', 'Veracruz', 'Yucatan', 'Zacatecas'
]

# Crear un diccionario para almacenar las respuestas
responses = {}

# Título del cuestionario
st.title('Cuestionario Paciente - BioBanco')

# Formulario para todas las preguntas
with st.form(key='cuestionario_form'):
    # Pregunta 1: Fecha de entrevista
    fecha_entrevista = st.date_input('Fecha de entrevista', value=datetime.now())
    responses['Fecha de entrevista'] = fecha_entrevista.strftime('%d/%m/%Y')

    # Pregunta 2: Procedencia del paciente
    responses['Procedencia del paciente'] = st.selectbox(
        'Procedencia del paciente', 
        [
            'Consulta externa lado A',
            'Consulta externa lado B',
            'Clínica Arritmias',
            'Clínica Coagulación',
            'Clínica Valvulares',
            'Clínica Hipertensión',
            'Donador Control'
        ]
    )

    # Pregunta 3: Núm. registro INCICh
    num_registro = st.text_input('Núm. registro INCICh')
    if not num_registro.isdigit():
        st.error('El número de expediente debe ser un valor numérico.')
    else:
        responses['Núm. registro INCICh'] = int(num_registro)

    # Pregunta 4: Nombre del paciente
    responses['Nombre del paciente'] = st.text_input('Nombre del paciente')

    # Pregunta 5: Fecha de nacimiento
    fecha_nacimiento = st.date_input('Fecha de nacimiento', min_value=datetime(1920, 1, 1), max_value=datetime.now())
    responses['Fecha de nacimiento'] = fecha_nacimiento.strftime('%d/%m/%Y')

    # Cálculo de la edad
    hoy = datetime.now()
    edad = hoy.year - fecha_nacimiento.year - ((hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
    responses['Edad actual (años)'] = edad

    # Pregunta 7: Género
    responses['Género'] = st.selectbox('Género', ['Masculino', 'Femenino', 'Otro'])

    # Pregunta 8: Peso (Kg)
    peso = st.number_input('Peso (Kg)', min_value=0.0, max_value=999.9, step=0.1, format="%.1f")
    responses['Peso (Kg)'] = peso

    # Pregunta 9: Estatura (m)
    estatura = st.number_input('Estatura (m)', min_value=0.0, max_value=9.99, step=0.01, format="%.2f")
    responses['Estatura (m)'] = estatura

    # Pregunta 10: Índice de masa corporal (IMC)
    if estatura > 0:
        imc = round(peso / (estatura ** 2), 1)
    else:
        imc = 0.0
    responses['Índice de masa corporal (IMC)'] = imc

    # Pregunta 11: Circunferencia de cintura (cm)
    responses['Circunferencia de cintura (cm)'] = st.number_input('Circunferencia de cintura (cm)', min_value=0.0, max_value=999.9, step=0.1, format="%.1f")

    # Pregunta 12: Tensión arterial Sistólica (mmHg)
    responses['Tensión arterial Sistólica (mmHg)'] = st.number_input('Tensión arterial Sistólica (mmHg)', min_value=0, max_value=999, step=1)

    # Pregunta 13: Tensión arterial Diastólica (mmHg)
    responses['Tensión arterial Diastólica (mmHg)'] = st.number_input('Tensión arterial Diastólica (mmHg)', min_value=0, max_value=999, step=1)

    # Pregunta 14: Frecuencia cardiaca (lpm)
    responses['Frecuencia cardiaca (lpm)'] = st.number_input('Frecuencia cardiaca (lpm)', min_value=0, max_value=999, step=1)

    # Pregunta 15: Grupo étnico al que pertenece
    responses['Grupo étnico al que pertenece.'] = st.selectbox('Grupo étnico al que pertenece.', ['Otro', 'Mestizo', 'Pueblo indígena', 'Caucásico', 'Afrodescendiente'])

    # Pregunta 16: ¿Dónde nació su abuelo materno?
    responses['¿Dónde nació su abuelo materno?'] = st.selectbox('¿Dónde nació su abuelo materno?', estados_mexico)

    # Pregunta 16.1: ¿Dónde nació su abuela materna?
    responses['¿Dónde nació su abuela materna?'] = st.selectbox('¿Dónde nació su abuela materna?', estados_mexico)

    # Pregunta 17: ¿Dónde nació su abuelo paterno?
    responses['¿Dónde nació su abuelo paterno?'] = st.selectbox('¿Dónde nació su abuelo paterno?', estados_mexico)

    # Pregunta 17.1: ¿Dónde nació su abuela paterna?
    responses['¿Dónde nació su abuela paterna?'] = st.selectbox('¿Dónde nació su abuela paterna?', estados_mexico)

    # Pregunta 18: ¿Dónde nació su padre?
    responses['¿Dónde nació su padre?'] = st.selectbox('¿Dónde nació su padre?', estados_mexico)

    # Pregunta 18.1: ¿Dónde nació su madre?
    responses['¿Dónde nació su madre?'] = st.selectbox('¿Dónde nació su madre?', estados_mexico)

    # Pregunta 19: ¿Dónde nació usted?
    responses['¿Dónde nació usted?'] = st.selectbox('¿Dónde nació usted?', estados_mexico)

    # Pregunta 20: ¿Tuvo o tiene familiar con alguna de las siguientes enfermedades?
    responses['¿Tuvo o tiene familiar con alguna de las siguientes enfermedades?'] = st.selectbox(
        '¿Tuvo o tiene familiar con alguna de las siguientes enfermedades?', 
        ['Ninguna', 'Angina inestable', 'Angina estable', 'Cardiopatía congénita', 'Valvulopatía', 'Cardiopatía pulmonar', 
         'Arritmia cardiaca', 'Coágulos sanguíneos', 'Hipertensión sistémica', 'Dislipidemia', 'Diabetes', 
         'Hiperuricemia', 'Tabaquismo', 'Sobrepeso', 'Cardiopatía Isquémica']
    )

    # Pregunta 21: ¿Quién?
    responses['¿Quién?'] = st.selectbox('¿Quién?', ['Madre', 'Padre', 'Ambos', 'Hermano(a)', 'Ninguno'])

    # Pregunta 22: ¿Fuma actualmente?
    responses['¿Fuma actualmente?'] = st.selectbox('¿Fuma actualmente?', ['Sí', 'No', 'No sabe'])

    # Pregunta 23: En los últimos 3 meses ¿ha consumido alguna bebida que contenga alcohol?
    responses['En los últimos 3 meses ¿ha consumido alguna bebida que contenga alcohol?'] = st.selectbox(
        'En los últimos 3 meses ¿ha consumido alguna bebida que contenga alcohol?', ['Sí', 'No', 'No sabe']
    )

    # Pregunta 24: ¿El paciente tiene exceso de peso?
    if imc > 25:
        responses['¿El paciente tiene exceso de peso?'] = 'Sí'
    else:
        responses['¿El paciente tiene exceso de peso?'] = 'No'

    # Pregunta 25: ¿El paciente tiene diabetes?
    responses['¿El paciente tiene diabetes?'] = st.selectbox('¿El paciente tiene diabetes?', ['Sí', 'No', 'No sabe'])


    # Pregunta 25: ¿El paciente tiene diabetes?
    responses['¿El paciente tiene dislipidemia?'] = st.selectbox('¿El paciente tiene dislipidemia?', ['Sí', 'No', 'No sabe'])

    # Pregunta 26: ¿Le han indicado medicamento(s) para controlar su diabetes?
    responses['¿Le han indicado medicamento(s) para controlar su diabetes?'] = st.selectbox(
        '¿Le han indicado medicamento(s) para controlar su diabetes?', ['Sí', 'No', 'No sabe']
    )

    # Pregunta 27: ¿El paciente tiene hipertensión arterial?
    responses['¿El paciente tiene hipertensión arterial?'] = st.selectbox('¿El paciente tiene hipertensión arterial?', ['Sí', 'No', 'No sabe'])

    # Pregunta 28: ¿Le han indicado medicamentos para controlar la presión?
    responses['¿Le han indicado medicamentos para controlar la presión?'] = st.selectbox(
        '¿Le han indicado medicamentos para controlar la presión?', ['Sí', 'No', 'No sabe'], key='medicamentos_presion'
    )

    # Pregunta 29: ¿Tiene usted antecedentes de problemas cardíacos?
    responses['¿El paciente firmó el consentimiento informado para participar como donador del Biobanco del INCICh?'] = st.selectbox(
        '¿Firmó  el paciente  el consentimiento informado?', ['Sí', 'No'], key='firma_consentimiento'
    )

    # Pregunta 30: ¿Toma usted algún medicamento para los lípidos?
    responses['¿Toma usted algún medicamento para los lípidos?'] = st.selectbox(
        '¿Toma usted algún medicamento para los lípidos?', ['Sí', 'No', 'No sabe'], key='medicamento_lipicos'
    )

    # Pregunta 4: Nombre del paciente
    responses['Identificación de la muestra'] = st.text_input('Identificación de la muestra')

    # Pregunta 31: Correo electrónico
    email = st.text_input('Proporcione el correo electrónico del donante:')
    responses['Correo electrónico'] = email

    # Botón para enviar las respuestas
    submit_button = st.form_submit_button(label='Guardar Respuestas')
    # Botón para salir sin guardar
    cancel_button = st.form_submit_button(label='Salir sin Guardar')

# Al hacer clic en "Guardar Respuestas"
if submit_button:
    if not num_registro.isdigit():
        st.error('El número de expediente debe ser un valor numérico.')
    else:
        if '' in responses.values() or any(pd.isna(val) for val in responses.values()):
            st.error('Por favor, responda todas las preguntas antes de guardar.')
        else:
            responses_df = pd.DataFrame([responses])
            individual_excel_file = f'registro_{responses["Núm. registro INCICh"]}.xlsx'
            responses_df.to_excel(individual_excel_file, index=False)

            with FileLock(lock_file):
                if os.path.exists(acumulado_excel_file):
                    existing_data = pd.read_excel(acumulado_excel_file)
                    existing_data = existing_data.loc[:, ~existing_data.columns.duplicated()]
                    new_data = pd.concat([existing_data, responses_df], ignore_index=True)
                    columns_order = ['Fecha de entrevista', 'Nombre del paciente'] + [col for col in new_data.columns if col not in ['Fecha de entrevista', 'Nombre del paciente']]
                    new_data = new_data[columns_order]
                else:
                    new_data = responses_df
                new_data.to_excel(acumulado_excel_file, index=False, engine='openpyxl')
                st.success('Las respuestas han sido guardadas exitosamente.')

            # Verificar si el correo es 'polanco@unam.mx' y permitir descarga
            if email.strip().lower() == 'polanco@unam.mx':
                st.success('Correo electrónico validado: polanco@unam.mx')
                with open(acumulado_excel_file, 'rb') as file:
                    st.download_button(
                        label='Descargar archivo Excel acumulado',
                        data=file,
                        file_name=acumulado_excel_file,
                        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                    )

# Al hacer clic en "Salir sin Guardar"
if cancel_button:
    st.warning('Para salir sin guardar cierre la aplicación.')
    st.stop()  # Detiene la ejecución del programa

