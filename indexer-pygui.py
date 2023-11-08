import PySimpleGUI as sg
import sqlite3
from pathlib import Path

left_col = [
    [
        sg.Text("Folder"),
        sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
        sg.FolderBrowse(),
    ]
]

layout = [
    [
        sg.Column(left_col, element_justification="c"),
        sg.Button("Index this folder", key="index_btn", visible=False),
        sg.Button("Reindex this folder", key="reindex_btn", visible=False),
    ],
    [sg.Text("", key="index_counter"), sg.Text("Search by name and file extension...", key="search_instructions", visible=False)],
    [sg.Input("", key="search_input", visible=False), sg.Combo(['Any'], key="extension_combo", visible=False, size=10)],
    [sg.Listbox(values=[], key="file_list", size=(70, 6), visible=False,)],
    [sg.Button("Search", key="search_btn", visible=False)]
]
window = sg.Window("Indexer", layout, resizable=True)

def index_folder(folder):
    db = sqlite3.connect(folder + "/index.sqlite3")
    db.execute(
        "CREATE TABLE IF NOT EXISTS FileIndex (id INTEGER PRIMARY KEY, absolute_path TEXT UNIQUE, file_name TEXT, size_bytes INTEGER, content_type TEXT ALLOW NULL)"
    )

    records = []
    file_count = 0
    for file in Path(folder).rglob("*"):
        records.append((str(file.resolve()), file.name, file.stat().st_size, file.suffix))
        file_count += 1
        window.write_event_value("indexer_msg", file_count)

    db.executemany(
        "INSERT OR IGNORE INTO FileIndex(absolute_path ,file_name, size_bytes, content_type) VALUES(?, ?, ?, ?)",
        records,
    )
    db.commit()
    db.close()

def get_available_file_extensions(folder):
    db = sqlite3.connect(folder + "/index.sqlite3")
    extensions = [ext[0] for ext in db.execute("SELECT distinct(content_type) from FileIndex")]
    db.close()

    extensions.append('Any')
    return extensions

def human_readable_filesize(size):
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti']:
        if abs(size) < 1024.0:
            return f"{size:.1f}{unit}B"
        size /= 1024.0


def search_files(folder, name, file_ext=None):
    sql = "SELECT file_name, size_bytes FROM FileIndex WHERE file_name LIKE ?"
    query_params = ("%" + name + "%",)
    if file_ext not in ["Any", None, ""]:
        sql += " AND content_type = ?"
        query_params += (file_ext,)
    
    db = sqlite3.connect(folder + "/index.sqlite3")
    files = []
    for file in db.execute(sql, query_params):
        files.append(f"{file[0]} - {human_readable_filesize(file[1])}")
    db.close()
    return files


while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, "Exit"):
        break
    if event == "-FOLDER-":
        folder = values["-FOLDER-"]
        if Path(folder + "/index.sqlite3").is_file():
            window["reindex_btn"].Update(visible=True)
            window["search_instructions"].Update(visible=True)
            window["search_input"].Update(visible=True)
            window["extension_combo"].Update(visible=True, values=get_available_file_extensions(folder))
            window["file_list"].Update(visible=True)
            window["search_btn"].Update(visible=True)
            
        else:
            window["index_btn"].Update(visible=True)

    if event == "index_btn" or event == "reindex_btn":
        window["index_btn"].Update(disabled=True)
        window.start_thread(lambda: index_folder(folder), "index_completed")

    if event == "indexer_msg":
        window["index_counter"].Update(f"Indexed {values['indexer_msg']} files...")

    if event == "search_btn":
        window["file_list"].Update(values=search_files(folder, values['search_input'], values['extension_combo']))

    elif event == "index_completed":
        sg.popup("Your folder has been indexed!")
        window["index_btn"].Update(disabled=False, visible=False)
        window["reindex_btn"].Update(disabled=False, visible=True)
        window["search_instructions"].Update(visible=True)

        window["index_counter"].Update(visible=False)
        window["search_input"].Update(visible=True)
        window["extension_combo"].Update(visible=True, values=get_available_file_extensions(folder))
        window["file_list"].Update(visible=True)
        window["search_btn"].Update(visible=True)

window.close()
