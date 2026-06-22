import tkinter as tk
from tkinter import filedialog, messagebox
import math
from datetime import datetime



COLOR_FONDO = "#0F172A"
COLOR_PANEL = "#1E293B"
COLOR_BOTON = "#334155"
COLOR_CIENTIFICO = "#4F46E5"
COLOR_IGUAL = "#22C55E"
COLOR_C = "#DC2626"
COLOR_BORRAR = "#F59E0B"

ARCHIVO_HISTORIAL = "historial.txt"



root = tk.Tk()
root.title("Calculadora Profesional 2.0")
root.geometry("1200x700")
root.configure(bg=COLOR_FONDO)
root.resizable(False, False)



def escribir(valor):
    entrada.insert(tk.END, valor)

def limpiar():
    entrada.delete(0, tk.END)

def borrar():
    texto = entrada.get()
    entrada.delete(0, tk.END)
    entrada.insert(0, texto[:-1])

def guardar_historial(expresion, resultado):

    fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    linea = f"[{fecha}] {expresion} = {resultado}\n"

    with open(ARCHIVO_HISTORIAL, "a", encoding="utf-8") as archivo:
        archivo.write(linea)

    historial.config(state="normal")
    historial.insert(tk.END, linea)
    historial.see(tk.END)
    historial.config(state="disabled")

def calcular():

    try:

        expresion_original = entrada.get()

        expresion = expresion_original.replace("^", "**")
        expresion = expresion.replace("π", str(math.pi))

        resultado = eval(
            expresion,
            {"__builtins__": None},
            {
                "sqrt": math.sqrt,
                "sin": math.sin,
                "cos": math.cos,
                "tan": math.tan,
                "log": math.log10,
                "pi": math.pi
            }
        )

        guardar_historial(expresion_original, resultado)

        entrada.delete(0, tk.END)
        entrada.insert(0, str(resultado))

    except Exception as e:

        messagebox.showerror(
            "Error",
            f"Operación inválida\n\n{e}"
        )

def cargar_historial():

    try:

        with open(
            ARCHIVO_HISTORIAL,
            "r",
            encoding="utf-8"
        ) as archivo:

            contenido = archivo.read()

            historial.config(state="normal")
            historial.insert(tk.END, contenido)
            historial.config(state="disabled")

    except FileNotFoundError:
        pass

def limpiar_historial():

    open(
        ARCHIVO_HISTORIAL,
        "w",
        encoding="utf-8"
    ).close()

    historial.config(state="normal")
    historial.delete(1.0, tk.END)
    historial.config(state="disabled")

def exportar_historial():

    ruta = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Archivo TXT", "*.txt")]
    )

    if not ruta:
        return

    contenido = historial.get("1.0", tk.END)

    with open(ruta, "w", encoding="utf-8") as archivo:
        archivo.write(contenido)

    messagebox.showinfo(
        "Exportado",
        "Historial exportado correctamente."
    )



barra_menu = tk.Menu(root)

menu_archivo = tk.Menu(barra_menu, tearoff=0)

menu_archivo.add_command(
    label="Exportar Historial",
    command=exportar_historial
)

menu_archivo.add_separator()

menu_archivo.add_command(
    label="Salir",
    command=root.destroy
)

barra_menu.add_cascade(
    label="Archivo",
    menu=menu_archivo
)

root.config(menu=barra_menu)



frame_calc = tk.Frame(
    root,
    bg=COLOR_PANEL
)

frame_calc.pack(
    side="left",
    fill="both",
    expand=True,
    padx=15,
    pady=15
)

titulo = tk.Label(
    frame_calc,
    text="CALCULADORA PROFESIONAL",
    bg=COLOR_PANEL,
    fg="#38BDF8",
    font=("Segoe UI", 22, "bold")
)

titulo.pack(pady=15)

entrada = tk.Entry(
    frame_calc,
    font=("Consolas", 26),
    justify="right",
    bg="#020617",
    fg="white",
    insertbackground="white",
    relief="flat"
)

entrada.pack(
    fill="x",
    padx=20,
    pady=10,
    ipady=15
)



frame_control = tk.Frame(
    frame_calc,
    bg=COLOR_PANEL
)

frame_control.pack(pady=10)

tk.Button(
    frame_control,
    text="C",
    width=8,
    height=2,
    bg=COLOR_C,
    fg="white",
    font=("Segoe UI", 12, "bold"),
    relief="flat",
    command=limpiar
).pack(side="left", padx=5)

tk.Button(
    frame_control,
    text="⌫",
    width=8,
    height=2,
    bg=COLOR_BORRAR,
    fg="white",
    font=("Segoe UI", 12, "bold"),
    relief="flat",
    command=borrar
).pack(side="left", padx=5)



frame_cientifico = tk.Frame(
    frame_calc,
    bg=COLOR_PANEL
)

frame_cientifico.pack(pady=10)

cientificos = [
    ("√", "sqrt("),
    ("sin", "sin("),
    ("cos", "cos("),
    ("tan", "tan("),
    ("log", "log("),
    ("π", "π")
]

for texto, valor in cientificos:

    tk.Button(
        frame_cientifico,
        text=texto,
        width=8,
        height=2,
        bg=COLOR_CIENTIFICO,
        fg="white",
        relief="flat",
        font=("Segoe UI", 11, "bold"),
        command=lambda v=valor: escribir(v)
    ).pack(side="left", padx=4)



frame_botones = tk.Frame(
    frame_calc,
    bg=COLOR_PANEL
)

frame_botones.pack(pady=10)

botones = [
    ["(", ")", "%", "/"],
    ["7", "8", "9", "*"],
    ["4", "5", "6", "-"],
    ["1", "2", "3", "+"],
    ["0", ".", "^", "="]
]

for fila in botones:

    fila_frame = tk.Frame(
        frame_botones,
        bg=COLOR_PANEL
    )

    fila_frame.pack()

    for texto in fila:

        if texto == "=":
            color = COLOR_IGUAL
            comando = calcular
        else:
            color = COLOR_BOTON
            comando = lambda t=texto: escribir(t)

        tk.Button(
            fila_frame,
            text=texto,
            width=8,
            height=2,
            bg=color,
            fg="white",
            relief="flat",
            font=("Segoe UI", 14, "bold"),
            command=comando
        ).pack(
            side="left",
            padx=3,
            pady=3
        )



frame_historial = tk.Frame(
    root,
    bg="#020617",
    width=350
)

frame_historial.pack(
    side="right",
    fill="y",
    padx=15,
    pady=15
)

titulo_historial = tk.Label(
    frame_historial,
    text="HISTORIAL",
    bg="#020617",
    fg="#22C55E",
    font=("Segoe UI", 18, "bold")
)

titulo_historial.pack(pady=10)

historial = tk.Text(
    frame_historial,
    bg="#0F172A",
    fg="white",
    font=("Consolas", 11),
    state="disabled"
)

historial.pack(
    fill="both",
    expand=True,
    padx=10,
    pady=10
)

tk.Button(
    frame_historial,
    text="Limpiar Historial",
    bg="#B91C1C",
    fg="white",
    relief="flat",
    command=limpiar_historial
).pack(
    fill="x",
    padx=10,
    pady=10
)



root.bind("<Return>", lambda e: calcular())
root.bind("<Escape>", lambda e: limpiar())
root.bind("<Delete>", lambda e: limpiar())
root.bind("<BackSpace>", lambda e: borrar())


cargar_historial()

root.mainloop()
