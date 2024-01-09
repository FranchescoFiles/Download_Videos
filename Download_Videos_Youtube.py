import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from pytube import YouTube

def download_video(url, download_format):
    try:
        yt = YouTube(url, on_progress_callback=progress_callback)

        #en_esta_parte_del_codigo_obtenemos_la_ubicacion_para_guardar_el_file
        destination_folder = filedialog.askdirectory()

        if download_format == "MP3":
            # Descarga_como_MP3
            audio_stream = yt.streams.filter(only_audio=True).first()
            audio_stream.download(output_path=destination_folder)
        elif download_format == "MP4":
            # Descarga_como_MP4
            video_stream = yt.streams.get_highest_resolution()
            video_stream.download(output_path=destination_folder)

        status_label.config(text="Descarga Completa")
    except Exception as e:
        status_label.config(text=f"Error: {str(e)}")

def progress_callback(stream, chunk, remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - remaining
    percentage = (bytes_downloaded / total_size) * 100
    progress_var.set(percentage)
    root.update_idletasks()  #en_esta_parte_Actualizamos_la_interfaz_gráfica

def on_format_change(*args):
    selected_format = format_var.get()
    if selected_format == "MP3":
        #aqui_Eliminamos_el_rastreo_existente_version_audio
        progress_var.trace_variable("w", lambda *args: None)
        status_label.config(text="Seleccionado MP3 (Audio)")
    elif selected_format == "MP4":
        #aqui_Eliminamos_el_rastreo_existente_version_video
        progress_var.trace_variable("w", lambda *args: None)
        status_label.config(text="Seleccionado MP4 (Video)")


#en esta parte Configuramos la ventana principal
root = tk.Tk()
root.title("Descarga videos de YouTube free")

# en esta parte haremos los campos y etiquetas
url_label = tk.Label(root, text="URL:")
url_entry = tk.Entry(root, width=40)
format_label = tk.Label(root, text="Formato:")
format_var = tk.StringVar(root)
format_var.set("MP4")  # Valor predeterminado
format_dropdown = tk.OptionMenu(root, format_var, "MP3", "MP4")
download_button = tk.Button(root, text="Descargar", command=lambda: download_video(url_entry.get(), format_var.get()))
status_label = tk.Label(root, text="Progreso de descarga:")
progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100, length=200)

#en esta parte organizaremos los widgets en la ventana
url_label.grid(row=0, column=0, padx=5, pady=5)
url_entry.grid(row=0, column=1, padx=5, pady=5)
format_label.grid(row=1, column=0, padx=5, pady=5)
format_dropdown.grid(row=1, column=1, padx=5, pady=5)
download_button.grid(row=2, column=0, columnspan=2, pady=10)
status_label.grid(row=3, column=0, columnspan=2)
progress_bar.grid(row=4, column=0, columnspan=2, pady=10)

format_var.trace_add("write", on_format_change)

#en esta parte iniciamos la app
root.mainloop()
