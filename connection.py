import requests

class Connection():
    # Your Firebase Realtime Database URL
    def __init__(self) -> None:
        self.firebase_url = 'https://pygame-4ec45-default-rtdb.asia-southeast1.firebasedatabase.app/'
    # GET    
    def get_data(self, path):
        response = requests.get(self.firebase_url + path)
        if response.status_code == 200:
            data = response.json()
            print("Data from Firebase:")
            # print(data)
            return data
        else:
            print("Error:", response.text)
    # POST
    def store_data(self, path, json):
        response = requests.post(self.firebase_url + path, json=json)
        if response.status_code == 200:
            print("Data successfully sent to Firebase!")
        else:
            print("Error:", response.text)
    # PATCH
    def update_data(self, path, new_data):
        response = requests.patch(self.firebase_url + path, json=new_data)
        if response.status_code == 200:
            print("Data updated successfully!")
        else:
            print("Error:", response.text)
    # Delete
    def delete_data(self, path, data):
        response = requests.delete(self.firebase_url + path)
        if response.status_code == 200:
            print("Old key deleted successfully!")
        else:
            print("Error deleting old key:", response.text)
    # Update played_time
    def update_played(self, path):
        response = requests.get(self.firebase_url + path)
        if response.status_code == 200:
            data = response.json()
            print("Data from Firebase:")
            print(data)
            if 'played_time' in data:
                data['played_time'] += 1
                response = requests.patch(self.firebase_url + path, json=data)
                if response.status_code == 200:
                    print("Played updated successfully", data['played_time'])
                else:
                    print("Error updating played_time:", response.text)
        else:
            print("Error:", response.text)
    # Update highest score
    def update_highest_score(self, path, score):
        response = requests.get(self.firebase_url + path)
        if response.status_code == 200:
            data = response.json()
            if 'score' in data:
                if data['score'] < score:
                    response = requests.patch(self.firebase_url + path, json=data)
                    if response.status_code == 200:
                        print("Played updated successfully", data['played_time'])
                    else:
                        print("Error updating played_time:", response.text)
        else:
            print("Error:", response.text)

firebase = Connection()

# Example
# name = 'gege'
# data = {
#     'name': name,
#     'played_time': 0,
#     'tel': '0877777777',
#     'score': 0
# }
# path = f'users_score/{name}.json' # user_ref
# user_number = 1
# firebase.store_data(path, data)
# firebase.get_data(path)
# firebase.update_data(path, data)
# firebase.update_played(path)
