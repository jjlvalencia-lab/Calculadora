from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.button import Button
from kivymd.uix.label import MDLabel
from kivy.uix.gridlayout import GridLayout
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Rectangle

class Principal(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.ecuacion = ''

        with self.canvas:
            Color(0.6, 0.6, 0.6, 0.9)
            self.rect = Rectangle(size = (self.size[0], 0.15*self.size[1]), pos = (0, 0.85*self.height))

        self.muestra = MDLabel(text = self.ecuacion, bold = True, halign = 'center', pos_hint = {'center_y': 0.925})
        self.add_widget(self.muestra)

        self.botones = GridLayout(cols = 4, size_hint = (1, 0.7), spacing = 5, padding = 10, pos_hint = {'center_x': 0.5, 'top': 0.82})

        self.botones.add_widget(Button(text = '7', bold = True, size_hint = (0.25, 0.18), background_color = 'lightblue', on_press = lambda x: self.presionar('7')))
        self.botones.add_widget(Button(text = '8', bold = True, size_hint = (0.25, 0.18), background_color = 'lightblue', on_press = lambda x: self.presionar('8')))
        self.botones.add_widget(Button(text = '9', bold = True, size_hint = (0.25, 0.18), background_color = 'lightblue', on_press = lambda x: self.presionar('9')))
        self.botones.add_widget(Button(text = '+', bold = True, size_hint = (0.25, 0.18), background_color = 'lightblue', on_press = lambda x: self.presionar('+')))
        self.botones.add_widget(Button(text = '4', bold = True, size_hint = (0.25, 0.18), background_color = 'lightblue', on_press = lambda x: self.presionar('4')))
        self.botones.add_widget(Button(text = '5', bold = True, size_hint = (0.25, 0.18), background_color = 'lightblue', on_press = lambda x: self.presionar('5')))
        self.botones.add_widget(Button(text = '6', bold = True, size_hint = (0.25, 0.18), background_color = 'lightblue', on_press = lambda x: self.presionar('6')))
        self.botones.add_widget(Button(text = '-', bold = True, size_hint = (0.25, 0.18), background_color = 'lightblue', on_press = lambda x: self.presionar('-')))
        self.botones.add_widget(Button(text = '1', bold = True, size_hint = (0.25, 0.18), background_color = 'lightblue', on_press = lambda x: self.presionar('1')))
        self.botones.add_widget(Button(text = '2', bold = True, size_hint = (0.25, 0.18), background_color = 'lightblue', on_press = lambda x: self.presionar('2')))
        self.botones.add_widget(Button(text = '3', bold = True, size_hint = (0.25, 0.18), background_color = 'lightblue', on_press = lambda x: self.presionar('3')))
        self.botones.add_widget(Button(text = '*', bold = True, size_hint = (0.25, 0.18), background_color = 'lightblue', on_press = lambda x: self.presionar('*')))
        self.botones.add_widget(Button(text = '.', bold = True, size_hint = (0.25, 0.18), background_color = 'lightblue', on_press = lambda x: self.presionar('.')))
        self.botones.add_widget(Button(text = '0', bold = True, size_hint = (0.25, 0.18), background_color = 'lightblue', on_press = lambda x: self.presionar('0')))
        self.botones.add_widget(Button(text = '=', bold = True, size_hint = (0.25, 0.18), background_color = 'lightblue', on_press = lambda x: self.resultado()))
        self.botones.add_widget(Button(text = '/', bold = True, size_hint = (0.25, 0.18), background_color = 'lightblue', on_press = lambda x: self.presionar('/')))


        self.add_widget(self.botones)

        self.add_widget(Button(text = 'Borrar', bold = True, size_hint = (0.25, 0.12), background_color = 'red', on_press = lambda x: self.borrar(),
        pos_hint = {'center_x': 0.5}))

    def on_size(self, *args):
        self.rect.size = (self.size[0], 0.15*self.size[1])
        self.rect.pos = (0, 0.85*self.height)

    def presionar(self, valor):
        self.ecuacion = self.ecuacion + valor
        self.muestra.text = self.ecuacion

    def resultado(self):
        try:
            self.ecuacion = str(eval(self.ecuacion))
            self.muestra.text = self.ecuacion

        except:
            self.ecuacion = ''
            self.muestra.text = 'Error'

    def borrar(self):
        self.ecuacion = ''
        self.muestra.text = self.ecuacion

class Miapp(MDApp):
    def build(self):

        SC = ScreenManager()
        SC.add_widget(Principal(name = 'principal'))
        self.theme_cls.theme_style = "Dark"

        return SC

Miapp().run()