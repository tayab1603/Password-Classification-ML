
from flask import Flask, render_template, request
import pickle

app = Flask(__name__)

# Load trained model
with open('password_model.pkl', 'rb') as file:
    saved_data = pickle.load(file)

model = saved_data['model']

# Extract password features
def extract_features(password):

    length = len(password)

    uppercase = sum(c.isupper() for c in password)

    lowercase = sum(c.islower() for c in password)

    digits = sum(c.isdigit() for c in password)

    special = sum(not c.isalnum() for c in password)

    return [
        length,
        uppercase,
        lowercase,
        digits,
        special
    ]

@app.route('/', methods=['GET', 'POST'])
def home():

    result = None

    if request.method == 'POST':

        password = request.form.get('password', '')

        if password:

            features = extract_features(password)

            prediction = model.predict([features])[0]

            labels = {
                0: 'Weak',
                1: 'Medium',
                2: 'Strong'
            }

            result = labels[prediction]

    return render_template('index.html', result=result)


if __name__ == '__main__':
    app.run(debug=True)
