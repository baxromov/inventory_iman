import sys
import locale
import re

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QLineEdit, QScrollArea, QVBoxLayout, QLayout, \
    QDesktopWidget


class GridExample(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        scroll_area = QScrollArea()  # Create a QScrollArea
        scroll_widget = QWidget()  # Create a QWidget to hold the grid layout
        scroll_area.setWidget(scroll_widget)  # Set the scroll area's widget

        grid = QGridLayout(scroll_widget)  # Use the scroll widget for the grid layout
        scroll_widget.setLayout(grid)

        self.setLayout(grid)

        self.price_input = QLineEdit()
        self.price_input.setPlaceholderText("Сумма заявки")
        self.price_input.textChanged.connect(self.calculate_commission)

        self.price_input.setStyleSheet(
            """
            QLineEdit {
                border: 1px solid #4B5563;
                font-size: 18px;
                font-weight: bold;
                padding: 8px;
                background: #374151;
                border-radius: 30px;
                color: white;
            }
            """
        )
        grid.addWidget(self.price_input, 0, 0, 1, 3)

        months = [
            [1, 3, 6],
            [9, 12, 15],
            [18, 24]
        ]
        commission_rates = [0.07, 0.15, 0.25, 0.32, 0.38, 0.50, 0.56, 0.75]
        self.commission_labels = []

        for i, row in enumerate(months):
            for j, month in enumerate(row):
                rate = commission_rates[i * 3 + j]
                text = f"""
                        Месяцев: {month}\n
                        Сум/месяц: 0 сум\n 
                        Сумма заявки:0 сум\n
                        Комиссия {int(rate * 100)}%: 0 сум\n
                    """
                label = QLabel(text)
                label.setStyleSheet(
                    """
                     QLabel {
                         border: 1px solid #4B5563;
                         font-size: 18px;
                         font-weight: bold;
                         border-radius: 20px;
                         background: #1F2937;
                         color: white;
                         transition: background 1s;
                     }
                     QLabel:hover {
                         background: #374151;
                         transition: background 1s;
                     }
                     """
                )
                grid.addWidget(label, i + 1, j)
                self.commission_labels.append(label)

        scroll_area.setWidgetResizable(True)  # Allow the scroll area to resize its widget
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)  # Show vertical scroll bar
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # Hide horizontal scroll bar

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll_area)  # Add the scroll area to the main layout

        screen_geometry = QDesktopWidget().screenGeometry()
        self.resize(screen_geometry.width(), self.height())
        self.setWindowTitle('Калькулятор')
        self.setStyleSheet("background-color: #111827;")
        self.setWindowIcon(QIcon('rasrochka.ico'))
        self.show()

    def calculate_commission(self):
        locale.setlocale(locale.LC_ALL, '')
        months = [
            [1, 3, 6],
            [9, 12, 15],
            [18, 24]
        ]
        price = re.sub(r'[^\d]', '', self.price_input.text())
        if price:
            try:
                price = float(price) / 100
                commission_rates = [0.07, 0.15, 0.25, 0.32, 0.38, 0.50, 0.56, 0.75]

                for i, row in enumerate(months):
                    for j, month in enumerate(row):
                        rate = commission_rates[i * 3 + j]
                        commission = price * rate
                        label = self.commission_labels[i * 3 + j]
                        formatted_price = locale.format_string('%.2f', price, grouping=True)
                        formatted_commission = locale.format_string('%.2f', commission + price, grouping=True)
                        text = f"""
                            Месяцев: {month}\n
                            Сум/месяц: {locale.format_string('%.2f', (commission + price) / month, grouping=True)}  сум\n 
                            Сумма заявки: {formatted_price}\n
                            Комиссия {int(rate*100)}%: {formatted_commission}\n
                        """
                        label.setText(text)
            except ValueError:
                pass

        formatted_input = locale.format_string('%.2f', float(price), grouping=True)
        self.price_input.setText(formatted_input)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # Set the application style to "Fusion" for a modern look
    ex = GridExample()
    sys.exit(app.exec_())
