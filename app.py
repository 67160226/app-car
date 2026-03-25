import streamlit as st
import pandas as pd
import joblib

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Cardekho Price Predictor", page_icon="🏎️", layout="centered")

# --- 🎨 ส่วนตกแต่งธีมเว็บ (Future Dark / Neon Blue Theme) ---
st.markdown("""
<style>
    /* 1. โหลด Font 'Exo 2' จาก Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Exo+2:wght@300;400;700&display=swap');

    /* สั่งให้ใช้ Exo 2 กับตัวหนังสือทั้งหมด */
    html, body, [class*="css"], .stMarkdown, .stSelectbox label, .stNumberInput label {
        font-family: 'Exo 2', sans-serif !important;
    }

    /* 2. สีพื้นหลังหลักของเว็บ */
    .stApp {
        background-color: #080F1F !important; 
        color: #F0F2F6 !important; 
    }
    
    /* 3. ตกแต่งส่วนบน */
    .header-container {
        text-align: center;
        margin-bottom: 25px;
    }

    .glow-title {
        color: #00E5FF !important; 
        font-size: 3.2rem !important;
        font-weight: 700 !important;
        text-shadow: 0px 0px 10px #00E5FF, 0px 0px 20px #00E5FF !important; 
        margin-bottom: 10px !important;
    }

    .info-bar {
        background-color: #141A29; 
        border: 1px solid #2B334D;
        border-radius: 8px;
        padding: 10px;
        display: flex;
        justify-content: center; 
        gap: 20px; 
        margin-bottom: 20px;
    }

    .info-item {
        color: #E0E1DD;
        font-size: 1rem;
    }
    .info-highlight {
        color: #00E5FF !important; 
        font-weight: bold;
    }

    /* ตกแต่ง Divider Icon */
    .divider-container {
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 30px;
    }
    .divider-line {
        flex: 1;
        height: 1px;
        background-color: #2B334D;
    }
    .divider-icon {
        color: #3A506B; 
        font-size: 1.5rem;
        margin: 0 15px;
    }

    /* สีของกล่อง Form */
    div[data-testid="stForm"] {
        background-color: #141A29 !important; 
        border: 2px solid #2B334D !important; 
        border-radius: 12px !important;
        padding: 25px !important;
        box-shadow: 0px 0px 15px #2B334D !important; 
    }

    /* สีของหัวข้อใน Form */
    h2, h3, .stSubheader {
        color: #00E5FF !important; 
        text-shadow: 0px 0px 5px #00E5FF !important; 
    }

    /* ปุ่มประเมินราคา */
    div[data-testid="stFormSubmitButton"] > button {
        background-color: #00E5FF !important;
        color: #080F1F !important;
        font-weight: bold;
        font-size: 19px !important;
        border-radius: 10px !important;
        border: none !important;
        transition: 0.3s !important;
        box-shadow: 0px 0px 15px #00E5FF !important;
        width: 100% !important;
        margin-top: 10px;
    }
    div[data-testid="stFormSubmitButton"] > button:hover {
        background-color: #2B334D !important;
        color: #00E5FF !important;
        border: 1px solid #00E5FF !important;
        box-shadow: 0px 0px 20px #00E5FF !important;
    }
</style>
""", unsafe_allow_html=True)

# 1. โหลดโมเดล
@st.cache_resource
def load_model():
    try:
        model = joblib.load('car_price_model.pkl')
        return model
    except FileNotFoundError:
        st.error("❌ ไม่พบไฟล์ car_price_model.pkl กรุณาตรวจสอบว่ามีไฟล์นี้อยู่ในโฟลเดอร์เดียวกับ app.py")
        st.stop()

model = load_model()

# 2. ส่วนหัวของเว็บ
st.markdown('<div class="header-container">', unsafe_allow_html=True)
st.markdown('<p class="glow-title">🏎️ AI Car Price Predictor</p>', unsafe_allow_html=True)

# แถบบอกข้อมูลโมเดล (Hardcoded จากผลการเทรนของเรา)
st.markdown('''
    <div class="info-bar">
        <span class="info-item">🚗 Model: <span class="info-highlight">Random Forest</span></span>
        <span class="info-item">📊 Accuracy: <span class="info-highlight">93.7%</span></span>
    </div>
''', unsafe_allow_html=True)

st.markdown('''
    <div class="divider-container">
        <div class="divider-line"></div>
        <div class="divider-icon">⇓</div>
        <div class="divider-line"></div>
    </div>
''', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.write("กรอกข้อมูลรถยนต์ของคุณด้านล่าง เพื่อให้ AI ช่วยประเมินราคาขายที่เหมาะสม (หน่วย: รูปีอินเดีย)")

# 3. ฟอร์มรับข้อมูล
with st.form("car_price_form"):
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📝 ข้อมูลพื้นฐาน")
        brand = st.selectbox("ยี่ห้อรถ", ['Maruti', 'Hyundai', 'Honda', 'Toyota', 'Ford', 'Volkswagen', 'Mahindra', 'Tata', 'Renault', 'Chevrolet', 'Nissan', 'Datsun', 'Fiat'])
        vehicle_age = st.number_input("อายุรถ (ปี)", min_value=0, max_value=30, value=5)
        km_driven = st.number_input("เลขไมล์ (กิโลเมตร)", min_value=0, value=50000, step=1000)
        seller_type = st.selectbox("ประเภทผู้ขาย", ['Individual', 'Dealer', 'Trustmark Dealer'])

    with col2:
        st.subheader("⚙️ สเปกเครื่องยนต์")
        fuel_type = st.selectbox("ประเภทเชื้อเพลิง", ['Petrol', 'Diesel', 'CNG', 'LPG', 'Electric'])
        transmission_type = st.selectbox("ระบบเกียร์", ['Manual', 'Automatic'])
        engine = st.number_input("ขนาดเครื่องยนต์ (CC)", min_value=500, max_value=6000, value=1500, step=100)
        max_power = st.number_input("แรงม้า (BHP)", min_value=20.0, max_value=600.0, value=100.0, step=5.0)
        mileage = st.number_input("อัตราสิ้นเปลือง (km/l)", min_value=5.0, value=15.0, step=1.0)
        seats = st.selectbox("จำนวนที่นั่ง", [2, 4, 5, 6, 7, 8, 9, 10], index=2)

    # ปุ่มกดคำนวณราคา
    submitted = st.form_submit_button("🔮 ประเมินราคาด้วย AI")

# 4. ส่วนแสดงผลลัพธ์
if submitted:
    # เตรียมข้อมูลสำหรับทำนาย
    input_data = pd.DataFrame({
        'vehicle_age': [vehicle_age],
        'km_driven': [km_driven],
        'mileage': [mileage],
        'engine': [engine],
        'max_power': [max_power],
        'seats': [seats],
        'brand': [brand],
        'seller_type': [seller_type],
        'fuel_type': [fuel_type],
        'transmission_type': [transmission_type]
    })
    
    with st.spinner('กำลังคำนวณ...'):
        prediction = model.predict(input_data)[0]
    
    st.markdown("---")
    st.markdown(f"<h3 style='text-align: center;'>ราคาประเมินที่เหมาะสมคือ</h3>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='text-align: center; color: #00E5FF; text-shadow: 0px 0px 10px #00E5FF;'>₹ {prediction:,.0f} รูปี</h1>", unsafe_allow_html=True)
    st.balloons()
