import streamlit as st
import utils.sidebar as sb
import pandas as pd
import joblib
import time
import datetime

st.set_page_config(
    page_title="SupplyRisk - Prediction",
    layout="centered",
    page_icon="🤖")

sb.show_sidebar()

st.markdown('<h1 style="background-color: rgb(96, 180, 255); color: white; padding: 5px; border-radius: 5px; text-align: center;">Detección de Envío Tardío</h1>',
            unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)


st.title("Formulario de Envío")

hours = list(range(0, 24))
cities = ["Annapolis", "Hanford", "Cerritos", "Norfolk", "Alpharetta", "New Bedford", "Gwynn Oak", "Granada Hills", "Littleton", "Westland",
          "Springfield", "Doylestown", "Glendale", "Billings", "Rego Park", "San Ramon", "Fort Worth", "San Pablo", "Alhambra", "San Bernardino",
          "Campbell", "Washington", "Lynnwood", "Wayne", "West Jordan", "Katy", "Asheboro", "Fremont", "New Haven", "Sanford",
          "Weslaco", "Modesto", "Cincinnati", "Grand Prairie", "Forest Hills", "Bellingham", "Hamtramck", "Stamford", "Cumberland", "Arecibo",
          "Elyria", "Gardena", "Salinas", "Hacienda Heights", "Lutz", "Pekin", "Highland Park", "Irvington", "Lombard", "Panorama City",
          "Greensburg", "Orlando", "Fullerton", "Mesa", "Pittsburg", "Apex", "Potomac", "Richmond", "Oxnard", "Carrollton",
          "Williamsport", "La Mirada", "Lewisville", "New Orleans", "Lawrenceville", "Bend", "Huntington Station", "North Tonawanda", "Lakewood", "Beaverton",
          "Plainfield", "Hamilton", "Jersey City", "Diamond Bar", "Aguadilla", "Edinburg", "Hampton", "Indio", "Trujillo Alto", "Albany",
          "Chapel Hill", "San Jose", "Norwalk", "Toa Baja", "Kenner", "Hayward", "Middletown", "Silver Spring", "New Braunfels", "Columbia",
          "Union", "Augusta", "Far Rockaway", "South Richmond Hill", "West Lafayette", "San Francisco", "Cicero", "Webster", "South Ozone Park", "Hickory",
          "Chula Vista", "Peoria", "Cary", "Dubuque", "Marrero", "Santa Maria", "Jacksonville", "Colorado Springs", "Ponce", "Bayamon",
          "Moline", "Perth Amboy", "Crystal Lake", "Reynoldsburg", "Mayaguez", "Medford", "Federal Way", "Costa Mesa", "Strongsville", "Pomona",
          "Wyoming", "El Monte", "Wheeling", "Lynn", "Lodi", "La Puente", "Enfield", "Passaic", "Blacksburg", "Saint Charles",
          "Compton", "Opelousas", "Allentown", "Piscataway", "Livermore", "Napa", "Clovis", "Hialeah", "Salt Lake City", "Germantown",
          "La Mesa", "Chambersburg", "Toms River", "San Diego", "Pasadena", "Tustin", "Murfreesboro", "Madison", "Del Rio", "Stockbridge",
          "Algonquin", "Kent", "Morganton", "Longview", "Bismarck", "Dayton", "Canton", "Fort Washington", "Dorchester Center", "Jonesboro",
          "Fountain Valley", "Mission Viejo", "Hesperia", "Winnetka", "Bristol", "Arlington", "Garden Grove", "Las Vegas", "Michigan City", "Zanesville",
          "Normal", "Santa Cruz", "Powder Springs", "Poway", "Lindenhurst", "Knoxville", "North Richland Hills", "Victorville", "Birmingham", "Eugene",
          "Glen Burnie", "Morristown", "Taylor", "Ypsilanti", "Santa Clara", "Chicago", "East Brunswick", "Buena Park", "Pacoima", "Baldwin Park", "Portland",
          "Laguna Hills", "El Paso", "Massillon", "Sylmar", "San Pedro", "Seattle", "Taunton", "Bell Gardens", "North Hollywood",
          "Westerville", "San Juan", "West Haven", "Beloit", "Scottsdale", "Anaheim", "West New York", "Bloomfield", "Rochester", "South El Monte"
          "Moreno Valley", "Hagerstown", "Lilburn", "Colton", "Summerville", "Dundalk", "Reno", "Catonsville", "Encinitas", "North Hills",
          "Huntington Park", "Stafford", "Long Beach", "Vista", "Sheboygan", "Endicott", "Placentia", "Sugar Land", "Raleigh", "Clearfield",
          "Decatur", "Ann Arbor", "Frankfort", "Provo", "Daly City", "Redmond", "Saint Paul", "Marietta", "Woodbridge", "Azusa",
          "Granite City", "York", "Guayama", "Mount Pleasant", "Tonawanda", "Phoenix", "Elgin", "Revere", "Oceanside", "Cypress",
          "Kaneohe", "Danbury", "New Brunswick", "Bountiful", "Bay Shore", "Bronx", "Oak Lawn", "Manchester", "Round Rock", "Brockton",
          "Upland", "Rialto", "Mechanicsburg", "Mentor", "Tampa", "Sunnyvale", "Chicago Heights", "Everett", "Pompano Beach", "New Albany",
          "San Marcos", "Lockport", "Pharr", "Albuquerque", "Reseda", "Bridgeton", "Amarillo", "Santa Fe", "Valrico", "Saint Peters",
          "Bensalem", "Apopka", "Bakersfield", "Rancho Cordova", "Marion", "Aurora", "Milpitas", "Roseburg", "Carolina", "Brownsville",
          "Fond Du Lac", "Ontario", "Baltimore", "Berwyn", "Tracy", "Denver", "Ewa Beach", "Chillicothe", "Escondido", "Orange Park",
          "Union City", "Rock Hill", "Alameda", "West Covina", "Newburgh", "Citrus Heights", "Palmdale", "Lenoir", "Tempe", "Martinsburg",
          "Cleveland", "Davis", "Henderson", "College Station", "Bayonne", "Jackson", "Metairie", "Milwaukee", "South San Francisco", "Howell",
          "Meridian", "North Bergen", "Lawton", "Wyandotte", "Austin", "Stockton", "Pawtucket", "Jackson Heights", "Henrico"]

