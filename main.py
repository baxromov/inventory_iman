import xml.etree.ElementTree as ET


def get_data():
    values = []
    tree = ET.parse('2900.xml')
    root = tree.getroot()
    items = list(root.iter('{urn:schemas-microsoft-com:office:spreadsheet}Row'))
    for row in items:
        temp = []
        for cell in row.iter('{urn:schemas-microsoft-com:office:spreadsheet}Cell'):
            data_element = cell.find('.//{urn:schemas-microsoft-com:office:spreadsheet}Data')
            if data_element is not None and data_element.attrib['{urn:schemas-microsoft-com:office:spreadsheet}Type'] == "Number" and cell.attrib['{urn:schemas-microsoft-com:office:spreadsheet}StyleID'] == "s96":
                temp.append(data_element.text)

            if data_element is not None and cell.attrib.get('{urn:schemas-microsoft-com:office:spreadsheet}MergeAcross') == str(2) and data_element.attrib['{urn:schemas-microsoft-com:office:spreadsheet}Type'] == "String":
                temp.append(data_element.text)

            if data_element is not None and cell.attrib.get('{urn:schemas-microsoft-com:office:spreadsheet}StyleID') == 's100' and data_element.attrib['{urn:schemas-microsoft-com:office:spreadsheet}Type'] == "Number":
                temp.append(data_element.text)

        values.append(temp)

    t = []
    fi = list(filter(lambda x: len(x) >= 2, values))
    for i in range(0, len(fi), 3):
        g = fi[i:i+3]
        t.append(
            {
                "title": str(g[0][0]),
                "price": float(g[0][1]),
                "quantity": float(g[1][1]),
            }
        )

    return t

print(get_data())




"""

def get_data(file):
    workbook = openpyxl.load_workbook(file)
    worksheet = workbook['Отчет']

    data = []

    for row in worksheet.iter_rows(min_row=8, values_only=True):
        data.append(row)

    result = []
    for i in range(0, len(data), 6):
        if i + 1 < len(data):
            info = [value for item in data[i:i + 2] for value in item if value is not None]
            title = list(filter(lambda x: isinstance(x, str), info))[0]
            ZERO_PRICE = list(map(lambda x: float(x), list(filter(lambda x: not isinstance(x, str), info))))[0]
            QTY = list(map(lambda x: int(x), list(filter(lambda x: not isinstance(x, str),
                                                         [value for item in data[i + 1:i + 2] for value in item if
                                                          value is not None]))))[0]

            price = ZERO_PRICE / QTY
            result.append({
                "title": title,
                "price": price,
                "quantity": QTY
            })
    return result

"""