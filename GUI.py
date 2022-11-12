import PySimpleGUI as sg
import sqlite3
from prettytable import PrettyTable, ALL
import textwrap
from crawler.crawler.settings import WEBSITE

#--------------------FOR TESTING ONLY
#--------------------RUN THIS FILE 4TH TO ACCESS DATA--------------------
class GUI():
    def __init__(self):
        con = sqlite3.connect("%s/%s.db"%(WEBSITE,WEBSITE))
        cur = con.cursor()

        upper = [[sg.Text('INPUT: ', font=('',12,''))],
                        [sg.Multiline(enable_events=True, font=('Cascadia Mono',12), size=(500,100), key='-INPUT-', no_scrollbar=True)]]

        mid = [[sg.Button('RUN', expand_x=True, key='-RUN-')]]

        low = [[sg.Text('OUTPUT:', font=('',12,''))],[sg.Multiline(key='-OUTPUT-', size=(500,1000),
                        font=('Cascadia Mono',12), reroute_cprint=True, write_only=True, no_scrollbar=True)]]

        # ----- Full layout -----

        layout = [
            [sg.Column(upper, size=(1000,200), scrollable=True)],
            [mid],
            [sg.Column(low, size=(1000,300), scrollable=True)]
        ]

        # ----- Window interface -----

        window = sg.Window('SQLITE lite', layout)

        while True:
            event, values = window.read()

            if event in (None, 'Exit'):
                break
            if event == '-RUN-':
                try:
                    script = values['-INPUT-']
                    cur.execute(script)
                    myTable = PrettyTable()
                    myTable.hrules = ALL
                    wrapper = textwrap.TextWrapper(width=50)
                    for c in cur.fetchall():
                        list_c=list(c)
                        for i in range(len(list_c)):
                            list_c[i] = wrapper.fill(text=str(list_c[i]))
                        c = tuple(list_c)
                        myTable.add_row(c)
                    window['-OUTPUT-'].update(myTable)
                except Exception as e:
                    window['-OUTPUT-'].update(e)

        window.close()
        con.close()
