import threading
import time

from datetime import timedelta

import PySimpleGUI as sg

from .timer import Timer

class Layout:
    timer_column = [
        [
            sg.Text('Overall Elapsed:', size=(18))
        ]
    ]

    split_column = [
         [
            sg.Text('Splits:', size=(18))
        ]
    ]

    layout = [
    [
        sg.Column(timer_column),
        sg.VSeperator(),
        sg.Column(split_column),
    ]
]

class TimerGUI(Timer):

    def __init__(self, num_splits=10):
        Timer.__init__(self)
        self.timer_column: list = []
        self.split_column: list = []
        self.button_column: list = []
        self.layout: list = []
        self.windows: sg.Window = None
        self.num_splits: int = num_splits
        self.font: str = 'Arial'
        self._gui_threads: dict = {}

    def open_gui(self):
        self._get_layout()
        self.window = sg.Window("Time Split", self.layout)
        while True:
            event, values = self.window.read()
            if event == "Exit" or event == sg.WIN_CLOSED:
                break
            if event == 'Start':
                self._reset_splits()
                self.start()
                self._start_gui_threads()
            if event == 'Split':
                self._add_split_to_gui('Split')
            if event == 'Stop':
                self._add_split_to_gui('Stopped')
                self.stop()

    def _get_layout(self):
        self.timer_column = [
            [sg.Text(self.overall_elapsed, key='-OVERALL_ELAPSED-', size=12, font=(self.font, 36), text_color='white')],
            [sg.Text(self.current_elapsed, key='-CURRENT_ELAPSED-', size=12, font=(self.font, 24), text_color='yellow')]
        ]

        self.button_column = [
            [
                sg.Button("Start"),
                sg.Button("Split"),
                sg.Button("Stop"),
                sg.VerticalSeparator(),
                sg.Button("Save")
            ]
        ]
        
        for i in range(self.num_splits):
            index = i + 1
            self.split_column.append(
                [
                    sg.Text('', size=10, key=f'-SPLIT{index}_ELAPSED-'),
                    sg.Text('', size=25, key=f'-SPLIT{index}_SPLIT_TIME-'),
                    sg.Text('', size=30, key=f'-SPLIT{index}_DESC-')
                ]
            )


        self.layout = [
            [
                sg.Column(self.timer_column, expand_x=True),
                sg.VSeparator(),
                sg.Column(self.split_column, expand_x=True)
            ],
            [
                sg.Column(self.button_column, expand_x=True)
            ]
        ]


    def _start_gui_threads(self):
        if self._update_text.__name__ not in self._gui_threads:
            self._gui_threads[self._update_text.__name__] = threading.Thread(target=self._update_text, daemon=True)
            self._gui_threads[self._update_text.__name__].start()

    def _update_text(self):
        while True:
            self.window['-OVERALL_ELAPSED-'].update(str(timedelta(seconds=self.overall_elapsed))[:-3])
            self.window['-CURRENT_ELAPSED-'].update(str(timedelta(seconds=self.current_elapsed))[:-3])
            self.window.refresh()
            time.sleep(0.001)

    def _add_split_to_gui(self, desc):
        if self._running:
            split = self.split(desc)
            index = len(self.splits)
            if f'-SPLIT{index}_ELAPSED-' not in self.window.AllKeysDict:
                index = 1
            keys = {
                f'-SPLIT{index}_ELAPSED-': split.elapsed,
                f'-SPLIT{index}_SPLIT_TIME-': split.split_time,
                f'-SPLIT{index}_DESC-': split.description
            }
            for key in keys:
                self.window[key].update(keys[key])

    def _reset_splits(self):
        for i in range(self.num_splits):
            index = i + 1
            self.window[f'-SPLIT{index}_ELAPSED-'].update('')
            self.window[f'-SPLIT{index}_SPLIT_TIME-'].update('')
            self.window[f'-SPLIT{index}_DESC-'].update('')
        self.window.refresh()
            
