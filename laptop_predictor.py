import joblib
import pandas as pd
import streamlit as st

model_filename = 'gradient_boosting_model.joblib'
best_model = joblib.load(model_filename)

expected_feature_names = [
    'Inches', 'Ram', 'Weight', 'ScreenW', 'ScreenH', 'CPU_freq',
    'TypeName_TypeName_2 in 1 Convertible', 'TypeName_TypeName_Gaming',
    'TypeName_TypeName_Netbook', 'TypeName_TypeName_Notebook',
    'TypeName_TypeName_Ultrabook', 'TypeName_TypeName_Workstation',
    'Screen_Screen_4K Ultra HD', 'Screen_Screen_Full HD',
    'Screen_Screen_Quad HD+', 'Screen_Screen_Standard',
    'CPU_model_grouped_CPU_model_grouped_Celeron Dual Core N3060',
    'CPU_model_grouped_CPU_model_grouped_Celeron Dual Core N3350',
    'CPU_model_grouped_CPU_model_grouped_Core i3 6006U',
    'CPU_model_grouped_CPU_model_grouped_Core i3 7100U',
    'CPU_model_grouped_CPU_model_grouped_Core i5 6200U',
    'CPU_model_grouped_CPU_model_grouped_Core i5 7200U',
    'CPU_model_grouped_CPU_model_grouped_Core i5 7300HQ',
    'CPU_model_grouped_CPU_model_grouped_Core i5 8250U',
    'CPU_model_grouped_CPU_model_grouped_Core i7 6500U',
    'CPU_model_grouped_CPU_model_grouped_Core i7 6700HQ',
    'CPU_model_grouped_CPU_model_grouped_Core i7 7500U',
    'CPU_model_grouped_CPU_model_grouped_Core i7 7700HQ',
    'CPU_model_grouped_CPU_model_grouped_Core i7 8550U',
    'CPU_model_grouped_CPU_model_grouped_Other'
]

def get_user_input():
    st.title("💻 Laptop Price Prediction Tool")

    st.markdown(""" 🛠 What Does This Tool Do?
    This tool helps you estimate the **price of a laptop** based on several key features, such as:
    - Screen size, resolution, and type
    - RAM and weight
    - CPU model and frequency

    Simply fill in the details below and click **Predict Price** to see the estimated price!""")

    TypeName = st.selectbox("Type of Laptop", [
        'TypeName_2 in 1 Convertible', 'TypeName_Gaming', 'TypeName_Netbook', 
        'TypeName_Notebook', 'TypeName_Ultrabook', 'TypeName_Workstation'
    ])
    Screen = st.selectbox("Screen Type", [
        'Screen_4K Ultra HD', 'Screen_Full HD', 'Screen_Quad HD+', 'Screen_Standard'
    ])
    CPU_model_grouped = st.selectbox("CPU Model", [
        'CPU_model_grouped_Celeron Dual Core N3060', 'CPU_model_grouped_Celeron Dual Core N3350', 
        'CPU_model_grouped_Core i3 6006U', 'CPU_model_grouped_Core i3 7100U', 
        'CPU_model_grouped_Core i5 6200U', 'CPU_model_grouped_Core i5 7200U', 
        'CPU_model_grouped_Core i5 7300HQ', 'CPU_model_grouped_Core i5 8250U', 
        'CPU_model_grouped_Core i7 6500U', 'CPU_model_grouped_Core i7 6700HQ', 
        'CPU_model_grouped_Core i7 7500U', 'CPU_model_grouped_Core i7 7700HQ', 
        'CPU_model_grouped_Core i7 8550U', 'CPU_model_grouped_Other'
    ])

    Inches = st.number_input("Screen Size (Inches)", min_value=10.0, max_value=18.0, value=14.0, step=0.1)
    Ram = st.number_input("RAM (GB)", min_value=2, max_value=16, value=8, step=1)
    Weight = st.number_input("Weight (kg)", min_value=0.5, max_value=3.5, value=1.5, step=0.1)
    ScreenW = st.number_input("Screen Width (cm)", min_value=1366.0, max_value=3840.0, value=1920.0, step=10.0)
    ScreenH = st.number_input("Screen Height (cm)", min_value=768.0, max_value=2160.0, value=1080.0, step=10.0)
    CPU_freq = st.number_input("CPU Frequency (GHz)", min_value=0.5, max_value=4.0, value=2.5, step=0.1)

    user_data = {
        'Inches': [Inches],
        'Ram': [Ram],
        'Weight': [Weight],
        'ScreenW': [ScreenW],
        'ScreenH': [ScreenH],
        'CPU_freq': [CPU_freq],
    }

    user_data[f'TypeName_{TypeName}'] = [1]
    user_data[f'Screen_{Screen}'] = [1]
    user_data[f'CPU_model_grouped_{CPU_model_grouped}'] = [1]

    for col in expected_feature_names:
        if col not in user_data:
            user_data[col] = [0]

    user_data_df = pd.DataFrame(user_data)

    user_data_df = user_data_df[expected_feature_names]

    return user_data_df, TypeName

user_data, TypeName = get_user_input()

def get_laptop_image(type_name):
    image_map = {
        'TypeName_2 in 1 Convertible': '2in1.png',
        'TypeName_Gaming': 'gaming.png',
        'TypeName_Netbook': 'netbook.jpg',
        'TypeName_Notebook': 'notebook.jpg',
        'TypeName_Ultrabook': 'ultrabook.png',
        'TypeName_Workstation': 'workstation.png',
    }
    return image_map.get(type_name, 'notebook.jpg')

if st.button("Predict Price", help="Click to predict the laptop price based on entered specifications"):
    predicted_price = best_model.predict(user_data)
    st.markdown(f"### Predicted Price: €{predicted_price[0]:.2f}")
    st.success(f"The predicted price for this laptop is: €{predicted_price[0]:.2f}")
    
    image_path = get_laptop_image(TypeName)
    st.image(image_path, caption=f"Image of {TypeName}", use_container_width=True)
