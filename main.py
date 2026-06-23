import math
from datetime import datetime
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.utils import get_color_from_hex

HISTORIAL_FILE = "historial.txt"

class CalculadoraApp(App):
    def build(self):
        Window.clearcolor = get_color_from_hex("#0F172A")
        self.historial_texto = ""

        root = BoxLayout(orientation='horizontal', padding=10, spacing=10)

        # Panel izquierdo — calculadora
        panel_calc = BoxLayout(orientation='vertical', spacing=8, size_hint=(0.65, 1))

        titulo = Label(
            text="CALCULADORA PROFESIONAL",
            font_size='18sp',
            bold=True,
            color=get_color_from_hex("#38BDF8"),
            size_hint_y=None,
            height=50
        )
        panel_calc.add_widget(titulo)

        self.entrada = TextInput(
            font_size='28sp',
            multiline=False,
            halign='right',
            background_color=get_color_from_hex("#020617"),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(1, 1, 1, 1),
            size_hint_y=None,
            height=70
        )
        panel_calc.add_widget(self.entrada)

        # Botones C y borrar
        fila_ctrl = BoxLayout(size_hint_y=None, height=55, spacing=6)
        fila_ctrl.add_widget(self._btn("C", "#DC2626", self.limpiar))
        fila_ctrl.add_widget(self._btn("⌫", "#F59E0B", self.borrar))
        panel_calc.add_widget(fila_ctrl)

        # Botones científicos
        fila_cien = GridLayout(cols=6, size_hint_y=None, height=55, spacing=4)
        cientificos = [("√", "sqrt("), ("sin", "sin("), ("cos", "cos("),
                       ("tan", "tan("), ("log", "log("), ("π", "pi")]
        for texto, val in cientificos:
            fila_cien.add_widget(self._btn(texto, "#4F46E5", lambda v=val: self.escribir(v)))
        panel_calc.add_widget(fila_cien)

        # Teclado numérico
        teclas = [
            ["(", ")", "%", "/"],
            ["7", "8", "9", "*"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["0", ".", "^", "="],
        ]
        grid = GridLayout(cols=4, spacing=5)
        for fila in teclas:
            for t in fila:
                if t == "=":
                    grid.add_widget(self._btn(t, "#22C55E", self.calcular))
                else:
                    grid.add_widget(self._btn(t, "#334155", lambda v=t: self.escribir(v)))
        panel_calc.add_widget(grid)

        root.add_widget(panel_calc)

        # Panel derecho — historial
        panel_hist = BoxLayout(orientation='vertical', spacing=6, size_hint=(0.35, 1))

        panel_hist.add_widget(Label(
            text="HISTORIAL",
            font_size='16sp',
            bold=True,
            color=get_color_from_hex("#22C55E"),
            size_hint_y=None,
            height=40
        ))

        scroll = ScrollView()
        self.lbl_historial = Label(
            text="",
            font_size='11sp',
            color=(1, 1, 1, 1),
            halign='left',
            valign='top',
            text_size=(None, None),
            size_hint_y=None
        )
        self.lbl_historial.bind(texture_size=lambda inst, val: setattr(inst, 'height', val[1]))
        self.lbl_historial.bind(width=lambda inst, val: setattr(inst, 'text_size', (val, None)))
        scroll.add_widget(self.lbl_historial)
        panel_hist.add_widget(scroll)

        panel_hist.add_widget(self._btn("Limpiar", "#B91C1C", self.limpiar_historial,
                                        size_hint_y=None, height=45))

        root.add_widget(panel_hist)

        self._cargar_historial()
        return root

    def _btn(self, texto, color_hex, accion, **kwargs):
        b = Button(
            text=texto,
            background_color=get_color_from_hex(color_hex),
            background_normal='',
            color=(1, 1, 1, 1),
            font_size='15sp',
            bold=True,
            **kwargs
        )
        b.bind(on_press=lambda x: accion())
        return b

    def escribir(self, valor):
        self.entrada.text += valor

    def limpiar(self):
        self.entrada.text = ""

    def borrar(self):
        self.entrada.text = self.entrada.text[:-1]

    def calcular(self):
        try:
            expr = self.entrada.text
            expr_eval = expr.replace("^", "**").replace("π", str(math.pi)).replace("pi", str(math.pi))
            resultado = eval(expr_eval, {"__builtins__": None}, {
                "sqrt": math.sqrt, "sin": math.sin, "cos": math.cos,
                "tan": math.tan, "log": math.log10, "pi": math.pi
            })
            self._guardar_historial(expr, resultado)
            self.entrada.text = str(resultado)
        except Exception as e:
            self.entrada.text = "Error"

    def _guardar_historial(self, expr, resultado):
        fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
        linea = f"[{fecha}] {expr} = {resultado}\n"
        self.historial_texto += linea
        self.lbl_historial.text = self.historial_texto
        try:
            with open(HISTORIAL_FILE, "a", encoding="utf-8") as f:
                f.write(linea)
        except Exception:
            pass

    def _cargar_historial(self):
        try:
            with open(HISTORIAL_FILE, "r", encoding="utf-8") as f:
                self.historial_texto = f.read()
                self.lbl_historial.text = self.historial_texto
        except FileNotFoundError:
            pass

    def limpiar_historial(self):
        self.historial_texto = ""
        self.lbl_historial.text = ""
        try:
            open(HISTORIAL_FILE, "w").close()
        except Exception:
            pass

if __name__ == "__main__":
    CalculadoraApp().run()