with st.form("shipping_form"):
    # Shipping Mode
    shipping_mode = st.selectbox("Modo de envío", [
        "Second Class", "Standard Class", "First Class", "Same Day"
    ])

    # Customer Store City
    customer_store_city = st.selectbox(
        "Ciudad de la tienda del cliente", cities, index=0)

    # Order Country
    order_country = st.selectbox("Pais de la oden", [
        "Indonesia", "Bangladesh", "Suazilandia", "Venezuela", "Cameroon", "Luxembourg", "Perú", "Singapur",
        "República Centroafricana", "Montenegro", "Uganda", "Jordan", "Cambodia", "Ireland", "Túnez", "Laos",
        "Sri Lanka", "Finland", "Portugal", "Colombia", "Albania", "Saudi Arabia", "Cuba", "Taiwán", "Ucrania",
        "Kyrgyzstan", "Algeria", "France", "Trinidad y Tobago", "Slovakia", "Israel", "Surinam", "Ghana", "Senegal",
        "Kenya", "Malaysia", "Panamá", "Zambia", "Kuwait", "Madagascar", "Hong Kong", "República de Gambia",
        "Bosnia and Herzegovina", "Liberia", "Philippines", "Benin", "United States", "República Checa", "Guinea",
        "Cyprus", "Nigeria", "Sierra Leona", "China", "Belarus", "Armenia", "Qatar", "Polonia", "Lesotho", "Gabon",
        "Paraguay", "Australia", "Martinique", "Países Bajos", "Serbia", "República Democrática del Congo", "Angola",
        "Libya", "Bahrain", "Siria", "República Dominicana", "Spain", "Yibuti", "Pakistán", "Sáhara Occidental",
        "United Arab Emirates", "Reino Unido", "Ruanda", "Georgia", "Belgium", "Papúa Nueva Guinea", "Burundi",
        "Bhutan", "Togo", "Burkina Faso", "Tailandia", "El Salvador", "Italy", "Uruguay", "Sudán del Sur", "Rumania",
        "Germany", "Eritrea", "Canada", "South Korea", "Zimbabue", "Suiza", "Barbados", "República del Congo", "Namibia",
        "Argentina", "Slovenia", "Azerbaijan", "Rusia", "Greece", "Egypt", "Sudán", "Afghanistan", "Chad", "India",
        "Iran", "Chile", "Estonia", "Vietnam", "Omán", "Kazakhstan", "Guadeloupe", "Japan", "Ivory Coast", "Denmark",
        "Turquía", "Jamaica", "Mongolia", "Iraq", "Mauritania", "Suecia", "Mozambique", "New Zealand", "Ecuador",
        "SudAfrica", "Hungary", "Belize", "Honduras", "Norway", "Botswana", "Brazil", "Austria", "Guatemala",
        "Guinea-Bissau", "Bolivia", "Ethiopia", "Turkmenistán", "Niger", "Yemen", "Lithuania", "Bulgaria", "Croatia",
        "Mali", "Uzbekistán", "North Macedonia", "Morocco", "Moldova", "Myanmar", "Tayikistán", "Nicaragua", "Mexico",
        "Nepal", "Guyana", "Tanzania", "Lebanon", "French Guiana", "Costa Rica", "Haiti", "Equatorial Guinea", "Somalia"
    ])

    # Customer Store State
    customer_store_state = st.selectbox("Estado de la tienda del cliente", [
        "Oklahoma", "North Carolina", "Colorado", "Florida", "Delaware", "Nevada", "Louisiana", "New York",
        "West Virginia", "South Carolina", "New Jersey", "Arkansas", "Hawaii", "New Mexico", "Missouri",
        "Connecticut", "District of Columbia", "Indiana", "Iowa", "Massachusetts", "Rhode Island", "Ohio",
        "Michigan", "Minnesota", "Pennsylvania", "Washington", "Montana", "Kentucky", "Wisconsin", "Arizona",
        "Illinois", "Virginia", "Maryland", "Georgia", "Puerto Rico", "Utah", "North Dakota", "California",
        "Tennessee", "Kansas", "Oregon", "Texas", "Idaho", "Alabama"
    ], index=32)

    # Order Date
    min_date = datetime.date(2014, 1, 1)
    max_date = datetime.date(2018, 12, 31)
    default_date = datetime.date(2017, 1, 2)

    order_date = st.date_input("Fecha de la orden",
                               min_value=min_date,
                               max_value=max_date,
                               value=default_date,
                               format="DD/MM/YYYY")

    # Order Hour
    order_hour = st.selectbox("Hora de la orden", hours)

    # Payment Method
    order_payment_type = st.selectbox(
        "Método de pago", ["CASH", "DEBIT", "PAYMENT", "TRANSFER"])

    input_data = {
        'order_shipping_mode': [shipping_mode],
        'date_hour': [order_hour],
        'customer_store_city': [customer_store_city],
        'order_country': [order_country],
        'date_month': [order_date.month],
        'date_weekday': [order_date.weekday()],
        'order_payment_type': [order_payment_type]
    }

    X = pd.DataFrame(input_data)

    # Botón de envío
    submitted = st.form_submit_button("Enviar")

    if submitted:
        model = joblib.load("./src/models/model_deploy.pkl")
        input_data = {
            'order_shipping_mode': [shipping_mode],
            'date_hour': [order_hour],
            'customer_store_city': [customer_store_city],
            'order_country': [order_country],
            'customer_store_state': [customer_store_state],
            'date_month': [order_date.month],
            'date_weekday': [order_date.weekday()],
            'order_payment_type': [order_payment_type]
        }
        X = pd.DataFrame(input_data)
        with st.spinner("Procesando la predicción..."):
            time.sleep(2)
            prediction = model.predict(X)
            if prediction[0] == 1:
                st.markdown(
                    "### Predicción del modelo: :red[Alto riesgo entrega tardía]")
            else:
                st.markdown(
                    "### Predicción del modelo: :green[Sin riesgo entrega tardía]")
