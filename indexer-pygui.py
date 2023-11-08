import PySimpleGUI as sg
import sqlite3
from pathlib import Path

# Constants
DB_NAME = "index.sqlite3"
TABLE_NAME = "FileIndex"

def create_index_table(db):
    db.execute(f"CREATE TABLE IF NOT EXISTS {TABLE_NAME} (id INTEGER PRIMARY KEY, absolute_path TEXT UNIQUE, file_name TEXT, size_bytes INTEGER, content_type TEXT ALLOW NULL)")

def connect_to_database(folder):
    db_file = folder / DB_NAME
    return sqlite3.connect(str(db_file))

def index_folder(window, folder):
    db = connect_to_database(folder)
    create_index_table(db)

    records = []
    file_count = 0
    for file in folder.rglob("*"):
        window.write_event_value("indexer_msg", file_count)
        records.append((str(file.resolve()), file.name, file.stat().st_size, file.suffix))
        file_count +=1
    
    with db:
        db.executemany(f"INSERT OR IGNORE INTO {TABLE_NAME}(absolute_path, file_name, size_bytes, content_type) VALUES(?, ?, ?, ?)", records)

def get_available_file_extensions(folder):
    db = connect_to_database(folder)
    with db:
        extensions = [ext[0] for ext in db.execute("SELECT DISTINCT(content_type) FROM FileIndex")]
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

    db = connect_to_database(folder)
    with db:
        files = [f"{file[0]} - {human_readable_filesize(file[1])}" for file in db.execute(sql, query_params)]
    return files

def main():
    layout = [
        [sg.Text("Folder"), sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"), sg.FolderBrowse()],
        [sg.Column([[sg.Button("Index this folder", key="index_btn", visible=False), sg.Button("Reindex this folder", key="reindex_btn", visible=False)]])],
        [sg.Text("", key="index_counter"), sg.Text("Search by name and file extension...", key="search_instructions", visible=False)],
        [sg.Input("", key="search_input", visible=False), sg.Combo(['Any'], key="extension_combo", visible=False, size=(10, 1))],
        [sg.Listbox(values=[], key="file_list", size=(70, 6), visible=False)],
        [sg.Button("Search", key="search_btn", visible=False)]
    ]

    window = sg.Window("Indexer", layout, resizable=True)

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, "Exit"):
            break

        if event == "-FOLDER-":
            folder = Path(values["-FOLDER-"])
            if (folder / DB_NAME).is_file():
                window["reindex_btn"].update(visible=True)
                window["search_instructions"].update(visible=True)
                window["search_input"].update(visible=True)
                window["extension_combo"].update(visible=True, values=get_available_file_extensions(folder))
                window["file_list"].update(visible=True)
                window["search_btn"].update(visible=True)
            else:
                window["index_btn"].update(visible=True)

        if event == "index_btn" or event == "reindex_btn":
            window["index_btn"].update(disabled=True)
            window["index_counter"].update(visible=True)
            window.start_thread(lambda: index_folder(window, folder), "index_completed")

        if event == "indexer_msg":
            window["index_counter"].update(f"Indexed {values['indexer_msg']} files...")

        if event == "search_btn":
            files = search_files(folder, values['search_input'], values['extension_combo'])
            window["file_list"].update(values=files)

        elif event == "index_completed":
            sg.popup("Your folder has been indexed!")
            window["index_btn"].update(disabled=False, visible=False)
            window["reindex_btn"].update(disabled=False, visible=True)
            window["search_instructions"].update(visible=True)
            window["index_counter"].update(visible=False)
            window["search_input"].update(visible=True)
            window["extension_combo"].update(visible=True, values=get_available_file_extensions(folder))
            window["file_list"].update(visible=True)
            window["search_btn"].update(visible=True)

    window.close()

if __name__ == "__main__":
    main()