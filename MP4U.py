import csv
import os
import re
import sys
import locale
from collections import Counter

import numpy as np
import pandas as pd

from PySide6 import QtCharts
from PySide6.QtCharts import QPieSlice, QChart, QChartView
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from main_functions import MainFunctions
from ui_main import Ui_main_window

# ADJUST QT FONT DPI FOR HEIGHT SCALE
# ///////////////////////////////////////////////////////////////
os.environ["QT_FONT_DPI"] = "75"

# compile command: python3 -m nuitka --enable-plugin=pyside6 --include-data-files="./icon_*=./" --macos-create-app-bundle --macos-app-icon=logo.icns --disable-console --standalone --output-dir="dist" --output-filename=MP4U MP4U.py

global_pie_chart_window = None


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Setup Main Window
        self.ui = Ui_main_window()
        self.ui.setupUi(self)

        # Set Title
        self.setWindowTitle("MP4U Analytics Viewer")
        self.setWindowIconText("MP4U Analytics Viewer")

        # Setup Widgets
        MainFunctions.setup_widgets(self)

        # Setup dicts
        self.data_dict = None
        self.compare_data_dict = None
        self.compare_data_dict_sum = None
        self.data_dict_finances = None
        self.compare_data_dict_finances = None
        self.compare_data_dict_finances_sum = None
        self.data_dict_finances_square = None
        self.data_dict_finances_square_compare = None
        self.data_dict_finances_square_compare_sum = None
        self.employee_data_dict = None
        self.employee_data_dict_compare = None
        self.employee_data_dict_compare_sum = None
        self.data = {}
        self.compare_data = {}
        self.date_range_file = "Titles"
        self.date_range_compare_file = "Compare Titles"
        self.selected_file_paths = None
        self.selected_file_compare_paths = None
        self.pie_charts_connected = []

        locale.setlocale(locale.LC_ALL, 'en_CA.UTF-8')

        # Show App
        self.show()

    @staticmethod
    def add_splitter(orientation, layout, widgets=None):
        splitter = QSplitter(orientation)
        if widgets is not None:
            for widget in widgets:
                splitter.addWidget(widget)

        splitter.setSizes([300, 300])
        splitter.setHandleWidth(15)

        layout.addWidget(splitter)

        return splitter

    def create_orders_sum_compare_data_dict(self):
        self.compare_data_dict_sum = self.compare_data_dict.copy()

        for key in self.compare_data_dict_sum:
            self.compare_data_dict_sum[key] = self.calculate_percent_difference(
                self.clean_and_convert_to_float(self.compare_data_dict[key]),
                self.clean_and_convert_to_float(self.data_dict[key]))

        return self.compare_data_dict_sum

    def create_orders_compare_data_dict(self, compare_data, prep_data):
        self.compare_data_dict = self.data_dict.copy()

        quantity_column = [int(row[15]) for row in compare_data[1:]]
        size_column = [str(row[14]) for row in compare_data[1:]]
        small_count = 0
        large_count = 0
        smoothie_count = 0
        salad_count = 0
        treat_count = 0
        breakfast_count = 0
        pb_count = 0
        custom_count = 0
        unique_numbers = set()
        number_of_rows = [int(row[2]) for row in compare_data[1:] if
                          (int(row[2]) not in unique_numbers) and unique_numbers.add(int(row[2])) is None]
        app_orders = len(number_of_rows)
        meal_per_order = sum(quantity_column) / app_orders

        to_sell_lg_numbers = [pd.to_numeric(num, errors='coerce') if pd.notna(num) else pd.NaT for row in prep_data if
                              'To Sell: LG' in row for num in row[2:]]
        to_sell_sm_numbers = [pd.to_numeric(num, errors='coerce') if pd.notna(num) else pd.NaT for row in prep_data if
                              'To Sell: SM' in row for num in row[2:]]

        # Filter out NaT values before summing
        filtered_numbers = filter(lambda x: not pd.isna(x), to_sell_lg_numbers + to_sell_sm_numbers)

        # Sum with a default value of np.nan
        meals_to_sell = next(filtered_numbers, np.nan) + sum(filtered_numbers)

        count = 1
        for size in size_column:
            current_main_type = str(compare_data[count][12])
            current_quantity = int(compare_data[count][15])

            if size.__contains__("Small"):
                small_count += current_quantity
            elif size.__contains__("Large"):
                large_count += current_quantity
            elif size.__contains__("Regular"):
                if current_main_type.__contains__("TREAT"):
                    treat_count += current_quantity
                elif current_main_type.__contains__("SMOOTHIES"):
                    smoothie_count += current_quantity
                elif current_main_type.__contains__("Salad"):
                    salad_count += current_quantity
            elif size.__contains__("PB Bars"):
                pb_count += current_quantity
            elif size.__contains__("Breakfast"):
                breakfast_count += current_quantity
            else:
                custom_count += current_quantity
            count += 1

        self.compare_data_dict["Meals Pre Ordered"] = str(sum(quantity_column))
        self.compare_data_dict["Total Small"] = str(small_count)
        self.compare_data_dict["Total Treats"] = str(treat_count)
        self.compare_data_dict["Total Salads"] = str(salad_count)
        self.compare_data_dict["Total Smoothies"] = str(smoothie_count)
        self.compare_data_dict["Total Large"] = str(large_count)
        self.compare_data_dict["Total Breakfast"] = str(breakfast_count)
        self.compare_data_dict["Total PB Bars"] = str(pb_count)
        self.compare_data_dict["Total Custom"] = str(custom_count)
        self.compare_data_dict["Storefront Customers"] = str(app_orders)
        self.compare_data_dict["Meals per App Order"] = str(round(meal_per_order, 2))
        self.compare_data_dict["Meals to Sell"] = str(meals_to_sell)

        return self.compare_data_dict

    def create_orders_data_dict(self, data, prep_data):
        self.data_dict = {
            "Meals Pre Ordered": "",
            "Total Small": "",
            # regular
            "Total Smoothies": "",
            "Total Salads": "",
            "Total Treats": "",
            # end regular
            "Total Large": "",
            "Total Breakfast": "",
            "Total PB Bars": "",
            "Total Custom": "",
            "Storefront Customers": "",
            "Meals per App Order": "",
            "Meals to Sell": "",
        }

        quantity_column = [int(row[15]) for row in data[1:]]
        size_column = [str(row[14]) for row in data[1:]]
        small_count = 0
        large_count = 0
        smoothie_count = 0
        salad_count = 0
        treat_count = 0
        breakfast_count = 0
        pb_count = 0
        custom_count = 0
        unique_numbers = set()
        number_of_rows = [int(row[2]) for row in data[1:] if
                          (int(row[2]) not in unique_numbers) and unique_numbers.add(int(row[2])) is None]
        app_orders = len(number_of_rows)
        meal_per_order = sum(quantity_column) / app_orders
        to_sell_lg_numbers = [pd.to_numeric(num, errors='coerce') if pd.notna(num) else pd.NaT for row in prep_data if
                              'To Sell: LG' in row for num in row[2:]]
        to_sell_sm_numbers = [pd.to_numeric(num, errors='coerce') if pd.notna(num) else pd.NaT for row in prep_data if
                              'To Sell: SM' in row for num in row[2:]]

        # Filter out NaT values before summing
        filtered_numbers = filter(lambda x: not pd.isna(x), to_sell_lg_numbers + to_sell_sm_numbers)

        # Sum with a default value of np.nan
        meals_to_sell = next(filtered_numbers, np.nan) + sum(filtered_numbers)

        count = 1
        for size in size_column:
            current_main_type = str(data[count][12])
            current_quantity = int(data[count][15])

            if size.__contains__("Small"):
                small_count += current_quantity
            elif size.__contains__("Large"):
                large_count += current_quantity
            elif size.__contains__("Regular"):
                if current_main_type.__contains__("TREAT"):
                    treat_count += current_quantity
                elif current_main_type.__contains__("SMOOTHIES"):
                    smoothie_count += current_quantity
                elif current_main_type.__contains__("Salad"):
                    salad_count += current_quantity
            elif size.__contains__("PB Bars"):
                pb_count += current_quantity
            elif size.__contains__("Breakfast"):
                breakfast_count += current_quantity
            else:
                custom_count += current_quantity
            count += 1

        self.data_dict["Meals Pre Ordered"] = str(sum(quantity_column))
        self.data_dict["Total Small"] = str(small_count)
        self.data_dict["Total Treats"] = str(treat_count)
        self.data_dict["Total Salads"] = str(salad_count)
        self.data_dict["Total Smoothies"] = str(smoothie_count)
        self.data_dict["Total Large"] = str(large_count)
        self.data_dict["Total Breakfast"] = str(breakfast_count)
        self.data_dict["Total PB Bars"] = str(pb_count)
        self.data_dict["Total Custom"] = str(custom_count)
        self.data_dict["Storefront Customers"] = str(app_orders)
        self.data_dict["Meals per App Order"] = str(round(meal_per_order, 2))
        self.data_dict["Meals to Sell"] = str(meals_to_sell)

        return self.data_dict

    def create_finances_data_dict(self, data):
        self.data_dict_finances = {
            "Total Gross": "",
            "Total Discounts": "",
            "Total Net": "",
            "Total Taxes": "",
            "Total Sales": "",
            "Total Paid": "",
            "Total Credit Used": "",
            "Dollar per App Order": ""
        }

        gross_column = [self.clean_and_convert_to_float(row[16]) for row in data[1:]]
        discount_column = [self.clean_and_convert_to_float(row[17]) for row in data[1:]]
        net_column = [self.clean_and_convert_to_float(row[18]) for row in data[1:]]
        tax_column = [self.clean_and_convert_to_float(row[19]) for row in data[1:]]
        sales_column = [self.clean_and_convert_to_float(row[20]) for row in data[1:]]
        credit_column = [self.clean_and_convert_to_float(row[21]) for row in data[1:]]
        paid_column = [self.clean_and_convert_to_float(row[22]) for row in data[1:]]
        unique_numbers = set()
        number_of_rows = [int(row[2]) for row in data[1:] if
                          (int(row[2]) not in unique_numbers) and unique_numbers.add(int(row[2])) is None]
        app_orders = len(number_of_rows)
        dollar_per_order = round(sum(gross_column) / app_orders, 2)

        self.data_dict_finances["Total Gross"] = str(round(sum(gross_column), 2))
        self.data_dict_finances["Total Discounts"] = str(round(sum(discount_column), 2))
        self.data_dict_finances["Total Net"] = str(round(sum(net_column), 2))
        self.data_dict_finances["Total Taxes"] = str(round(sum(tax_column), 2))
        self.data_dict_finances["Total Sales"] = str(round(sum(sales_column), 2))
        self.data_dict_finances["Total Credit Used"] = str(round(sum(credit_column), 2))
        self.data_dict_finances["Total Paid"] = str(round(sum(paid_column), 2))
        self.data_dict_finances["Dollar per App Order"] = str(dollar_per_order)

        for key in self.data_dict_finances:
            self.data_dict_finances[key] = locale.currency(self.clean_and_convert_to_float(self.data_dict_finances[key]), grouping=True)

        return self.data_dict_finances

    def create_finances_data_dict_compare(self, compare_data):
        self.compare_data_dict_finances = self.data_dict_finances.copy()

        gross_column = [self.clean_and_convert_to_float(row[16]) for row in compare_data[1:]]
        discount_column = [self.clean_and_convert_to_float(row[17]) for row in compare_data[1:]]
        net_column = [self.clean_and_convert_to_float(row[18]) for row in compare_data[1:]]
        tax_column = [self.clean_and_convert_to_float(row[19]) for row in compare_data[1:]]
        sales_column = [self.clean_and_convert_to_float(row[20]) for row in compare_data[1:]]
        credit_column = [self.clean_and_convert_to_float(row[21]) for row in compare_data[1:]]
        paid_column = [self.clean_and_convert_to_float(row[22]) for row in compare_data[1:]]
        unique_numbers = set()
        number_of_rows = [int(row[2]) for row in compare_data[1:] if
                          (int(row[2]) not in unique_numbers) and unique_numbers.add(int(row[2])) is None]
        app_orders = len(number_of_rows)
        dollar_per_order = round(sum(gross_column) / app_orders, 2)

        self.compare_data_dict_finances["Total Gross"] = str(round(sum(gross_column), 2))
        self.compare_data_dict_finances["Total Discounts"] = str(round(sum(discount_column), 2))
        self.compare_data_dict_finances["Total Net"] = str(round(sum(net_column), 2))
        self.compare_data_dict_finances["Total Taxes"] = str(round(sum(tax_column), 2))
        self.compare_data_dict_finances["Total Sales"] = str(round(sum(sales_column), 2))
        self.compare_data_dict_finances["Total Credit Used"] = str(round(sum(credit_column), 2))
        self.compare_data_dict_finances["Total Paid"] = str(round(sum(paid_column), 2))
        self.compare_data_dict_finances["Dollar per App Order"] = str(dollar_per_order)

        for key in self.compare_data_dict_finances:
            self.compare_data_dict_finances[key] = locale.currency(self.clean_and_convert_to_float(self.compare_data_dict_finances[key]),
                                                                   grouping=True)

        return self.compare_data_dict_finances

    def create_finances_data_dict_compare_sum(self):
        self.compare_data_dict_finances_sum = self.compare_data_dict_finances.copy()

        for key in self.compare_data_dict_finances_sum:
            self.compare_data_dict_finances_sum[key] = self.calculate_percent_difference(
                self.clean_and_convert_to_float(self.compare_data_dict_finances[key].replace('$', '').replace(',', '')),
                self.clean_and_convert_to_float(self.data_dict_finances[key].replace('$', '').replace(',', '')))

            splitValue = self.compare_data_dict_finances_sum[key].split('(')

            firstPart = locale.currency(self.clean_and_convert_to_float(splitValue[0]), grouping=True)

            self.compare_data_dict_finances_sum[key] = firstPart + ' (' + str(splitValue[1])

        return self.compare_data_dict_finances_sum

    def create_finances_square_data_dict(self, square_data, qbo_data):
        gross_column = [self.clean_and_convert_to_float(row[5].replace('$', '').replace(',', '')) for row in square_data[1:]]
        discount_column = [self.clean_and_convert_to_float(row[8].replace('$', '').replace(',', '')) for row in square_data[1:]]
        net_column = [self.clean_and_convert_to_float(row[9].replace('$', '').replace(',', '')) for row in square_data[1:]]
        tax_column = [self.clean_and_convert_to_float(row[10].replace('$', '').replace(',', '')) for row in square_data[1:]]

        float_values = [self.clean_and_convert_to_float(value) for value in qbo_data.values() if '.' in value]
        expression_sum = sum(float_values)

        # Calculate and update data_dict
        self.data_dict_finances_square = {
            "Total Gross": 0.0,
            "Total Discounts": 0.0,
            "Total Taxes": 0.0,
            "Total Net": 0.0,
            "Total Paid": 0.0,
            "Total Credit Used": 0.0,
            "Total Sales": 0.0,
            "Square Gross": round(sum(gross_column), 2),
            "Square Discounts": -round(sum(discount_column), 2),
            "Square Net": round(sum(net_column), 2),
            "Square Taxes": round(sum(tax_column), 2),
            "Total App Gross": self.clean_and_convert_to_float(self.data_dict_finances["Total Gross"].replace('$', '').replace(',', '')),
            "Dollar per App Order": self.clean_and_convert_to_float(self.data_dict_finances["Dollar per App Order"].replace('$', '').replace(',', '')),
            "Avg Storefront Spend": round(sum(gross_column), 2) / self.clean_and_convert_to_float(self.data_dict["Storefront Customers"]),
            "QBO Gross": expression_sum
        }

        self.data_dict_finances_square["Total Gross"] = self.clean_and_convert_to_float(
            self.data_dict_finances["Total Gross"].replace('$', '').replace(',', '')) + \
                                                        self.data_dict_finances_square["Square Gross"] + \
                                                        self.data_dict_finances_square["QBO Gross"]
        self.data_dict_finances_square["Total Discounts"] = self.clean_and_convert_to_float(
            self.data_dict_finances["Total Discounts"].replace('$', '').replace(',', '')) + \
                                                            self.data_dict_finances_square["Square Discounts"]
        self.data_dict_finances_square["Total Taxes"] = self.clean_and_convert_to_float(
            self.data_dict_finances["Total Taxes"].replace('$', '').replace(',', '')) + \
                                                        self.data_dict_finances_square[
                                                            "Square Taxes"]
        self.data_dict_finances_square["Total Net"] = self.clean_and_convert_to_float(
            self.data_dict_finances["Total Net"].replace('$', '').replace(',', '')) + \
                                                      self.data_dict_finances_square[
                                                          "Square Net"]
        self.data_dict_finances_square["Total Paid"] = self.clean_and_convert_to_float(
            self.data_dict_finances["Total Paid"].replace('$', '').replace(',', ''))
        self.data_dict_finances_square["Total Credit Used"] = self.clean_and_convert_to_float(
            self.data_dict_finances["Total Credit Used"].replace('$', '').replace(',', ''))
        self.data_dict_finances_square["Total Sales"] = self.clean_and_convert_to_float(
            self.data_dict_finances["Total Sales"].replace('$', '').replace(',', ''))

        for key in self.data_dict_finances_square:
            self.data_dict_finances_square[key] = locale.currency(self.clean_and_convert_to_float(self.data_dict_finances_square[key]),
                                                                  grouping=True)

        return self.data_dict_finances_square

    def create_finances_square_data_dict_compare(self, square_data, qbo_data):
        gross_column = [self.clean_and_convert_to_float(row[5].replace('$', '').replace(',', '')) for row in square_data[1:]]
        discount_column = [self.clean_and_convert_to_float(row[8].replace('$', '').replace(',', '')) for row in square_data[1:]]
        net_column = [self.clean_and_convert_to_float(row[9].replace('$', '').replace(',', '')) for row in square_data[1:]]
        tax_column = [self.clean_and_convert_to_float(row[10].replace('$', '').replace(',', '')) for row in square_data[1:]]

        float_values = [self.clean_and_convert_to_float(value) for value in qbo_data.values() if '.' in value]
        expression_sum = sum(float_values)

        # Calculate and update data_dict
        self.data_dict_finances_square_compare = {
            "Total Gross": 0.0,
            "Total Discounts": 0.0,
            "Total Taxes": 0.0,
            "Total Net": 0.0,
            "Total Paid": 0.0,
            "Total Credit Used": 0.0,
            "Total Sales": 0.0,
            "Square Gross": round(sum(gross_column), 2),
            "Square Discounts": -round(sum(discount_column), 2),
            "Square Net": round(sum(net_column), 2),
            "Square Taxes": round(sum(tax_column), 2),
            "Total App Gross": self.clean_and_convert_to_float(self.compare_data_dict_finances["Total Gross"].replace('$', '').replace(',', '')),
            "Dollar per App Order": self.clean_and_convert_to_float(
                self.compare_data_dict_finances["Dollar per App Order"].replace('$', '').replace(',', '')),
            "Avg Storefront Spend":  round(sum(gross_column), 2) / self.clean_and_convert_to_float(self.compare_data_dict["Storefront Customers"]),
            "QBO Gross": expression_sum
        }

        self.data_dict_finances_square_compare["Total Gross"] = self.clean_and_convert_to_float(
            self.compare_data_dict_finances["Total Gross"].replace('$', '').replace(',', '')) + \
                                                                self.data_dict_finances_square_compare["Square Gross"] + self.data_dict_finances_square_compare["QBO Gross"]
        self.data_dict_finances_square_compare["Total Discounts"] = self.clean_and_convert_to_float(
            self.compare_data_dict_finances["Total Discounts"].replace('$', '').replace(',', '')) + \
                                                                    self.data_dict_finances_square_compare[
                                                                        "Square Discounts"]
        self.data_dict_finances_square_compare["Total Taxes"] = self.clean_and_convert_to_float(
            self.compare_data_dict_finances["Total Taxes"].replace('$', '').replace(',', '')) + \
                                                                self.data_dict_finances_square_compare[
                                                                    "Square Taxes"]
        self.data_dict_finances_square_compare["Total Net"] = self.clean_and_convert_to_float(
            self.compare_data_dict_finances["Total Net"].replace('$', '').replace(',', '')) + \
                                                              self.data_dict_finances_square_compare[
                                                                  "Square Net"]
        self.data_dict_finances_square_compare["Total Paid"] = self.clean_and_convert_to_float(
            self.compare_data_dict_finances["Total Paid"].replace('$', '').replace(',', ''))
        self.data_dict_finances_square_compare["Total Credit Used"] = self.clean_and_convert_to_float(
            self.compare_data_dict_finances["Total Credit Used"].replace('$', '').replace(',', ''))
        self.data_dict_finances_square_compare["Total Sales"] = self.clean_and_convert_to_float(
            self.compare_data_dict_finances["Total Sales"].replace('$', '').replace(',', ''))

        for key in self.data_dict_finances_square_compare:
            self.data_dict_finances_square_compare[key] = locale.currency(
                self.clean_and_convert_to_float(self.data_dict_finances_square_compare[key]),
                grouping=True)

        return self.data_dict_finances_square_compare

    def create_finances_square_data_dict_compare_sum(self):
        self.data_dict_finances_square_compare_sum = self.data_dict_finances_square_compare.copy()

        for key in self.data_dict_finances_square_compare_sum:
            self.data_dict_finances_square_compare_sum[key] = self.calculate_percent_difference(
                self.clean_and_convert_to_float(self.data_dict_finances_square_compare[key].replace('$', '').replace(',', '')),
                self.clean_and_convert_to_float(self.data_dict_finances_square[key].replace('$', '').replace(',', '')))

            splitValue = self.data_dict_finances_square_compare_sum[key].split('(')

            firstPart = locale.currency(self.clean_and_convert_to_float(splitValue[0]), grouping=True)

            self.data_dict_finances_square_compare_sum[key] = firstPart + ' (' + str(splitValue[1])

        return self.data_dict_finances_square_compare_sum

    def create_employees_data_dict(self, data):
        regular_hours = self.clean_and_convert_to_float(data[-1][15])
        overtime_hours = self.clean_and_convert_to_float(data[-1][16])
        total_hours = str(round(regular_hours + (overtime_hours * 1.5), 2))

        self.employee_data_dict = {
            "Leckie Hours": data[-1][15],
            "Leckie OT Hours": data[-1][16],
            "Leckie Total Hours": total_hours,
            "Hours per $1000": "",
            "Hours per Items": "",
        }

        if self.data_dict_finances_square is not None:
            total_gross_string = str(self.data_dict_finances_square["Total Gross"]).replace('$', '').replace(',', '')

            square_hours_per_1000 = round(
                self.clean_and_convert_to_float(self.employee_data_dict["Leckie Total Hours"])
                / (self.clean_and_convert_to_float(total_gross_string) / 1000), 2)

            self.employee_data_dict["Hours per $1000"] = str(square_hours_per_1000)

        else:
            hours_per_1000 = round(
                self.clean_and_convert_to_float(self.employee_data_dict["Leckie Total Hours"])
                / (self.clean_and_convert_to_float(self.data_dict_finances["Total Gross"].replace('$', '').replace(',', '')) / 1000), 2)
            self.employee_data_dict["Hours per $1000"] = str(hours_per_1000)

        hours_per_items = round(
            self.clean_and_convert_to_float(self.employee_data_dict["Leckie Total Hours"]) / self.clean_and_convert_to_float(self.data_dict["Meals Pre Ordered"]), 2)

        self.employee_data_dict["Hours per Items"] = str(hours_per_items)

        return self.employee_data_dict

    def create_employees_data_dict_compare(self, data):
        regular_hours = self.clean_and_convert_to_float(data[-1][15])
        overtime_hours = self.clean_and_convert_to_float(data[-1][16])
        total_hours = str(round(regular_hours + (overtime_hours * 1.5), 2))

        self.employee_data_dict_compare = {
            "Leckie Hours": data[-1][15],
            "Leckie OT Hours": data[-1][16],
            "Leckie Total Hours": total_hours,
            "Hours per $1000": "",
            "Hours per Items": "",
        }

        if self.data_dict_finances_square_compare is not None:
            total_gross_string = str(self.data_dict_finances_square_compare["Total Gross"]).replace('$', '').replace(',', '')

            square_hours_per_1000 = round(
                self.clean_and_convert_to_float(self.employee_data_dict_compare["Leckie Total Hours"])
                / (self.clean_and_convert_to_float(total_gross_string) / 1000), 2)

            self.employee_data_dict_compare["Hours per $1000"] = str(square_hours_per_1000)

        elif self.compare_data_dict_finances is not None:
            hours_per_1000 = round(
                self.clean_and_convert_to_float(self.employee_data_dict_compare["Leckie Total Hours"])
                / (self.clean_and_convert_to_float(self.compare_data_dict_finances["Total Gross"].replace('$', '').replace(',', '')) / 1000), 2)
            self.employee_data_dict_compare["Hours per $1000"] = str(hours_per_1000)

        else:
            hours_per_1000 = round(
                self.clean_and_convert_to_float(self.employee_data_dict_compare["Leckie Total Hours"])
                / (self.clean_and_convert_to_float(self.data_dict_finances["Total Gross"].replace('$', '').replace(',', '')) / 1000), 2)
            self.employee_data_dict_compare["Hours per $1000"] = str(hours_per_1000)

        hours_per_items = round(
            self.clean_and_convert_to_float(self.employee_data_dict_compare["Leckie Total Hours"]) / self.clean_and_convert_to_float(self.data_dict["Meals Pre Ordered"]), 2)

        self.employee_data_dict_compare["Hours per Items"] = str(hours_per_items)

        return self.employee_data_dict_compare

    def create_employees_data_dict_compare_sum(self):
        self.employee_data_dict_compare_sum = {
            "Leckie Hours": "",
            "Leckie OT Hours": "",
            "Leckie Total Hours": "",
            "Hours per $1000": "",
            "Hours per Items": "",
        }

        for key in self.employee_data_dict_compare_sum:
            self.employee_data_dict_compare_sum[key] = self.calculate_percent_difference(
                self.clean_and_convert_to_float(self.employee_data_dict_compare[key]),
                self.clean_and_convert_to_float(self.employee_data_dict[key]))

        return self.employee_data_dict_compare_sum

    def create_table_items(self, data_dict, table, labels, pie_chart_series=None, compare_sum=False,
                           compare_sum_finances=False, bar_set=None):
        def handle_double_clicked_slice(slice_item):
            if slice_item.label().__contains__("Large") or slice_item.label().__contains__("Small"):
                global global_pie_chart_window
                print(slice_item.label(), slice_item.value())

                if global_pie_chart_window:
                    global_pie_chart_window.close()

                pie_chart_window = QWidget()
                pie_chart_window.setWindowTitle(slice_item.label())
                pie_chart_window.setGeometry(200, 200, 600, 400)

                # Create a layout for the pie chart window
                layout = QVBoxLayout(pie_chart_window)

                # Create a scene and set its background brush
                scene = QGraphicsScene(pie_chart_window)
                scene.setBackgroundBrush(QBrush(QColor(50, 56, 66)))

                series = QtCharts.QPieSeries()

                item_data_dict = self.data[next((path for path in self.selected_file_paths if 'kelowna' in path.lower()), None)]

                df = pd.DataFrame(item_data_dict[1:], columns=item_data_dict[0])
                desired_size = str(slice_item.label()).split('(')[0].replace(" ", "")

                if slice_item.label().__contains__("Large") or slice_item.label().__contains__("Small"):
                    prep_numbers = df[df['Size'] == desired_size]['Prep No.'].tolist()
                    numbers_list = list(map(int, prep_numbers))
                    # Use Counter to count occurrences
                    numbers_count = Counter(numbers_list)
                    # Convert Counter to a dictionary
                    numbers_dict = dict(numbers_count)
                    filtered_dict = {key: value for key, value in numbers_dict.items() if key <= 5}
                    pie_value = sum(filtered_dict.values())

                    # Add slices to the pie chart
                    for prep_no, count in filtered_dict.items():
                        if prep_no > 5:
                            break
                        percent = (count / pie_value * 100)
                        custom_label = f"Meal #{prep_no} ({percent:.2f}%)"
                        slice_item = QtCharts.QPieSlice(custom_label, count)
                        slice_item.setLabelColor("#ffffff")
                        slice_item.setLabelFont(QFont("Segoe UI", 14))
                        series.append(slice_item)
                        series.setLabelsVisible()

                # Create a pie chart
                chart = QChart()
                chart.legend().hide()  # Hide the legend
                chart.addSeries(series)

                chart_view = QChartView(chart)
                chart_view.setRenderHint(QPainter.Antialiasing)
                chart_view.chart().setBackgroundBrush(QBrush(QColor(50, 56, 66)))

                layout.addWidget(chart_view, stretch=1)  # Set stretch to 1 to make it expand

                # Store a reference to the window
                global_pie_chart_window = pie_chart_window

                pie_chart_window.show()

        def handle_clicked_slice(slice_item):
            if pie_chart_series is not None:
                for slice_item_series in pie_chart_series.slices():
                    slice_item_series.setExploded(False)

            slice_item.setExploded(True)

        table.clear()

        table.setColumnCount(2)

        table.setColumnWidth(0, 250)
        table.setColumnWidth(1, 250)
        table.setHorizontalHeaderLabels(labels)
        table.setRowCount(data_dict.__len__())

        if pie_chart_series is not None:
            pie_chart_series.clear()
            keys_to_exclude = ["Storefront Customers", "Meals per App Order", "Meals to Sell", "Meals Pre Ordered"]
            filtered_data_dict = {key: value for key, value in data_dict.items() if key not in keys_to_exclude}
            total_value = sum(int(value) for key, value in filtered_data_dict.items())
            for item_pie, additional_item_pie in filtered_data_dict.items():
                custom_label = f"{item_pie.replace('Total', '')} ({(self.clean_and_convert_to_float(additional_item_pie) / total_value * 100):.2f}%)"
                slice_item = QPieSlice(custom_label, int(additional_item_pie))
                slice_item.setLabelColor("#ffffff")
                slice_item.setLabelFont(QFont("Segoe UI", 14))
                pie_chart_series.append(slice_item)
                pie_chart_series.setLabelsVisible()

            if self.pie_charts_connected.__contains__(pie_chart_series):
                pie_chart_series.clicked.disconnect()
                pie_chart_series.doubleClicked.disconnect()
                self.pie_charts_connected.remove(pie_chart_series)

            pie_chart_series.clicked.connect(handle_clicked_slice)
            pie_chart_series.doubleClicked.connect(handle_double_clicked_slice)
            self.pie_charts_connected.append(pie_chart_series)

        row = 0
        for item, additional_item in data_dict.items():
            tableItem = QTableWidgetItem(item)
            additionalTableItem = QTableWidgetItem(additional_item)
            tableItem.setFlags(tableItem.flags() ^ Qt.ItemFlag.ItemIsEditable)
            additionalTableItem.setFlags(additionalTableItem.flags() ^ Qt.ItemFlag.ItemIsEditable)
            table.setItem(row, 0, tableItem)
            table.setItem(row, 1, additionalTableItem)

            if bar_set is not None:
                bar_set.append(self.clean_and_convert_to_float(additional_item.replace('$', '').replace(',', '')))

            if compare_sum:
                if self.clean_and_convert_to_float(additional_item.split("(")[0]) >= 0:
                    # Set the text color to green for the QTableWidgetItem
                    brush = QBrush(QColor(0, 255, 0))
                    additionalTableItem.setForeground(brush)
                elif self.clean_and_convert_to_float(additional_item.split("(")[0]) < 0:
                    # Set the text color to green for the QTableWidgetItem
                    brush = QBrush(QColor(255, 0, 0))
                    additionalTableItem.setForeground(brush)

            if compare_sum_finances:
                if self.clean_and_convert_to_float(additional_item.replace('$', '').replace(',', '').split("(")[0]) >= 0:
                    # Set the text color to green for the QTableWidgetItem
                    brush = QBrush(QColor(0, 255, 0))
                    additionalTableItem.setForeground(brush)
                elif self.clean_and_convert_to_float(additional_item.replace('$', '').replace(',', '').split("(")[0]) < 0:
                    # Set the text color to green for the QTableWidgetItem
                    brush = QBrush(QColor(255, 0, 0))
                    additionalTableItem.setForeground(brush)
            row += 1

    def calculate_percent_difference(self, new_value, original_value):
        difference = new_value - original_value
        percent_difference = self.clean_and_convert_to_float((difference / original_value) * 100)
        return f"{difference:.2f} ({percent_difference:.2f}%)"

    def parse_data(self, compare_file=False):
        for widget in MainFunctions.created_widgets:
            self.removeSelectedWidget(widget)

        MainFunctions.created_widgets.clear()

        def clear_data(compare=False):
            if compare:
                self.compare_data_dict = None
                self.compare_data_dict_sum = None
                self.compare_data_dict_finances = None
                self.compare_data_dict_finances_sum = None
                self.data_dict_finances_square_compare = None
                self.data_dict_finances_square_compare_sum = None
                self.employee_data_dict_compare = None
                self.employee_data_dict_compare_sum = None
                self.compare_data = {}
                self.selected_file_compare_paths = None

            elif not compare:
                self.data_dict = None
                self.data_dict_finances = None
                self.data_dict_finances_square = None
                self.employee_data_dict = None
                self.data = {}
                self.selected_file_paths = None
                MainFunctions.is_file_selected = False
                MainFunctions.show_select_file(self, self.select_file_button)

        clear_data(compare_file)

        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        dialog.setNameFilter("Supported files (*.csv *.xlsx)")
        if dialog.exec():
            if not compare_file:
                self.selected_file_paths = dialog.selectedFiles()
            elif compare_file:
                self.selected_file_compare_paths = dialog.selectedFiles()

            try:
                if not compare_file:
                    if len(self.selected_file_paths) < 4:
                        raise ValueError("Not enough files selected.")
                    if len(self.selected_file_paths) > 5:
                        raise ValueError("Too many files selected.")
                    for file_path in self.selected_file_paths:
                        if file_path.endswith('.csv'):
                            with open(file_path, 'r', encoding='utf-8') as csv_file:
                                csv_reader = csv.reader(csv_file)
                                self.data[file_path] = list(csv_reader)
                        elif file_path.endswith('.xlsx'):
                            df = pd.read_excel(file_path)
                            self.data[file_path] = df.values.tolist()
                        else:
                            raise ValueError("Unsupported file format")
                elif compare_file:
                    if len(self.selected_file_compare_paths) < 4:
                        raise ValueError("Not enough files selected.")
                    if len(self.selected_file_compare_paths) > 5:
                        raise ValueError("Too many files selected.")
                    for file_path in self.selected_file_compare_paths:
                        if file_path.endswith('.csv'):
                            with open(file_path, 'r', encoding='utf-8') as csv_file:
                                csv_reader = csv.reader(csv_file)
                                self.compare_data[file_path] = list(csv_reader)
                        elif file_path.endswith('.xlsx'):
                            df = pd.read_excel(file_path)
                            self.compare_data[file_path] = df.values.tolist()
                        else:
                            raise ValueError("Unsupported file format")

                if not compare_file:
                    selected_path = next((path for path in self.selected_file_paths if 'kelowna' in path.lower()), None)
                    selected_path_square = next((path for path in self.selected_file_paths if 'item' in path.lower()),
                                                None)
                    selected_path_employees = next((path for path in self.selected_file_paths if 'shifts' in path.lower()),
                                                   None)
                    selected_path_prep = next((path for path in self.selected_file_paths if 'pages' in path.lower()), None)
                    selected_path_qbo = next((path for path in self.selected_file_paths if 'inc' in path.lower()), None)
                    if selected_path is None or selected_path_square is None or selected_path_employees is None or selected_path_prep is None or selected_path_qbo is None:
                        raise ValueError("Incorrect files selected.")

                    self.ui.file_path_label.setText(selected_path)
                    self.date_range_file = self.get_date_range_file()

                elif compare_file:
                    selected_path_compare = next((path for path in self.selected_file_compare_paths if 'kelowna' in path.lower()), None)
                    selected_path_square_compare = next((path for path in self.selected_file_compare_paths if 'item' in path.lower()),
                                                None)
                    selected_path_employees_compare = next(
                        (path for path in self.selected_file_compare_paths if 'shifts' in path.lower()),
                        None)
                    selected_path_prep_compare = next((path for path in self.selected_file_compare_paths if 'pages' in path.lower()),
                                              None)
                    selected_path_qbo_compare = next((path for path in self.selected_file_compare_paths if 'inc' in path.lower()), None)
                    if selected_path_compare is None or selected_path_square_compare is None or selected_path_employees_compare is None or selected_path_prep_compare is None or selected_path_qbo_compare is None:
                        raise ValueError("Incorrect files selected.")

                    self.ui.label_2.setText(selected_path_compare)
                    self.date_range_compare_file = self.get_date_range_compare_file()

                MainFunctions.is_file_selected = True
                MainFunctions.occupy_tabs(self)
                MainFunctions.show_orders(self, self.orders_button)

            except FileNotFoundError:
                self.show_error_message("File not found.")
                clear_data(False)
                clear_data(True)
            except PermissionError:
                self.show_error_message("Permission denied.")
                clear_data(False)
                clear_data(True)
            except ValueError as e:
                self.show_error_message(str(e))
                print(e)
                clear_data(False)
                clear_data(True)
            except Exception as e:
                self.show_error_message(str(e))
                print(e)
                clear_data(False)
                clear_data(True)
            except UnicodeDecodeError as e:
                self.show_error_message(str(e))
                print(e)
                clear_data(False)
                clear_data(True)

    def get_date_range_file(self):
        return re.search(r'(\w+ \d{1,2}, \d{4} - \w+ \d{1,2}, \d{4})', self.ui.file_path_label.text()).group(1) \
            if re.search(r'(\w+ \d{1,2}, \d{4} - \w+ \d{1,2}, \d{4})', self.ui.file_path_label.text()) \
            else self.date_range_file

    def get_date_range_compare_file(self):
        return re.search(r'(\w+ \d{1,2}, \d{4} - \w+ \d{1,2}, \d{4})', self.ui.label_2.text()).group(1) \
            if re.search(r'(\w+ \d{1,2}, \d{4} - \w+ \d{1,2}, \d{4})', self.ui.label_2.text()) \
            else self.date_range_file

    @staticmethod
    def show_error_message(message):
        message_box = QMessageBox()
        message_box.setIcon(QMessageBox.Icon.Critical)
        message_box.setWindowTitle("Error")
        message_box.setText("Error")
        message_box.setInformativeText(message)
        message_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        message_box.exec()

    @staticmethod
    def removeSelectedWidget(widget):
        try:
            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()
        except Exception as e:
            # Handle the exception or log it, but do not pause further code execution.
            pass

    @staticmethod
    def clean_and_convert_to_float(value):
        try:
            # If the value is already a float or int, return it as is
            if isinstance(value, (float, int)):
                return value

            # If the value is None or not a string, return a default or log an error
            if value is None or not isinstance(value, str):
                print(f"Invalid value for conversion: {value}")
                return 0.0  # or handle it differently

            # Remove non-numeric characters, then convert to float
            cleaned_value = re.sub(r'[^\d\.-]', '', value)
            return float(cleaned_value)

        except ValueError as e:
            print(f"Error converting value to float: {value} - Error: {e}")
            return 0.0  # or handle it differently

        except Exception as e:
            print(f"Unexpected error during conversion: {e}")
            return 0.0  # or handle it differently


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("logo.ico"))
    window = MainWindow()
    sys.exit(app.exec())
