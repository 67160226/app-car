import streamlit as st
import pandas as pd
import joblib

# 1. โหลดโมเดลที่เทรนไว้
# (โปรแกรมจะหาไฟล์ car_price_model.pkl ในโฟลเดอร์เดียวกัน)
try:
    model = joblib.load('car_price_model.pkl')
except FileNotFoundError:
    st.error("ไม่พบไฟล์ car_price_model.pkl กรุณาตรวจสอบว่ามีไฟล์นี้อยู่ในโฟลเดอร์เดียวกับ app.py")
    st.stop()

# 2. ตั้งค่าหน้าเว็บ
st.title("🚗 ระบบประเมินราคารถยนต์มือสอง (Cardekho)")
st.write("กรอกข้อมูลรถยนต์ของคุณด้านล่าง เพื่อให้ AI ช่วยประเมินราคาที่เหมาะสมให้ครับ")

# 3. สร้างฟอร์มรับข้อมูลจากผู้ใช้
col1, col2 = st.columns(2)

with col1:
    # ข้อมูลตัวเลข
    vehicle_age = st.number_input("อายุรถ (ปี)", min_value=0, max_value=30, value=5)
    km_driven = st.number_input("เลขไมล์ (กิโลเมตร)", min_value=0, value=50000, step=1000)
    engine = st.number_input("ขนาดเครื่องยนต์ (CC)", min_value=500, value=1500, step=100)
    
with col2:
    # ข้อมูลตัวเลข (ต่อ)
    max_power = st.number_input("แรงม้า (BHP)", min_value=20.0, value=100.0, step=5.0)
    mileage = st.number_input("อัตราสิ้นเปลือง (km/l)", min_value=5.0, value=15.0, step=1.0)
    seats = st.selectbox("จำนวนที่นั่ง", [2, 4, 5, 6, 7, 8, 9, 10], index=2)

st.markdown("---")

col3, col4 = st.columns(2)
with col3:
    # ข้อมูลหมวดหมู่
    brand = st.selectbox("ยี่ห้อรถ", ['Maruti', 'Hyundai', 'Honda', 'Toyota', 'Ford', 'Volkswagen', 'Mahindra', 'Tata', 'Renault', 'Chevrolet', 'Nissan', 'Datsun', 'Fiat'])
    seller_type = st.selectbox("ประเภทผู้ขาย", ['Individual', 'Dealer', 'Trustmark Dealer'])

with col4:
    fuel_type = st.selectbox("ประเภทเชื้อเพลิง", ['Petrol', 'Diesel', 'CNG', 'LPG', 'Electric'])
    transmission_type = st.selectbox("ระบบเกียร์", ['Manual', 'Automatic'])

# 4. ปุ่มกดคำนวณราคา
if st.button("💰 ประเมินราคา", type="primary"):
    
    # รวบรวมข้อมูลที่กรอกมาจัดเป็น DataFrame แบบเดียวกับตอนเทรนเป๊ะๆ
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
    
    # ส่งข้อมูลเข้าโมเดลเพื่อทำนาย
    prediction = model.predict(input_data)[0]
    
    # แสดงผลลัพธ์
    st.success(f"🎉 **ราคาประเมินเบื้องต้นคือ: {prediction:,.2f} รูปี**")
    st.caption("(หมายเหตุ: ราคาที่ได้เป็นการประมาณการจากข้อมูลในอดีตเท่านั้น)")