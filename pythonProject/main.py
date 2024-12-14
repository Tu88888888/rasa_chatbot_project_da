from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def hello():
    if request.method == "GET":
        # Initial render when accessing the page
        return render_template('index.html', noidungchathientai="")
    else:
        # Safely retrieve form data
        user_message = request.form.get('user_message', "").strip()  # Default to empty string if not provided
        noidungchathientai = request.form.get('chat_content', "").strip()  # Default to empty string if not provided

        # Check if the user_message is empty
        if not user_message:
            return render_template('index.html', noidungchathientai=noidungchathientai + "\n[ERROR]: Message cannot be empty.")

        # Send the user message to the Rasa bot
        try:
            r = requests.post(
                'http://127.0.0.1:5005/webhooks/rest/webhook',
                json={"sender": "test", "message": user_message},
                timeout=5  # Timeout to avoid long waits
            )
            if r.status_code == 200 and r.json():
                bot_response = r.json()[0].get("text", "No response text found.")
            else:
                bot_response = "Sorry, I couldn't get a valid response from the bot."
        except requests.exceptions.RequestException as e:
            bot_response = f"Error connecting to the bot: {e}"
        # Update chat content with user and bot messages
        noidungchathientai += f"\n[BẠN]: {user_message}\n[BOT]: {bot_response}"
        # Return the updated chat content
        return render_template('index.html', noidungchathientai=noidungchathientai)


# Run the Flask server


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
