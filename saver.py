from abc import ABC, abstractmethod
from vacancy import Vacancy
import json


class MasterSaver(ABC):

    @abstractmethod
    def add_vacancy(self, vacancy: Vacancy):
        pass

    @abstractmethod
    def get_vacancies_by_salary(self, lower_bound: int,
                                upper_bound: int | None):
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy: Vacancy):
        pass


class JSONSaver(MasterSaver):

    def __init__(self, filename: str = 'vacancies'):
        """Initialise a JSONSaver instance"""
        self.filename = filename + '.json'

    def add_vacancy(self, vacancy: Vacancy) -> None:
        """Saves a Vacancy to the JSON file"""
        vacancies = []  # temporary list to store vacancies
        try:
            # Read file
            with open(self.filename, 'r', encoding='utf-8') as f:
                vacancies = json.load(f)
        except json.JSONDecodeError:
            print('Saving first vacancy')
        # Write to file with added new vacancy
        with open(self.filename, 'w', encoding='utf-8') as f:
            vacancies.append(vacancy.__dict__)
            json.dump(vacancies, f, ensure_ascii=False, indent='\t')

    def get_vacancies_by_salary(self, lower_bound: int,
                                upper_bound: int) -> list:
        """Returns a list of vacancies by salary"""
        vacancies = []
        with open(self.filename, 'r', encoding='utf-8') as f:
            for dict_vacancy in json.load(f):
                # Create Vacancy class using unpacking operator
                vacancy = Vacancy(**dict_vacancy)
                # Validate salary of current vacancy
                if lower_bound <= vacancy.salary <= upper_bound:
                    vacancies.append(vacancy)
        return vacancies

    def delete_vacancy(self, vacancy: Vacancy) -> None:
        """Deletes specified vacancy in the database"""
        vacancies = []  # temporary list to store vacancies
        # Read file and store other vacancies
        with open(self.filename, 'r', encoding='utf-8') as f:
            for vacancy_dict in json.load(f):
                if vacancy_dict['url'] != vacancy.url:
                    vacancies.append(vacancy_dict)
        # Write to file
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(vacancies, f, ensure_ascii=False, indent='\t')

    def clear_file(self):
        """Clears the data in the file"""
        f = open(self.filename, 'w')
        f.close()
