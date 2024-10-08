import streamlit as st
import pandas as pd
import os
from datetime import datetime
from filelock import FileLock  # Importar FileLock
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

# Mostrar el logo
st.image("escudo_COLOR.jpg", width=100)

# Archivo Excel donde se acumularán todas las respuestas
acumulado_excel_file = 'respuestas_cuestionario_acumulado.xlsx'
lock_file = 'acumulado_excel_file.lock'  # Archivo de bloqueo

# Función para enviar el correo electrónico
def enviar_correo(destinatario, nombre, archivo_adjunto):
    smtp_server = "smtp.gmail.com"
    port = 587  # Puerto para usar TLS
    remitente = "abcdf2024dfabc@gmail.com"
    password = "hjdd gqaw vvpj hbsy"  # Tu contraseña de aplicación

    mensaje = MIMEMultipart()
    mensaje['From'] = remitente
    mensaje['To'] = destinatario
    mensaje['Subject'] = "Registro Completo"

    cuerpo = f"""\
Hola {nombre},

Estimado donante, le adjuntamos el cuestionario que le hemos efectuado. Gracias por el tiempo que dedicó a ello.

Atentamente,

Departamento del Biobanco
Instituto Nacional de Cardiología Ignacio Chávez
"""
    mensaje.attach(MIMEText(cuerpo, 'plain', 'utf-8'))

    # Adjuntar el archivo proporcionado (en este caso, Excel)
    with open(archivo_adjunto, 'rb') as attachment:
        part = MIMEApplication(attachment.read(), _subtype='vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        part.add_header('Content-Disposition', 'attachment', filename=os.path.basename(archivo_adjunto))
        mensaje.attach(part)

    # Establecer conexión segura con el servidor SMTP
    context = ssl.create_default_context()

    try:
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls(context=context)  # Iniciar una conexión segura
            server.login(remitente, password)  # Autenticarse en el servidor
            server.sendmail(remitente, destinatario, mensaje.as_string())  # Enviar el correo
        return True
    except Exception as e:
        st.error(f"Error al enviar el correo: {e}")
        return False

# Lista de estados de la República Mexicana
estados_mexico = [
    'Aguascalientes', 'Baja California', 'Baja California Sur', 'Campeche', 'Chiapas', 'Chihuahua', 'Ciudad de Mexico',
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
    responses['Fecha de entrevista'] = fecha_entrevista.strftime('%d/%m/%Y')  # Guardar solo la fecha

    # Pregunta 2: Procedencia del paciente
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

    # Pregunta 3: Núm. registro INCICh (numérico)
    num_registro = st.text_input('Núm. registro INCICh')
    if not num_registro.isdigit():
        st.error('El número de expediente debe ser un valor numérico.')
    else:
        responses['Núm. registro INCICh'] = int(num_registro)

    # Pregunta 4: Nombre del paciente
    responses['Nombre del paciente'] = st.text_input('Nombre del paciente')

    # Pregunta 5: Fecha de nacimiento
    fecha_nacimiento = st.date_input('Fecha de nacimiento', min_value=datetime(1920, 1, 1), max_value=datetime.now())
    responses['Fecha de nacimiento'] = fecha_nacimiento.strftime('%d/%m/%Y')  # Guardar solo la fecha

    # Pregunta 6: Edad actual (años)
    responses['Edad actual (años)'] = st.number_input('Edad actual (años)', min_value=0, max_value=120, step=1)

    # Pregunta 7: Género
    responses['Género'] = st.selectbox('Género', ['Masculino', 'Femenino', 'Otro'])

    # Pregunta 11: Circunferencia de cintura (cm)
    responses['Circunferencia de cintura (cm)'] = st.number_input('Circunferencia de cintura (cm)', min_value=0.0, max_value=999.9, step=0.1, format="%.1f")

    # Pregunta 12: Tensión arterial Sistólica (mmHg)
    responses['Tensión arterial Sistólica (mmHg)'] = st.number_input('Tensión arterial Sistólica (mmHg)', min_value=0, max_value=999, step=1)

    # Pregunta 13: Tensión arterial Diastólica (mmHg)
    responses['Tensión arterial Diastólica (mmHg)'] = st.number_input('Tensión arterial Diastólica (mmHg)', min_value=0, max_value=999, step=1)

    # Pregunta 14: Frecuencia cardiaca (lpm)
    responses['Frecuencia cardiaca (lpm)'] = st.number_input('Frecuencia cardiaca (lpm)', min_value=0, max_value=999, step=1)

    # Pregunta 15: Grupo étnico al que pertenece.
    responses['Grupo étnico al que pertenece.'] = st.selectbox('Grupo étnico al que pertenece.', ['Mestizo', 'Pueblo indígena', 'Caucásico', 'Afrodescendiente'])

    # Pregunta 16: ¿Dónde nacieron sus abuelos Maternos?
    responses['¿Dónde nacieron sus abuelos Maternos?'] = st.selectbox('¿Dónde nacieron sus abuelos Maternos?', estados_mexico)

    # Pregunta 17: ¿Dónde nacieron sus abuelos Paternos?
    responses['¿Dónde nacieron sus abuelos Paternos?'] = st.selectbox('¿Dónde nacieron sus abuelos Paternos?', estados_mexico)

    # Pregunta 18: ¿Dónde nacieron sus padres?
    responses['¿Dónde nacieron sus padres?'] = st.selectbox('¿Dónde nacieron sus padres?', estados_mexico)

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
    responses['¿El paciente tiene exceso de peso?'] = st.selectbox('¿El paciente tiene exceso de peso?', ['Sí', 'No', 'No sabe'])

    # Pregunta 25: ¿El paciente tiene diabetes?
    responses['¿El paciente tiene diabetes?'] = st.selectbox('¿El paciente tiene diabetes?', ['Sí', 'No', 'No sabe'])

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
    responses['¿Tiene usted antecedentes de problemas cardíacos?'] = st.selectbox(
        '¿Tiene usted antecedentes de problemas cardíacos?', ['Sí', 'No', 'No sabe'], key='problemas_cardiacos'
    )

    # Pregunta 30: ¿Toma usted algún medicamento para el colesterol?
    responses['¿Toma usted algún medicamento para el colesterol?'] = st.selectbox(
        '¿Toma usted algún medicamento para el colesterol?', ['Sí', 'No', 'No sabe'], key='medicamento_colesterol'
    )

    # Pregunta 31: Correo electrónico
    email = st.text_input('Proporcione el correo electrónico del donante:')
    responses['Correo electrónico'] = email

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

    # Mostrar el IMC calculado en tiempo real
    st.write(f"Su Índice de Masa Corporal (IMC) es: {imc}")

    # Guardar la respuesta en el diccionario
    responses['Índice de masa corporal (IMC)'] = imc

    # Botón para enviar las respuestas
    submit_button = st.form_submit_button(label='Guardar Respuestas')

# Al hacer clic en "Guardar Respuestas"
if submit_button:
    # Verificar que el número de expediente sea numérico antes de continuar
    if not num_registro.isdigit():
        st.error('El número de expediente debe ser un valor numérico.')
    else:
        # Verificar que todas las respuestas hayan sido completadas
        if '' in responses.values() or any(pd.isna(val) for val in responses.values()):
            st.error('Por favor, responda todas las preguntas antes de guardar.')
        else:
            # Convertir las respuestas a un DataFrame
            responses_df = pd.DataFrame([responses])

            # Crear el archivo individual para el usuario actual
            individual_excel_file = f'registro_{responses["Núm. registro INCICh"]}.xlsx'
            responses_df.to_excel(individual_excel_file, index=False)

            # Usar FileLock para bloquear el acceso al archivo acumulado
            with FileLock(lock_file):
                # Verificar si ya existe el archivo acumulado
                if os.path.exists(acumulado_excel_file):
                    # Cargar el archivo existente
                    existing_data = pd.read_excel(acumulado_excel_file)

                    # Eliminar columnas duplicadas si existen
                    existing_data = existing_data.loc[:, ~existing_data.columns.duplicated()]

                    # Concatenar los datos
                    new_data = pd.concat([existing_data, responses_df], ignore_index=True)

                    # Reordenar las columnas para que 'Fecha de entrevista' y 'Nombre del paciente' estén al inicio
                    columns_order = ['Fecha de entrevista', 'Nombre del paciente'] + [col for col in new_data.columns if col not in ['Fecha de entrevista', 'Nombre del paciente']]
                    new_data = new_data[columns_order]

                else:
                    # Si no existe, usar las nuevas respuestas como base
                    new_data = responses_df

                # Guardar las respuestas en el archivo acumulado
                new_data.to_excel(acumulado_excel_file, index=False, engine='openpyxl')
                st.success('Las respuestas han sido guardadas exitosamente.')

            # Enviar el cuestionario individual al correo electrónico proporcionado
            if email and 'Nombre del paciente' in responses:
                if enviar_correo(email, responses['Nombre del paciente'], individual_excel_file):
                    st.success('El cuestionario ha sido enviado al correo electrónico proporcionado.')
                else:
                    st.error('No se pudo enviar el correo. Verifique la dirección de correo e inténtelo de nuevo.')

# Mostrar el botón de "Extraer archivos" si el correo electrónico es "polanco@unam.mx"
if email.strip().lower() == 'polanco@unam.mx':
    st.success('Correo electrónico validado: polanco@unam.mx')
    with open(acumulado_excel_file, 'rb') as file:
        st.download_button(
            label='Descargar archivo Excel acumulado',
            data=file,
            file_name=acumulado_excel_file,
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
