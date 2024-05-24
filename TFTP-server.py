import FreeSimpleGUI as sg
import tftpy
import threading

server_state = False                     #Server in OFF state


def server_connection(server):
    print('TFTP server started...')
    server.listen('0.0.0.0', 71)        #Making the server to listen on port 71


def gui_start():
    global server_state
    layout = [
        [sg.Text('Select Image folder path')],
        [sg.InputText(key='-FOLDER-'), sg.FolderBrowse()],
        [sg.Button('Start Server'), sg.Button('Stop Server'), sg.Button('Exit')],
        [sg.Output(size=(60, 10))]
    ]

    window = sg.Window('TFTP Server', layout)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == 'Exit':
            break

        folder_path = values['-FOLDER-']

        if event == 'Start Server':
            if not folder_path:
                sg.popup_error('Please select a directory first.')
                continue
            server = tftpy.TftpServer(folder_path)
            threading.Thread(target=server_connection, args=(server,)).start()
            server_state = False
            print(f"TFTP server started serving files from {folder_path}")

        elif event == 'Stop Server':
            if server_state:
                server.stop()
                print("TFTP server stopped.")
            else:
                print("TFTP server is not running.")

    window.close()


if __name__ == '__main__':
    gui_start()
