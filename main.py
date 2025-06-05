from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape

import datetime
import pandas
import collections
from dotenv import load_dotenv
import os


def get_years_since_foundation(date_of_foundation: datetime) -> int:
    days_since_foundation = (datetime.date.today() - date_of_foundation).days
    days_in_year = 365
    years_since_foundation = int(days_since_foundation/days_in_year)
    return years_since_foundation


def get_date_pronounciation(year: int) -> str:
    years_pronounce = {
        '1': 'год',
        '2': 'года',
        '3': 'года',
        '4': 'года',
        '5': 'лет',
        '6': 'лет',
        '7': 'лет',
        '8': 'лет',
        '9': 'лет',
        '0': 'лет',
        '11': 'лет',
        '12': 'лет',
        '13': 'лет',
        '14': 'лет',
    }

    last_numbers = str(year)[-2:]
    last_number = str(year)[-1:]

    if last_numbers in years_pronounce:
        return years_pronounce[last_numbers]
    else:
        return years_pronounce[last_number]


def get_wines_from_excel(excel_filename: str) -> dict:
    wines_from_excel = pandas.read_excel(
                excel_filename,
                na_values=' ',
                keep_default_na=False
            ).to_dict(orient='records')

    wines = collections.defaultdict(list)
    [wines[wine['Категория']].append(wine) for wine in wines_from_excel]
    sorted_wines = dict(sorted(wines.items()))
    return sorted_wines


def main():
    load_dotenv()
    date_of_foundation = datetime.date(year=1920, month=1, day=1)
    
    excel_filename = os.environ["EXCEL_FILENAME"]
    years_since_foundation = get_years_since_foundation(date_of_foundation)

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    rendered_page = template.render(
        years_since_foundation=years_since_foundation,
        date_pronounciation=get_date_pronounciation(years_since_foundation),
        wines=get_wines_from_excel(excel_filename),
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()