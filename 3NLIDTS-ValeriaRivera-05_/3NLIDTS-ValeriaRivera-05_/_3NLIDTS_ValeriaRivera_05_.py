import tkinter as tk
from tkinter import ttk, messagebox
import re
# =========================
# CONFIGURACIÓN DE LA APP
# =========================
COLOR_FONDO = "#F3F5F9"
COLOR_TARJETA = "#FFFFFF"
COLOR_PRIMARIO = "#3657D5"
COLOR_TEXTO = "#202B45"
COLOR_SECUNDARIO = "#68738A"

FUENTE = ("Segoe UI", 10)
FUENTE_TITULO = ("Segoe UI", 20, "bold")
# =========================
# VALIDACIONES
# =========================
def texto_valido(valor):
    """Admite letras, espacios, apóstrofes y guiones."""
    valor = valor.strip()

    return (
        bool(valor)
        and all(
            caracter.isalpha() or caracter.isspace()
            or caracter in "-'’"
            for caracter in valor
        )
    )

def telefono_valido(valor):
    """Acepta exactamente diez dígitos."""
    return bool(re.fullmatch(r"\d{10}", valor.strip()))


def validar_edad(valor):
    """Comprueba que la edad sea un entero entre 1 y 120."""
    try:
        edad = int(valor.strip())
        return 1 <= edad <= 120
    except ValueError:
        return False

def validar_estatura(valor):
    """Acepta estaturas positivas con punto o coma decimal."""
    try:
        estatura = float(valor.strip().replace(",", "."))
        return 0 < estatura < 300
    except ValueError:
        return False
# =========================
# FUNCIONES DEL FORMULARIO
# =========================

def limpiar_campos():
    """Limpia todos los campos y restablece la selección."""
    for campo in campos.values():
        campo.delete(0, tk.END)

    var_genero.set("")
    campos["Nombres"].focus_set()

def guardar_datos():
    """Valida y guarda los datos en un archivo de texto."""

    datos = {
        nombre: campo.get().strip()
        for nombre, campo in campos.items()
    }

    errores = []

    if not texto_valido(datos["Nombres"]):
        errores.append(
            "• Nombres: introduce letras y espacios válidos."
        )

    if not texto_valido(datos["Apellidos"]):
        errores.append(
            "• Apellidos: introduce letras y espacios válidos."
        )

    if not telefono_valido(datos["Teléfono"]):
        errores.append(
            "• Teléfono: debe contener exactamente 10 dígitos."
        )

    if not validar_edad(datos["Edad"]):
        errores.append(
            "• Edad: introduce un entero entre 1 y 120."
        )

    if not validar_estatura(datos["Estatura"]):
        errores.append(
            "• Estatura: introduce un número positivo menor de 300 cm."
        )

    genero = var_genero.get()

    if not genero:
        errores.append("• Selecciona una opción de género.")

    if errores:
        messagebox.showerror(
            "Revisa los datos",
            "Corrige los siguientes campos:\n\n"
            + "\n".join(errores),
            parent=ventana
        )
        return

    try:
        estatura = float(
            datos["Estatura"].replace(",", ".")
        )

        registro = (
            f"Nombres: {datos['Nombres']}\n"
            f"Apellidos: {datos['Apellidos']}\n"
            f"Teléfono: {datos['Teléfono']}\n"
            f"Edad: {datos['Edad']} años\n"
            f"Estatura: {estatura:g} cm\n"
            f"Género: {genero}\n"
            f"{'-' * 35}\n"
        )

        with open("datos.txt", "a", encoding="utf-8") as archivo:
            archivo.write(registro)

        messagebox.showinfo(
            "Registro guardado",
            "Los datos se guardaron correctamente en datos.txt.",
            parent=ventana
        )

        limpiar_campos()

    except OSError as error:
        messagebox.showerror(
            "Error al guardar",
            f"No fue posible guardar el archivo.\n\n{error}",
            parent=ventana
        )
# =========================
# VENTANA PRINCIPAL
# =========================

ventana = tk.Tk()
ventana.title("Registro de información personal")
ventana.geometry("540x690")
ventana.minsize(500, 650)
ventana.configure(bg=COLOR_FONDO)

# Estilos de los componentes ttk
estilo = ttk.Style()
estilo.theme_use("clam")

