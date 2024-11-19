class CalculadoraLogica:
    def __init__(self):
        pass

    def calcular_resultado(self, expresion):
        """Calcula el resultado de la expresión ingresada."""
        try:
            resultado = eval(expresion)  # Evalúa la operación matemática
            return resultado
        except Exception as e:
            raise ValueError("Error en la operación: " + str(e))

    def generar_arbol(self, expresion):
        """Genera una representación estructurada del árbol de derivación."""
        arbol = []

        def analizar_expresion(expr):
            if '+' in expr:
                izq, der = expr.split('+', 1)
                return ('Suma', analizar_expresion(izq.strip()), analizar_expresion(der.strip()))
            elif '-' in expr:
                izq, der = expr.split('-', 1)
                return ('Resta', analizar_expresion(izq.strip()), analizar_expresion(der.strip()))
            elif '*' in expr:
                izq, der = expr.split('*', 1)
                return ('Multiplicación', analizar_expresion(izq.strip()), analizar_expresion(der.strip()))
            elif '/' in expr:
                izq, der = expr.split('/', 1)
                return ('División', analizar_expresion(izq.strip()), analizar_expresion(der.strip()))
            else:
                return expr

        arbol = analizar_expresion(expresion)
        return arbol
