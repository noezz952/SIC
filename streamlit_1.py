import streamlit as st
import pandas as pd
import numpy as np
import pyrebase
import time
import pickle

# Konfigurasi Firebase
config = {
    "apiKey": "AIzaSyDjHeDbeIotvRUuF0XZLeiRFjKgfv-6KHo",
    "authDomain": "sensor-b15c7.firebaseapp.com",
    "databaseURL": "https://sensor-b15c7-default-rtdb.firebaseio.com",
    "projectId": "sensor-b15c7",
    "storageBucket": "sensor-b15c7.appspot.com",
    "messagingSenderId": "34611770004",
    "appId": "1:34611770004:web:278e32c3bc729717ebba81"
}

# Inisialisasi aplikasi Firebase
firebase = pyrebase.initialize_app(config)
database = firebase.database()

# Load model
filename = 'XGBC_model.pkl'
with open(filename, 'rb') as file:
    loaded_model = pickle.load(file)

st.title("HeninG! - Monitoring Kebisingan Kelas")

# Pilihan Kelas
opsi_kelas = ["XA", "XB", "XC", "XD"]
kelas = st.selectbox("Pilih Kelas:", opsi_kelas)

sensor1, sensor2, sensor3 = st.columns(3)

if 'prev_max4466' not in st.session_state:
    st.session_state.prev_max4466 = 0
if 'prev_max9814' not in st.session_state:
    st.session_state.prev_max9814 = 0
if 'prev_soundSensor' not in st.session_state:
    st.session_state.prev_soundSensor = 0

# Fungsi untuk memperbarui data
def update_data():
    max4466 = database.child("/soundLevel%20MAX4466").get().val()
    max9814 = database.child("/soundLevel%20MAX9814").get().val()
    soundSensor = database.child("sound%20Sensor").get().val()

    delta_max4466 = max4466 - st.session_state.prev_max4466
    delta_max9814 = max9814 - st.session_state.prev_max9814
    delta_soundSensor = soundSensor - st.session_state.prev_soundSensor

    st.session_state.prev_max4466 = max4466
    st.session_state.prev_max9814 = max9814
    st.session_state.prev_soundSensor = soundSensor

    with sensor1:
        st.metric(label="SoundLevel 1", value=f"{soundSensor:.2f} dB", delta=f"{delta_soundSensor:.2f} dB")
    with sensor2:
        st.metric(label="SoundLevel 2", value=f"{max4466:.2f} dB", delta=f"{delta_max4466:.2f} dB")
    with sensor3:
        st.metric(label="SoundLevel 3", value=f"{max9814:.2f} dB", delta=f"{delta_max9814:.2f} dB")
    
    # Prediksi dengan model
    bising_test = [[soundSensor, max4466, max9814]]
    data_tes = np.array(bising_test)
    y_pred = loaded_model.predict(data_tes)

    if y_pred == 1:
        st.error('Kelas berisik!!', icon="⚠️")
        st.components.v1.html('<script>alert("Peringatan: Kelas sangat berisik!");</script>', height=0)
    else:
        st.success('Kelas dalam keadaan aman.', icon="✅")

interval = 1

while True:
    update_data()
    time.sleep(interval)
    st.experimental_rerun()
