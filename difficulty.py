import csv
import json
from connection import firebase

def json_to_csv(json_file, csv_file):
    # เปิดไฟล์ JSON เพื่ออ่านข้อมูล
    # with open(json_file, 'r') as f:
    #     data = json.load(f)
    data = json_file

    # เปิดไฟล์ CSV เพื่อเขียนข้อมูล
    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)

        # เขียนหัวข้อคอลัมน์
        writer.writerow(data[0].key())

        # เขียนข้อมูลแต่ละแถว
        for row in data:
            writer.writerow(row.values())

# ระบุที่อยู่ของไฟล์ JSON และ CSV
json_file = firebase.get_data(".json")

csv_file = 'data.csv'

# เรียกใช้ฟังก์ชัน json_to_csv เพื่อแปลง JSON เป็น CSV
json_to_csv(json_file, csv_file)

print("Finished Converting JSON to CSV")

# json_file = firebase.get_data(".json")
# print(json_file)
