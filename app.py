# Install these first if not installed
# pip install flask requests

from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

# --- Your Azure Keys and Endpoints ---
SPEECH_KEY = "D0T35pP14CsCSF21Axy37sUXZWMaAvdCuwGbXcNTCHrAXPeoMwtRJQQJ99BDACYeBjFXJ3w3AAAYACOGjaAn"
SPEECH_ENDPOINT = "https://eastus.api.cognitive.microsoft.com/"
VISION_KEY = "CUNrSkv6j6WJAlCXlsz6PEiMTFUeN2C6NwKDTHNIEk55mIli5uJiJQQJ99BDACYeBjFXJ3w3AAAFACOGvqc6"
VISION_ENDPOINT = "https://recobot-vision.cognitiveservices.azure.com/"
CLU_KEY = "7DaZAKFJb2DhSL3nMcCVGu8fSA3uTWgxGgAdMIegmbuD2F1bli3ZJQQJ99BDACYeBjFXJ3w3AAAaACOG1KlZ"
CLU_ENDPOINT = "https://recobot-language-clu.cognitiveservices.azure.com/"

# Simple HTML page for interaction
html_page = '''
<!DOCTYPE html>
<html>
<head><title>Intelligent Recommendation Bot</title></head>
<body>
    <h2>Talk to the Bot</h2>
    <form method="POST" enctype="multipart/form-data">
        <label>Text Input:</label><br>
        <input type="text" name="user_text"><br><br>
        
        <label>Voice Input (upload audio file - .wav or .mp3):</label><br>
        <input type="file" name="user_voice"><br><br>
        
        <label>Image Input (upload image):</label><br>
        <input type="file" name="user_image"><br><br>

        <input type="submit" value="Send">
    </form>

    {% if result %}
    <h3>Bot Response:</h3>
    <p>{{ result }}</p>
    {% endif %}
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    result = ""

    if request.method == 'POST':
        user_text = request.form.get('user_text')
        user_voice = request.files.get('user_voice')
        user_image = request.files.get('user_image')

        if user_text:
            # Simulate GPT response (for now dummy)
            result = f"You typed: {user_text}. (Bot recommends: Stay positive and hydrated!)"

        if user_voice:
            # Process voice file with Azure Speech-to-Text
            headers = {
                'Ocp-Apim-Subscription-Key': SPEECH_KEY,
                'Content-Type': 'audio/wav'  # or 'audio/mp3' based on file type
            }
            params = {
                "language": "en-US"
            }
            recognize_url = SPEECH_ENDPOINT + "speech/recognition/conversation/cognitiveservices/v1"
            audio_data = user_voice.read()
            response = requests.post(recognize_url, headers=headers, params=params, data=audio_data)
            speech_result = response.json()
            recognized_text = speech_result.get('DisplayText', '[Could not recognize speech]')
            result += f" | Voice said: {recognized_text}"

        if user_image:
            headers = {
                'Ocp-Apim-Subscription-Key': VISION_KEY,
                'Content-Type': 'application/octet-stream'
            }
            analyze_url = VISION_ENDPOINT + "/vision/v3.2/analyze?visualFeatures=Tags"
            img_data = user_image.read()
            response = requests.post(analyze_url, headers=headers, data=img_data)
            analysis = response.json()
            tags = [tag['name'] for tag in analysis.get('tags', [])]
            result += f" | Image tags: {tags}"

    return render_template_string(html_page, result=result)

if __name__ == '__main__':
    app.run(debug=True)