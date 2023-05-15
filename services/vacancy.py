class Vacancy:
    """Class to represent vacancy information"""
    def __init__(self, name: str, url: str, salary: int,
                 employer: str, requirement: str) -> None:
        """
        Instance initialisation

        :name: Vacancy name
        :url: URL link to vacancy
        :salary: Minimum salary
        :description: Description of the vacancy/company
        :requirement: Vacancy requirements
        """
        # Validate data for attributes
        if type(name) is str:
            self.name = name
        else:
            raise TypeError('Vacancy name must be string')
        if type(url) is str:
            self.url = url
        else:
            raise TypeError('Vacancy URL must be string')
        if type(salary) is int:
            self.salary = salary
        else:
            raise TypeError('Vacancy salary must be integer')
        if type(employer) is str:
            self.employer = employer
        else:
            raise TypeError('Vacancy description must be integer')
        if type(requirement) is str:
            self.requirement = requirement
        else:
            raise TypeError('Vacancy requirement must be integer')

    def __repr__(self) -> str:
        """Returns a developer representation of Vacancy class"""
        return (
            f"Vacancy({self.name}, {self.url}, {self.salary}, "
            f"{self.employer}, {self.requirement})"
        )

    def __str__(self) -> str:
        """"Returns a user representation of Vacancy class"""
        return (
            f"Name:         {self.name}\n"
            f"URL:          {self.url}\n"
            f"Salary:       {self.salary}\n"
            f"Company:      {self.employer}\n"
            f"Requirement:\n{self.requirement}\n"
        )

    def __eq__(self, other) -> bool:
        """
        Checks if salaries between two vacancies are equal
        """
        if type(other) == Vacancy:
            return self.salary == other.salary
        else:
            raise ValueError("Must be <Vacancy> object")

    def __lt__(self, other) -> bool:
        """
        Checks if salary of this vacancy is less than other
        """
        if type(other) == Vacancy:
            return self.salary < other.salary
        else:
            raise ValueError("Must be <Vacancy> object")

    def __le__(self, other) -> bool:
        """
        Checks if salary of this vacancy is less than other or equal
        """
        if type(other) == Vacancy:
            return self.salary <= other.salary
        else:
            raise ValueError("Must be <Vacancy> object")

    def __gt__(self, other) -> bool:
        """
        Checks if salary of this vacancy is more than other
        """
        if type(other) == Vacancy:
            return self.salary > other.salary
        else:
            raise ValueError("Must be <Vacancy> object")

    def __ge__(self, other) -> bool:
        """
        Checks if salary of this vacancy is more than other or equal
        """
        if type(other) == Vacancy:
            return self.salary >= other.salary
        else:
            raise ValueError("Must be <Vacancy> object")
