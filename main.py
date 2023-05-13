import vacancy_api


def get_platform() -> int:
    """
    Asks user to choose platform for vacancy search
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
    Maximum value is 10.
    """
    top_n = int(input("Please enter number to display "
                      "by top salary (maximum 10): "))
    # Validate user choice
    while top_n not in range(1, 11):
        top_n = int(input("Please enter correct number from 1 to 10: "))

    return top_n


def get_vacancies(platform: int, search_text: str) -> list:
    """
    Returns a list of vacancies base
    """
    headhunter_api = vacancy_api.HeadHunterAPI()
    superjob_api = vacancy_api.SuperJobAPI()

    match platform:
        case 1:
            return headhunter_api.get_vacancies(search_text)
        case 2:
            return superjob_api.get_vacancies(search_text)
        case 3:
            return headhunter_api.get_vacancies(search_text) + \
                   superjob_api.get_vacancies(search_text)


# Start Program
def main():
    """
    Main algorithm
    """
    # Ask user to choose platform
    platform = get_platform()
    # Ask user to enter search text
    search_text = input("Please enter search query: ")
    # Ask user to enter number of top vacancies (by salary) to display
    top_n = get_top_n()
    # Get vacancies using chosen platforms and search query
    vacancies = get_vacancies(platform, search_text)

    for vac in vacancies:
        print(vac)
    print(len(vacancies))


if __name__ == "__main__":
    main()
