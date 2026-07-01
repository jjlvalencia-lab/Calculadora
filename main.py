
import math
from datetime import datetime
from kivy.app import App
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.utils import get_color_from_hex

HISTORIAL_FILE="historial.txt"

class CalculadoraApp(App):
    def build(self):
        Window.clearcolor=get_color_from_hex("#111827")
        self.hist=""
        root=BoxLayout(orientation="vertical",padding=dp(10),spacing=dp(8))
        root.add_widget(Label(text="CALCULADORA",bold=True,font_size="26sp",
                              color=get_color_from_hex("#60A5FA"),size_hint_y=None,height=dp(40)))
        self.txt=TextInput(multiline=False,readonly=False,font_size="36sp",
                           halign="right",size_hint_y=None,height=dp(90),
                           background_color=get_color_from_hex("#030712"),
                           foreground_color=(1,1,1,1))
        root.add_widget(self.txt)
        top=GridLayout(cols=2,size_hint_y=None,height=dp(65),spacing=dp(8))
        top.add_widget(self.btn("C","#DC2626",self.clear))
        top.add_widget(self.btn("⌫","#F59E0B",self.back))
        root.add_widget(top)
        sci=GridLayout(cols=6,size_hint_y=None,height=dp(65),spacing=dp(5))
        for t,v in [("√","sqrt("),("sin","sin("),("cos","cos("),("tan","tan("),("log","log("),("π","pi")]:
            sci.add_widget(self.btn(t,"#2563EB",lambda x=v:self.add(x)))
        root.add_widget(sci)
        keys=[["7","8","9","/"],["4","5","6","*"],["1","2","3","-"],[".","0","^","+"],["(",")","%","="]]
        grid=GridLayout(cols=4,row_force_default=True,row_default_height=dp(78),spacing=dp(8))
        colors={"+":"#F97316","-":"#F97316","*":"#F97316","/":"#F97316","=":"#22C55E"}
        for r in keys:
            for k in r:
                if k=="=": grid.add_widget(self.btn(k,colors[k],self.calc))
                else: grid.add_widget(self.btn(k,colors.get(k,"#374151"),lambda x=k:self.add(x)))
        root.add_widget(grid)
        root.add_widget(Label(text="Historial",size_hint_y=None,height=dp(30),font_size="18sp"))
        sv=ScrollView(size_hint=(1,.3))
        self.lab=Label(size_hint_y=None,halign="left",valign="top",font_size="15sp")
        self.lab.bind(texture_size=lambda i,v:setattr(i,"height",v[1]))
        self.lab.bind(width=lambda i,v:setattr(i,"text_size",(v,None)))
        sv.add_widget(self.lab); root.add_widget(sv)
        root.add_widget(self.btn("Limpiar historial","#991B1B",self.clear_hist,size_hint_y=None,height=dp(55)))
        self.load()
        return root
    def btn(self,t,c,f,**kw):
        b=Button(text=t,background_normal="",background_color=get_color_from_hex(c),font_size="22sp",**kw)
        b.bind(on_press=lambda *_:f()); return b
    def add(self,v): self.txt.text+=v
    def clear(self): self.txt.text=""
    def back(self): self.txt.text=self.txt.text[:-1]
    def calc(self):
        try:
            exp=self.txt.text
            e=exp.replace("^","**").replace("π",str(math.pi)).replace("pi",str(math.pi))
            r=eval(e,{"__builtins__":None},{"sqrt":math.sqrt,"sin":math.sin,"cos":math.cos,"tan":math.tan,"log":math.log10})
            self.txt.text=str(r)
            line=f"[{datetime.now():%d/%m/%Y %H:%M}] {exp} = {r}\n"
            self.hist+=line; self.lab.text=self.hist
            open(HISTORIAL_FILE,"a",encoding="utf8").write(line)
        except: self.txt.text="Error"
    def load(self):
        try:
            self.hist=open(HISTORIAL_FILE,encoding="utf8").read(); self.lab.text=self.hist
        except: pass
    def clear_hist(self):
        self.hist=""; self.lab.text=""; open(HISTORIAL_FILE,"w").close()

if __name__=="__main__":
    CalculadoraApp().run()
