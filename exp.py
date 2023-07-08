import sys
import xml.etree.ElementTree as ET

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QFileDialog, QLabel, QVBoxLayout, QWidget,
    QLineEdit, QTableWidgetItem, QTableWidget
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Поиск товаров Iman")
        self.upload_button = QPushButton("Загрузить файл Excel", self)
        self.upload_button.clicked.connect(self.upload_file)

        self.search_button = QPushButton("Поиск", self)
        self.search_button.clicked.connect(self.search_data)

        self.price_label = QLabel("Цена:", self)
        self.price_input = QLineEdit(self)
        self.table_widget = QTableWidget(self)
        self.result_label = QLabel("Результат поиска:", self)

        layout = QVBoxLayout()
        layout.addWidget(self.upload_button, alignment=Qt.AlignCenter)
        layout.addWidget(self.price_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.price_input)
        layout.addWidget(self.search_button, alignment=Qt.AlignCenter)
        layout.addWidget(self.result_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.table_widget)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QLabel {
                font-size: 14px;
            }
            QPushButton {
                padding: 8px 16px;
                font-size: 14px;
                background-color: #4caf50;
                color: #fff;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QLineEdit {
                padding: 8px;
                font-size: 14px;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
            QTableWidget {
                background-color: #fff;
                border: none;
            }
            QTableWidget::item {
                padding: 8px;
            }
        """)

    def upload_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Выберите файл Excel", "", "Файлы Excel (*.xml)")

        if file_path:
            self.file_path = file_path
            self.result_label.setText("Файл успешно загружен.")

    def search_data(self):
        price = self.price_input.text()

        if not hasattr(self, 'file_path'):
            self.result_label.setText("Пожалуйста, сначала загрузите файл Excel.")
            return

        data = get_data(self.file_path)
        search_result = []
        for entry in data:
            low_price = float(price) * (1 - 0.125)
            if float(price) >= entry['price'] / entry['quantity'] >= low_price:
                search_result.append(entry)

        if search_result:
            self.display_result(search_result)
        else:
            self.result_label.setText("Совпадающих записей не найдено.")

    def display_result(self, search_result):
        self.table_widget.clear()
        self.table_widget.setColumnCount(3)
        self.table_widget.setRowCount(len(search_result))
        self.table_widget.setHorizontalHeaderLabels(["Наименование", "Цена", "Количество"])

        for row, entry in enumerate(search_result):
            title_item = QTableWidgetItem(entry["title"])
            pp = "{:,.0f}".format(float(entry["price"]) / float(entry['quantity']))
            price_item = QTableWidgetItem(pp)
            quantity_item = QTableWidgetItem(str(entry["quantity"]))
            self.table_widget.setItem(row, 0, title_item)
            self.table_widget.setItem(row, 1, price_item)
            self.table_widget.setItem(row, 2, quantity_item)

        self.table_widget.resizeColumnsToContents()


def get_data(file):
    values = []
    tree = ET.parse(file)
    root = tree.getroot()
    items = list(root.iter('{urn:schemas-microsoft-com:office:spreadsheet}Row'))
    for row in items:
        temp = []
        for cell in row.iter('{urn:schemas-microsoft-com:office:spreadsheet}Cell'):
            data_element = cell.find('.//{urn:schemas-microsoft-com:office:spreadsheet}Data')
            if data_element is not None and data_element.attrib[
                '{urn:schemas-microsoft-com:office:spreadsheet}Type'] == "Number" and cell.attrib[
                '{urn:schemas-microsoft-com:office:spreadsheet}StyleID'] == "s96":
                temp.append(data_element.text)

            if data_element is not None and cell.attrib.get(
                    '{urn:schemas-microsoft-com:office:spreadsheet}MergeAcross') == str(2) and data_element.attrib[
                '{urn:schemas-microsoft-com:office:spreadsheet}Type'] == "String":
                temp.append(data_element.text)

            if data_element is not None and cell.attrib.get(
                    '{urn:schemas-microsoft-com:office:spreadsheet}StyleID') == 's100' and data_element.attrib[
                '{urn:schemas-microsoft-com:office:spreadsheet}Type'] == "Number":
                temp.append(data_element.text)

        values.append(temp)

    t = []
    fi = list(filter(lambda x: len(x) >= 2, values))
    for i in range(0, len(fi), 3):
        g = fi[i:i + 3]
        t.append(
            {
                "title": str(g[0][0]),
                "price": float(g[0][1]),
                "quantity": float(g[1][1]),
            }
        )

    return t


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
