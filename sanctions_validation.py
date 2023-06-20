import requests 
import pandas
import tkinter as tk
from tkinter import filedialog
from lxml import etree
from constants import SANCTIONS_URLS

class XMLValidatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Sanctions Validator App')

        self.create_widgets()
        self.resize_window()

    def create_widgets(self):
        self.label = tk.Label(self, text='Excel file path:')
        self.label.pack()

        self.entry = tk.Entry(self)
        self.entry.pack()

        self.browse_button = tk.Button(self, text='Browse', command=self.browse_file)
        self.browse_button.pack()

        self.button = tk.Button(self, text='Fetch Sanctions', command=self.fetch_sanctions)
        self.button.pack()

    def resize_window(self):
        window_width = 400
        window_height = 200
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_cordinate = int((screen_width / 2) - (window_width / 2))
        y_cordinate = int((screen_height / 2) - (window_height / 2))
        self.geometry(f'{window_width}x{window_height}+{x_cordinate}+{y_cordinate}')


    def fetch_sanctions(self):
        accounts = read_input_excel(self.entry.get())

        for sanction_url in SANCTIONS_URLS:
            response = requests.get(sanction_url)
            if response.status_code == 200:
                analyse_xml(response.content, accounts)
            else:
                print(f'There was an error accessing: {sanction_url}')

    def browse_file(self):
        filetypes = (('Excel Files', '*.xlsx'), ('All Files', '*.*'))
        filename = filedialog.askopenfilename(filetypes=filetypes)
        self.entry.delete(0, tk.END)
        self.entry.insert(0, filename)
        

def read_input_excel(excel):
    pd = pandas.read_excel(excel)
    accounts = pd['Account Number'].tolist()
    return accounts

def analyse_xml(xml_content):
    root = etree.fromstring(xml_content)

if __name__ == '__main__':
    app = XMLValidatorApp()
    app.mainloop()
