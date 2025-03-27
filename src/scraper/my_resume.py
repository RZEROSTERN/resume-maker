from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

class MyResume:
    def __init__(self, username: str, password: str, profile_url: str):
        self.username = username
        self.password = password
        self.profile_url = profile_url
        self.resume_result = {}
        self.driver = self.configDriver()

    def configDriver(self):
        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument("--headless")

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        return driver
    
    def login(self):
        self.driver.get("https://www.linkedin.com/login")

        username_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "username"))
        )

        username_input.send_keys(self.username)

        password_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "password"))
        )
        password_input = self.driver.find_element(By.ID, "password")
        password_input.send_keys(self.password)
        password_input.send_keys(Keys.RETURN)

        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "global-nav-search"))
            )
            print("Inicio de sesión exitoso 💖")
        except:
            print("Error al iniciar sesión 💔")

    def getResume(self):
        self.__getProfileData()
        self.__getExperiences()
        self.__getEducation()
        self.__getCertifications()
        self.__getSkills()

        self.__shutdownDriver()

        return self.resume_result

    def __getProfileData(self):
        soup = self.__initializeSoup(self.profile_url)

        name = self.driver.find_element(By.CSS_SELECTOR, 'h1.inline.t-24.v-align-middle.break-words').text
        title = self.driver.find_element(By.CSS_SELECTOR, 'div.text-body-medium').text
        location = soup.find('span', {'class':'text-body-small inline t-black--light break-words'}).get_text().strip()
        
        sections = soup.find_all('section', {'class': 'artdeco-card pv-profile-card break-words mt2'})

        for sec in sections:
            if sec.find('div', {'id': 'about'}):
                about = sec.find('div', {'class': 'display-flex ph5 pv3'})
                about = about.find('span', {'class': 'visually-hidden'}).get_text().strip()

        self.resume_result['name'] = name
        self.resume_result['title'] = title
        self.resume_result['location'] = location
        self.resume_result['about'] = about

    def __getExperiences(self):
        soup = self.__initializeSoup(self.profile_url + "/details/experience")

        section = soup.find('section', {'class': 'artdeco-card pb3'})

        experiences = section.find_all('div', {'class': 'display-flex flex-column align-self-center flex-grow-1'})

        for exp in experiences:
            experience = {}

            name = exp.find('div', {'class': 'display-flex flex-wrap align-items-center full-height'})
            name = name.find('span', {'class': 'visually-hidden'})
            name = name.get_text().strip()

            company = exp.find('span', {'class': 't-14 t-normal'})
            company = company.find('span', {'class': 'visually-hidden'})
            company = company.get_text().strip()

            period = exp.find('span', {'class': 't-14 t-normal t-black--light'})
            period = period.find('span', {'class': 'visually-hidden'})
            period = period.get_text().strip()

            experience['name'] = name
            experience['company'] = company
            experience['period'] = period

            if 'experiences' not in self.resume_result:
                self.resume_result['experiences'] = []

            self.resume_result['experiences'].append(experience)

    def __getExperiences(self):
        soup = self.__initializeSoup(self.profile_url + "/details/experience")

        section = soup.find('section', {'class': 'artdeco-card pb3'})

        experiences = section.find_all('div', {'class': 'display-flex flex-column align-self-center flex-grow-1'})

        for exp in experiences:
            experience = {}

            name = exp.find('div', {'class': 'display-flex flex-wrap align-items-center full-height'})
            name = name.find('span', {'class': 'visually-hidden'})
            name = name.get_text().strip()

            company = exp.find('span', {'class': 't-14 t-normal'})
            company = company.find('span', {'class': 'visually-hidden'})
            company = company.get_text().strip()

            period = exp.find('span', {'class': 't-14 t-normal t-black--light'})
            period = period.find('span', {'class': 'visually-hidden'})
            period = period.get_text().strip()

            experience['name'] = name
            experience['company'] = company
            experience['period'] = period

            if 'experiences' not in self.resume_result:
                self.resume_result['experiences'] = []

            self.resume_result['experiences'].append(experience)

    def __getEducation(self):
        soup = self.__initializeSoup(self.profile_url + "/details/education")

        section = soup.find('section', {'class': 'artdeco-card pb3'})

        education = section.find_all('div', {'class': 'display-flex flex-column align-self-center flex-grow-1'})

        for edu in education:
            experience = {}

            institution = edu.find('div', {'class': 'display-flex align-items-center mr1 hoverable-link-text t-bold'})
            institution = institution.find('span', {'class': 'visually-hidden'})
            institution = institution.get_text().strip()

            program = edu.find('span', {'class': 't-14 t-normal'})
            program = program.find('span', {'class': 'visually-hidden'})
            program = program.get_text().strip()

            period = edu.find('span', {'class': 't-14 t-normal t-black--light'})
            period = period.find('span', {'class': 'visually-hidden'})
            period = period.get_text().strip()

            experience['institution'] = institution
            experience['program'] = program
            experience['period'] = period

            if 'education' not in self.resume_result:
                self.resume_result['education'] = []

            self.resume_result['education'].append(experience)

    def __getCertifications(self):
        soup = self.__initializeSoup(self.profile_url + "/details/certifications")

        section = soup.find('section', {'class': 'artdeco-card pb3'})

        certifications = section.find_all('div', {'class': 'display-flex flex-column align-self-center flex-grow-1'})

        for cert in certifications:
            certification = {}

            name = cert.find('div', {'class': 'display-flex flex-wrap align-items-center full-height'})
            name = name.find('span', {'class': 'visually-hidden'})
            name = name.get_text().strip()

            company = cert.find('span', {'class': 't-14 t-normal'})
            company = company.find('span', {'class': 'visually-hidden'})
            company = company.get_text().strip()

            period = cert.find('span', {'class': 't-14 t-normal t-black--light'})
            period = period.find('span', {'class': 'visually-hidden'}) if period is not None else ""
            period = period.get_text().strip() if period != "" else ""

            certification['name'] = name
            certification['company'] = company
            certification['period'] = period

            if 'certifications' not in self.resume_result:
                self.resume_result['certifications'] = []

            self.resume_result['certifications'].append(certification)

    def __getSkills(self):
        soup = self.__initializeSoup(self.profile_url + "/details/skills")

        section = soup.find('section', {'class': 'artdeco-card pb3'})

        skills = section.find_all('div', {'class': 'display-flex flex-column align-self-center flex-grow-1'})

        for sk in skills:
            skill = {}
            
            name = sk.find('div', {'class': 'display-flex flex-wrap align-items-center full-height'})
            name = name.find('span', {'class': 'visually-hidden'})
            name = name.get_text().strip()

            skill['name'] = name

            if 'skills' not in self.resume_result:
                self.resume_result['skills'] = []

            self.resume_result['skills'].append(skill)

    def __initializeSoup(self, url):
        self.driver.get(url)
        time.sleep(3)

        pageSource = self.driver.page_source
        soup = BeautifulSoup(pageSource, "html.parser")

        return soup

    def __shutdownDriver(self):
        self.driver.quit()
