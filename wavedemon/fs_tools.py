import pathlib

def create_m3u(playlist_name, folder_path):
    """
    Run after downloading a playlist and deposit file into
    playlist folder
    Return bool on success/fail

    Keyword arguments:
    playlist_name - Name of playlist
    folder_path - Path to playlist folder

    """
    try:
        m3u_file = open(file=f"{folder_path}\\{playlist_name}.m3u", encoding='UTF-8')
        file_list = [x for x in pathlib.Path(folder_path).glob('**/*') if x.is_file()]
        for file in file_list:
            m3u_file.writelines(f"{file}\\r\\n")
        m3u_file.close()
        return True
    except OSError():
        return False

def create_directory(folder_path: pathlib.Path()):
    """
    Just check if the path exists and create if not
    Return bool on success/fail

    Keyword arguments:
    folder_path - Path we gotta create

    """
    if not folder_path.exists() or folder_path.is_file():
        folder_path.mkdir()
        return True
    return False
