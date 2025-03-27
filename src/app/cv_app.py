from flask import Flask, request, jsonify
import json
from src.scraper.my_resume import MyResume

class CVApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.__registerRoutes()

    def __registerRoutes(self):
        @self.app.route('/api/generate-cv', methods=['POST'])
        def generateCV():
            data = request.get_json()

            username = data['username']
            password = data['password']
            profile_url = data['profileUrl']

            resume = MyResume(username, password, profile_url)
            try:
                resume.login()
                return json.dumps(resume.getResume(), indent=4)
            except Exception as e:
                return jsonify({"error": str(e)}), 500

    def run(self):
        self.app.run(debug=True)