estilo.configure(
    "TLabel",
    background=COLOR_TARJETA,
    foreground=COLOR_TEXTO,
    font=FUENTE
)

estilo.configure(
    "TEntry",
    padding=9,
    font=FUENTE
)

estilo.configure(
    "TRadiobutton",
    background=COLOR_TARJETA,
    foreground=COLOR_TEXTO,
    font=FUENTE
)

estilo.configure(
    "Guardar.TButton",
    background=COLOR_PRIMARIO,
    foreground="#FFFFFF",
    padding=(18, 10),
    font=("Segoe UI", 10, "bold"),
    borderwidth=0
)

estilo.map(
    "Guardar.TButton",
    background=[("active", "#2945B0")]
)

estilo.configure(
    "Borrar.TButton",
    background="#E9EDF5",
    foreground=COLOR_TEXTO,
    padding=(18, 10),
    font=FUENTE,
    borderwidth=0
)

estilo.map(
    "Borrar.TButton",
    background=[("active", "#DCE2EF")]
)
# =========================
# ENCABEZADO
# =========================

encabezado = tk.Frame(
    ventana,
    bg=COLOR_FONDO,
    padx=28,
    pady=20
)
encabezado.pack(fill="x")

tk.Label(
    encabezado,
    text="Registro personal",
    font=FUENTE_TITULO,
    fg=COLOR_TEXTO,
    bg=COLOR_FONDO
).pack(anchor="w")

tk.Label(
    encabezado,
    text="Completa los campos para registrar tu información.",
    font=("Segoe UI", 10),
    fg=COLOR_SECUNDARIO,
    bg=COLOR_FONDO
).pack(anchor="w", pady=(4, 0))

# =========================
# TARJETA DEL FORMULARIO
# =========================

tarjeta = tk.Frame(
    ventana,
    bg=COLOR_TARJETA,
    padx=26,
    pady=22,
    highlightbackground="#E0E5EF",
    highlightthickness=1
)
tarjeta.pack(fill="both", expand=True, padx=24, pady=(0, 24))

tk.Label(
    tarjeta,
    text="INFORMACIÓN PERSONAL",
    font=("Segoe UI", 10, "bold"),
    fg=COLOR_PRIMARIO,
    bg=COLOR_TARJETA
).pack(anchor="w", pady=(0, 16))

# Crear los campos sin repetir código
campos = {}
def crear_campo(nombre):
    """Crea una etiqueta y su campo de entrada."""
    tk.Label(
        tarjeta,
        text=nombre,
        font=("Segoe UI", 10, "bold"),
        fg=COLOR_TEXTO,
        bg=COLOR_TARJETA
    ).pack(anchor="w", pady=(0, 5))

    entrada = ttk.Entry(tarjeta)
    entrada.pack(fill="x", pady=(0, 13))

    campos[nombre] = entrada

crear_campo("Nombres")
crear_campo("Apellidos")
crear_campo("Teléfono")
crear_campo("Edad")
crear_campo("Estatura")
# =========================
# SELECCIÓN DE GÉNERO
# =========================

tk.Label(
    tarjeta,
    text="Género",
    font=("Segoe UI", 10, "bold"),
    fg=COLOR_TEXTO,
    bg=COLOR_TARJETA
).pack(anchor="w", pady=(0, 7))

var_genero = tk.StringVar(value="")

contenedor_genero = tk.Frame(
    tarjeta,
    bg=COLOR_TARJETA
)
contenedor_genero.pack(anchor="w", pady=(0, 20))

for opcion in ("Hombre", "Mujer", "Otro"):
    ttk.Radiobutton(
        contenedor_genero,
        text=opcion,
        variable=var_genero,
        value=opcion
    ).pack(side="left", padx=(0, 18))
# =========================
# BOTONES DE ACCIÓN
# =========================
contenedor_botones = tk.Frame(
    tarjeta,
    bg=COLOR_TARJETA
)
contenedor_botones.pack(fill="x", side="bottom")

ttk.Button(
    contenedor_botones,
    text="Guardar registro",
    style="Guardar.TButton",
    command=guardar_datos
).pack(side="left", fill="x", expand=True, padx=(0, 8))

ttk.Button(
    contenedor_botones,
    text="Limpiar",
    style="Borrar.TButton",
    command=limpiar_campos
).pack(side="left", padx=(8, 0))

campos["Nombres"].focus_set()

ventana.mainloop()
