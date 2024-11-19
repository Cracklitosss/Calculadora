import tkinter as tk
from tkinter import messagebox
from logica_calculadora import CalculadoraLogica


class CalculadoraApp:
    def __init__(self, root):
        self.logica = CalculadoraLogica()
        self.root = root
        self.root.title("Calculadora Avanzada")
        self.root.geometry("1100x800")
        self.root.configure(bg="#2C3333")

        # Marco principal
        marco_principal = tk.Frame(self.root, bg="#2C3333")
        marco_principal.pack(fill="both", expand=True, padx=20, pady=20)

        # Marco calculadora
        marco_calculadora = tk.Frame(marco_principal, bg="#395B64", padx=15, pady=15)
        marco_calculadora.pack(side="left", fill="y", padx=20)

        # Encabezado
        etiqueta_encabezado = tk.Label(
            marco_calculadora,
            text="Calculadora Avanzada",
            font=("Roboto", 24, "bold"),
            bg="#395B64",
            fg="#E7F6F2",
        )
        etiqueta_encabezado.pack(pady=15)

        # Entrada de texto
        self.entrada_var = tk.StringVar()
        self.entrada_texto = tk.Entry(
            marco_calculadora,
            textvariable=self.entrada_var,
            font=("Roboto Mono", 20),
            width=20,
            bg="#A5C9CA",
            fg="#2C3333",
            bd=0,
            relief="flat",
            justify="right",
            insertbackground="#2C3333",
        )
        self.entrada_texto.pack(pady=15, ipady=10)

        # Resultado
        self.resultado_var = tk.StringVar()
        etiqueta_resultado = tk.Label(
            marco_calculadora,
            textvariable=self.resultado_var,
            font=("Roboto Mono", 28, "bold"),
            bg="#395B64",
            fg="#E7F6F2",
            height=2,
        )
        etiqueta_resultado.pack(pady=15)

        # Marco de botones
        marco_botones = tk.Frame(marco_calculadora, bg="#395B64")
        marco_botones.pack(pady=15, expand=True, fill="both")

        # Configurar el grid para que se expanda
        for i in range(5):  # 5 filas
            marco_botones.grid_rowconfigure(i, weight=1)
        for i in range(4):  # 4 columnas
            marco_botones.grid_columnconfigure(i, weight=1)

        # Botones
        botones = [
            ("C", 0, 0, "#E7F6F2", "#2C3333"), ("(", 0, 1), (")", 0, 2), ("/", 0, 3, "#A5C9CA", "#2C3333"),
            ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("*", 1, 3, "#A5C9CA", "#2C3333"),
            ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("-", 2, 3, "#A5C9CA", "#2C3333"),
            ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("+", 3, 3, "#A5C9CA", "#2C3333"),
            ("0", 4, 0, None, None, 2), (".", 4, 2), ("=", 4, 3, "#E7F6F2", "#2C3333"),
        ]

        for boton in botones:
            if len(boton) >= 5:
                texto, fila, columna, bg_color, fg_color = boton[:5]
                colspan = boton[5] if len(boton) > 5 else 1
            else:
                texto, fila, columna = boton
                bg_color, fg_color = "#395B64", "#E7F6F2"
                colspan = 1

            tk.Button(
                marco_botones,
                text=texto,
                font=("Roboto", 16, "bold"),
                width=4,
                height=1,
                bg=bg_color,
                fg=fg_color,
                bd=0,
                relief="flat",
                activebackground="#A5C9CA",
                activeforeground="#2C3333",
                command=lambda t=texto: self.clic_boton(t),
            ).grid(row=fila, column=columna, columnspan=colspan, padx=3, pady=3, sticky="nsew")

        # Marco del árbol
        marco_arbol = tk.Frame(marco_principal, bg="#395B64", padx=15, pady=15)
        marco_arbol.pack(side="left", fill="both", expand=True, padx=20)

        etiqueta_arbol = tk.Label(
            marco_arbol,
            text="Árbol de Derivación",
            font=("Roboto", 20, "bold"),
            bg="#395B64",
            fg="#E7F6F2",
        )
        etiqueta_arbol.pack(pady=15)

        # Canvas
        self.lienzo_arbol = tk.Canvas(
            marco_arbol, 
            width=600, 
            height=500, 
            bg="#A5C9CA", 
            bd=0, 
            highlightthickness=0
        )
        self.lienzo_arbol.pack(fill="both", expand=True)

    def clic_boton(self, caracter):
        if caracter == "=":
            try:
                expresion = self.entrada_var.get()
                if not self.parentesis_balanceados(expresion):
                    messagebox.showerror("Error", "Los paréntesis no están balanceados")
                    return
                resultado = self.logica.calcular_resultado(expresion)
                self.resultado_var.set(resultado)
                arbol = self.logica.generar_arbol(expresion)
                self.dibujar_arbol(arbol)
            except Exception as e:
                messagebox.showerror("Error", str(e))
        elif caracter == "C":
            self.limpiar()
        else:
            self.entrada_var.set(self.entrada_var.get() + caracter)

    def parentesis_balanceados(self, expresion):
        """Verifica si los paréntesis están correctamente balanceados"""
        contador = 0
        for char in expresion:
            if char == '(':
                contador += 1
            elif char == ')':
                contador -= 1
            if contador < 0:
                return False
        return contador == 0

    def dibujar_arbol(self, arbol, x=300, y=30, coords_padre=None):
        """Dibuja el árbol de derivación en el lienzo."""
        self.lienzo_arbol.delete("all")
        radio_nodo = 25

        def dibujar_nodo(x, y, texto, coords_padre=None):
            # Dibuja círculo con nuevo estilo
            self.lienzo_arbol.create_oval(
                x - radio_nodo,
                y - radio_nodo,
                x + radio_nodo,
                y + radio_nodo,
                fill="#E7F6F2",
                outline="#395B64",
                width=2
            )
            self.lienzo_arbol.create_text(
                x, y, 
                text=texto, 
                font=("Roboto", 12, "bold"), 
                fill="#2C3333"
            )
            if coords_padre:
                self.lienzo_arbol.create_line(
                    coords_padre[0], 
                    coords_padre[1] + radio_nodo,
                    x, 
                    y - radio_nodo,
                    width=2,
                    fill="#395B64"
                )

        def recorrer_arbol(nodo, x, y, coords_padre=None):
            if isinstance(nodo, tuple):
                texto, izq, der = nodo
                dibujar_nodo(x, y, texto, coords_padre)
                recorrer_arbol(izq, x - 100, y + 80, (x, y))
                recorrer_arbol(der, x + 100, y + 80, (x, y))
            else:
                dibujar_nodo(x, y, nodo, coords_padre)

        recorrer_arbol(arbol, x, y)

    def limpiar(self):
        """Limpia la entrada y el resultado."""
        self.entrada_var.set("")
        self.resultado_var.set("")
        self.lienzo_arbol.delete("all")


if __name__ == "__main__":
    root = tk.Tk()
    app = CalculadoraApp(root)
    root.mainloop()
