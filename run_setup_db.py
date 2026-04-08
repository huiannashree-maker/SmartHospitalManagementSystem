from pymongo import MongoClient


def setup_database():
    try:
        # 1. Connect to MongoDB (Default local port is 27017)
        client = MongoClient("mongodb://localhost:27017/")
        db = client['hospital_db']
        doctors_collection = db['doctors']

        # 2. Clear existing data to avoid duplicates (Optional)
        doctors_collection.delete_many({})

        # 3. Your Doctor Data
        doctors_data = [
            {"name": "Dr. Smith", "age": 45, "email": "smith@hospital.com", "contact": "1234567890",
             "specialization": "Cardiologist"},
            {"name": "Dr. Sarah", "age": 38, "email": "sarah@hospital.com", "contact": "9876543210",
             "specialization": "Neurologist"},
            {"name": "Dr. Emily Chen", "age": 34, "email": "emily.chen@hospital.com", "contact": "9988776655",
             "specialization": "Pediatrician"},
            {"name": "Dr. Marcus Thorne", "age": 52, "email": "m.thorne@hospital.com", "contact": "8877665544",
             "specialization": "Orthopedic Surgeon"},
            {"name": "Dr. Elena Rodriguez", "age": 41, "email": "elena.r@hospital.com", "contact": "7766554433",
             "specialization": "Dermatologist"},
            {"name": "Dr. James Wilson", "age": 47, "email": "j.wilson@hospital.com", "contact": "6655443322",
             "specialization": "Oncologist"},
            {"name": "Dr. Linda Gray", "age": 39, "email": "linda.gray@hospital.com", "contact": "5544332211",
             "specialization": "Psychiatrist"},
            {"name": "Dr. Robert Lee", "age": 55, "email": "r.lee@hospital.com", "contact": "4433221100",
             "specialization": "Gastroenterologist"},
            {"name": "Dr. Susan Bones", "age": 36, "email": "s.bones@hospital.com", "contact": "3322110099",
             "specialization": "Radiologist"},
            {"name": "Dr. Alan Grant", "age": 49, "email": "a.grant@hospital.com", "contact": "2211009988",
             "specialization": "Endocrinologist"},
            {"name": "Dr. Monica Geller", "age": 33, "email": "m.geller@hospital.com", "contact": "1100998877",
             "specialization": "Gynecologist"},
            {"name": "Dr. Victor Fries", "age": 60, "email": "v.fries@hospital.com", "contact": "1029384756",
             "specialization": "Pulmonologist"},
            {"name": "Dr. Stephen Strange", "age": 44, "email": "s.strange@hospital.com", "contact": "5647382910",
             "specialization": "Neurosurgeon"},
            {"name": "Dr. Claire Temple", "age": 35, "email": "c.temple@hospital.com", "contact": "9182736450",
             "specialization": "General Physician"},
            {"name": "Dr. Gregory House", "age": 51, "email": "g.house@hospital.com", "contact": "8273645190",
             "specialization": "Diagnostic Specialist"},
            {"name": "Dr. Shaun Murphy", "age": 29, "email": "s.murphy@hospital.com", "contact": "7364519280",
             "specialization": "Pediatric Surgeon"},
            {"name": "Dr. Allison Cameron", "age": 37, "email": "a.cameron@hospital.com", "contact": "6451928370",
             "specialization": "Immunologist"}
        ]


        # 4. Insert into MongoDB
        result = doctors_collection.insert_many(doctors_data)
        print(f"Success! Inserted {len(result.inserted_ids)} doctor records.")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    setup_database()