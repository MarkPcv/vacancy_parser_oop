from abc import ABC, abstractmethod
import requests
import json
import os


class MasterAPI(ABC):

    @abstractmethod
    def get_vacancies(self, search_text):
        pass


class HeadHunterAPI(MasterAPI):
    """Class for API using HeadHunter Service"""

    def __init__(self):
        """
        Initialise the class
        """
        self.__base_url = "https://api.hh.ru/vacancies"

    def get_vacancies(self, search_text):
        """
        Returns a list of 20 vacancies based on the search text
        """
        vacancies = self.get_page(search_text)['items']
        return vacancies

    def get_page(self, search_text):
        """
        Returns JSON object of the vacancies using keyword
        """
        params = {
            'area': '113',          # location - Russia
            'page': 0,              # page number
            'text': search_text,
            'per_page': 20          # 20 vacancies per page
        }
        response = requests.get(self.__base_url, params)
        return response.json()


class SuperJobAPI(MasterAPI):
    """Class for API using SuperJob Service"""

    # Define API key for SuperJob
    api_key = os.getenv('SUPERJOB_API_KEY')

    def __init__(self):
        """
        Initialise the class
        """
        self.__base_url = 'https://api.superjob.ru/2.0/vacancies/'

    def get_vacancies(self ,search_text):
        """
        Returns a list of 20 vacancies based on the search text
        """
        vacancies = self.get_page(search_text)['objects']
        return vacancies

    def get_page(self, search_text):
        """
        Returns JSON object of the vacancies using keyword
        """
        # Parameters for GET request
        params = {
            'keyword': search_text,
            'c': [1],                   # location - Russia
            'page': 0,                  # page number
            'count': 20,                # 20 vacancies per page
        }
        # Header with API key for GET request
        headers = {
            'X-Api-App-Id': sj.api_key,
        }
        response = requests.get(self.__base_url, params, headers=headers)
        return response.json()


# HeadHunter Test

# hh = HeadHunterAPI()
# with open("sample.json", "w", encoding='utf8') as outfile:
#     json.dump(hh.get_vacancies('Python'), outfile, indent='\t', ensure_ascii=False)

# SuperJob Test

# sj = SuperJobAPI()
# with open("sample2.json", "w", encoding='utf8') as outfile:
#     json.dump(sj.get_vacancies('Python'), outfile, indent='\t', ensure_ascii=False)
