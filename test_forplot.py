import matplotlib.pyplot as plt
from datahandler import DataHandler


def main():
    data_handler = DataHandler()
    data = data_handler.get_all_data()
    data = data / data.iloc[0]

