from abc import ABC, abstractmethod
import requests
import os
import json
from vacancy import Vacancy

# Exchange rate of US dollars to Rubles
# Some salaries are expressed in US dollars
USD_RATE = 77.36  # as of 12 May 2023


class MasterAPI(ABC):

    @abstractmethod
    def get_vacancies(self, search_text):
        pass


class HeadHunterAPI(MasterAPI):
    """Class for API using HeadHunter Service"""

    @staticmethod
    def get_salary(vacancy: dict) -> int:
        # Check if vacancy has salary
        if not vacancy['salary']:
            return None
        # Check if salary is shown in USD
        if vacancy['salary']['currency'] == 'USD':
            conversion_rate = USD_RATE
        else:
            conversion_rate = 1
        # Check if vacancy has minimum salary otherwise return maximum
        if vacancy['salary']['from'] is None:
            return vacancy['salary']['to'] * conversion_rate
        return vacancy['salary']['from'] * conversion_rate

    def __init__(self):
        """
        Initialise the class
        """
        self.__base_url = "https://api.hh.ru/vacancies"

    def get_vacancies(self, search_text) -> list[Vacancy]:
        """
        Returns a list of vacancies (maximum 20) based on the search text
        """
        vacancies = []
        # Start vacancy search starting from first page till 20th
        for page in range(0, 21):
            # Get the list of vacancy dictionaries
            api_vacancies = self.get_page(search_text, page)['items']

            # Convert each dictionary to a Vacancy object
            for v in api_vacancies:
                name = v['name']
                url = v['alternate_url']
                salary = self.get_salary(v)
                employer = v['employer']['name']
                requirement = v['snippet']['requirement']
                # Add vacancy to the list
                try:
                    vacancies.append(Vacancy(name, url, salary,
                                             employer, requirement))
                except TypeError:
                    continue
                # Check if list is full
                if len(vacancies) == 20:
                    break
            # Check if list is full
            if len(vacancies) == 20:
                break

        return vacancies

    def get_page(self, search_text: str, page: int) -> dict:
        """
        Returns JSON object of the vacancies using keyword
        """
        params = {
            'area': '113',  # location - Russia
            'page': page,  # page number
            'text': search_text,
            'per_page': 20  # 20 vacancies per page
        }
        response = requests.get(self.__base_url, params)
        return json.loads(response.text)


class SuperJobAPI(MasterAPI):
    """Class for API using SuperJob Service"""

    @staticmethod
    def get_salary(vacancy: dict) -> int | None:
        # Check if vacancy has minimum salary
        if vacancy['payment_from'] == 0:
            # Checks if vacancy has maximum salary otherwise return None
            if vacancy['payment_to'] == 0:
                return None
            return vacancy['payment_to']
        return vacancy['payment_from']

    # Define API key for SuperJob
    api_key = os.getenv('SUPERJOB_API_KEY')

    def __init__(self):
        """
        Initialise the class
        """
        self.__base_url = 'https://api.superjob.ru/2.0/vacancies/'

    def get_vacancies(self, search_text):
        """
        Returns a list of vacancies (maximum 20) based on the search text
        """
        vacancies = []
        # Start vacancy search starting from first page till 20th
        for page in range(0, 21):
            # Get the list of vacancy dictionaries
            api_vacancies = self.get_page(search_text, page)['objects']

            # Convert each dictionary to a Vacancy object
            for v in api_vacancies:
                name = v['profession']
                url = v['link']
                salary = self.get_salary(v)
                employer = v['firm_name']
                requirement = v['candidat']
                # Add vacancy to the list
                try:
                    vacancies.append(Vacancy(name, url, salary,
                                             employer, requirement))
                except TypeError:
                    continue
                # Check if list is full
                if len(vacancies) == 20:
                    break
            # Check if list is full
            if len(vacancies) == 20:
                break

        return vacancies

    def get_page(self, search_text: str, page: int) -> dict:
        """
        Returns JSON object of the vacancies using keyword
        """
        # Parameters for GET request
        params = {
            'keyword': search_text,
            'c': [1],  # location - Russia
            'page': 0,  # page number
            'count': 20,  # 20 vacancies per page
        }
        # Header with API key for GET request
        headers = {
            'X-Api-App-Id': self.api_key,
        }
        response = requests.get(self.__base_url, params, headers=headers)
        return json.loads(response.text)
