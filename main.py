from services.utils import *


def main():
    """
    Main algorithm
    """
    # Ask user to choose platform
    platform = get_platform_choice()
    # Ask user to enter search text
    search_text = input("Please enter search query: ")
    # Ask user to enter number of top vacancies (by salary) to display
    top_n = get_top_n()
    # Ask user to enter filename to save vacancies into
    filename = get_filename()
    # Display top N vacancies sorted by salary
    show_top_n(platform, search_text, top_n, filename)
    # Display saved vacancies (and delete any)
    show_saved_vacancies(filename)


if __name__ == "__main__":
    main()
