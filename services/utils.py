from services import saver
from services import vacancy_api


def get_platform_choice() -> int:
    """
    Asks user to choose API platform for vacancy search
    """
    platform = int(input("Hi, please choose platforms for vacancy search:\n"
                         "1 - HeadHunter\n"
                         "2 - SuperJob\n"
                         "3 - both\n"))
    # Validate user choice
    while platform not in range(1, 4):
        platform = int(input("Please enter correct number from 1 to 3: "))

    return platform


def get_top_n() -> int:
    """
    Asks user to enter number of top vacancies (by salary) to display.
    Maximum value is 25.
    """
    top_n = int(input("Please enter number to display "
                      "by top salary (maximum 25): "))
    # Validate user choice
    while top_n not in range(1, 26):
        top_n = int(input("Please enter correct number from 1 to 10: "))

    return top_n


def get_filename() -> str:
    """
    # Asks user to enter filename to save vacancies into
    """
    filename = input("Please enter name for JSON file vacancy saving: ")
    # If file exists clear the data
    saver.JSONSaver(filename).clear_file()
    return filename


def get_vacancies(platform: int, search_text: str) -> list:
    """
    Returns a list of vacancies base
    """
    headhunter_api = vacancy_api.HeadHunterAPI()
    superjob_api = vacancy_api.SuperJobAPI()

    match platform:
        case 1:
            return headhunter_api.search_vacancies(search_text)
        case 2:
            return superjob_api.search_vacancies(search_text)
        case 3:
            return headhunter_api.search_vacancies(search_text) + \
                superjob_api.search_vacancies(search_text)


def save_vacancy(vacancy: vacancy_api.Vacancy, filename: str):
    """
    Saves the vacancy by user choice
    """
    choice = int(input("Do you want to save vacancy?\n"
                       "0 - No\n"
                       "1 - Yes\n"))
    # Validate user choice
    while choice not in range(0, 2):
        choice = int(input("Please enter correct number - 0 or 1: "))

    if choice:
        json_saver = saver.JSONSaver(filename)
        json_saver.add_vacancy(vacancy)


def show_top_n(platform: int, search_text: str, top_n: int, filename: str):
    """
    Displays the top N vacancies sorted by salary in descending order
    :param platform: API platform choice
    :param search_text: search query
    :param top_n: maximum number of vacancies to search
    :param filename: name of the file that stores the chosen vacancies
    """
    # Get vacancies using chosen platforms and search query
    vacancies = get_vacancies(platform, search_text)
    # Sort vacancies
    vacancies.sort(reverse=True)
    # Display top N vacancies by salary
    for i in range(top_n):
        # Check if the available number of vacancies is less than top N
        try:
            print(vacancies[i])
            # Ask user to save the vacancy
            save_vacancy(vacancies[i], filename)
        except IndexError:
            break


def delete_vacancy(vacancy: vacancy_api.Vacancy, filename: str):
    """
    Deletes the vacancy by user choice
    """
    choice = int(input("Do you want to delete this vacancy?\n"
                       "0 - No\n"
                       "1 - Yes\n"))
    # Validate user choice
    while choice not in range(0, 2):
        choice = int(input("Please enter correct number - 0 or 1: "))

    if choice:
        json_saver = saver.JSONSaver(filename)
        json_saver.delete_vacancy(vacancy)


def show_saved_vacancies(filename: str):
    """
    Shows saved vacancies in JSON file which are in range between
    minimum and maximum salaries determined by user.
    User also can delete any chosen vacancy from the file.
    """
    lower = int(input("Time to revise saved vacancies.\n"
                      "Please enter a minimum salary: "))
    upper = int(input("Please enter maximum salary: "))
    json_saver = saver.JSONSaver(filename)
    saved_vacancies = json_saver.get_vacancies_by_salary(lower, upper)
    for vacancy in saved_vacancies:
        print(vacancy)
        # Ask user to save the vacancy
        delete_vacancy(vacancy, filename)