from bs4 import BeautifulSoup
import requests
import csv

URL = "https://stackoverflow.com/questions"
PAGE_LIMIT = 4

def build_url(base_url=URL, tab="newest", page=1):
    return f"{base_url}?tab={tab}&page={page}"

def scrape_page(page=1):
    """
    Function to scrape a single page in stack overflow
    """
    response = requests.get(build_url(page=page))
    page_questions = []
    soup = BeautifulSoup(response.text, "html.parser")
    question_summary = soup.find_all("div", class_="question-summary")

    for summary in question_summary:
        question = summary.find(class_="question-hyperlink").text
        vote_count = summary.find(class_="vote-count-post").find("strong").text
        answers_count = summary.find(class_="status").find("strong").text
        view_count = summary.find(class_="views").text.split()[0]
        page_questions.append({
            "question":  question,
            "answers": answers_count,
            "views": view_count,
            "votes": vote_count
        })
    
    return page_questions


def scrape():
    """
    Function to scrape to PAGE_LIMIT
    """
    questions = []
    for i in range(1, PAGE_LIMIT + 1):
        page_questions = scrape_page(i)
        questions.extend(page_questions)
    return questions

def export_data():
    data = scrape()
    with open("questions.csv", "w") as data_file:
        fieldnames = ["answers", "question", "views", "votes"]
        data_writer = csv.DictWriter(data_file, fieldnames=fieldnames)
        data_writer.writeheader()
        for d in data:
            data_writer.writerow(d)
        print("Done")
        


if __name__ == "__main__":
    # from pprint import pprint
    # pprint(scrape())
    export_data()
