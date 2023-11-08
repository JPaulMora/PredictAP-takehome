import PySimpleGUI as sg
import time

left_col = [
    [
        sg.Text("Folder"),
        sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
        sg.FolderBrowse(),
    ]
]

layout = [[sg.Column(left_col, element_justification="c"), sg.Button("Index this folder", key='index_btn', visible=False)], [sg.Text('', key='index_counter')]]
window = sg.Window("Multiple Format Image Viewer", layout, resizable=True)


def index_folder(folder):
    i = 0
    while i < 30:
        time.sleep(0.1)
        window.write_event_value('indexer_msg', i)
        i += 1


while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, "Exit"):
        break
    if event == "-FOLDER-":
        folder = values["-FOLDER-"]
        window['index_btn'].Update(visible = True)
    
    if event == "index_btn":
        window['index_btn'].Update(disabled = True)
        window.start_thread(lambda: index_folder(folder), 'index_completed')

    if event == "indexer_msg":
        window['index_counter'].Update(f"Indexed {values['indexer_msg']} files...")

    elif event == "index_completed":
        sg.popup("Your folder has been indexed!")
        window['index_btn'].Update(disabled = False)
        window['index_counter'].Update(visible=False)

window.close()
