import openpyxl
import json


# Load the Excel file

def get_data(file):
    workbook = openpyxl.load_workbook(file)

    # Select the worksheet by name or index
    worksheet = workbook['Отчет']  # Replace 'Sheet1' with the actual sheet name

    # Iterate through rows starting from the second row (assuming header is in the first row)
    data = []

    for row in worksheet.iter_rows(min_row=8, values_only=True):
        data.append(row)

    result = []
    for i in range(0, len(data), 6):
        if i + 1 < len(data):
            info = [value for item in data[i:i + 2] for value in item if value is not None]
            result.append({
                "title": info[0],
                "price": info[1] / info[4]
            })
    return result


def write_to_file():
    with open('data.json', 'w', encoding='utf-8') as json_file:
        json.dump(get_data('2910.xlsx'), json_file,  ensure_ascii=False)