from my_resume import MyResume
import json

if __name__ == '__main__':
    with open('config.json', 'r') as file:
        config = json.load(file)

    username = config['credentials']['username']
    password = config['credentials']['password']
    profile_url = config["profileUrl"]

    resume = MyResume(username, password, profile_url)
    resume.login()

    print(json.dumps(resume.getResume(), indent=4))