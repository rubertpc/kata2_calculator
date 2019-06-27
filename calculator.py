from tkinter import *
from tkinter import ttk

_heightBtn = 50
_widthBtn = 68

class CalcDisplay(ttk.Frame):
    _value = '0'
    _espositivo = True

    def __init__(self, parent, **kwargs):
        self._value ='0'
        ttk.Frame.__init__(self, parent, height=_heightBtn, width=_widthBtn*4)

        self.pack_propagate(0)

        s = ttk.Style()
        s.theme_use('alt')
        s.configure('my.TLabel', font="Helvetica 42")

        self.lblDisplay = ttk.Label(self, text=self._value, style='my.TLabel', anchor=E, foreground="#ffffff", background="#000000")
        self.lblDisplay.pack(fill=BOTH, expand=True)

    def addDigit(self, digito):
        if self._value[0] != "-" and len(self._value) >= 10 or len(self._value) >= 11:
            return

        '''
        if self._value[0]:
            longmax = 11
        else:
            longmax = 10

        if len(self._value) >= longmax:
            return

        if len(self._value) == 10:
            return
        '''

        if self._value == '0':
            self._value = digito
        else:
            self._value += digito
        
        self.pintar()
        #self.lblDisplay.configure(text=self._value)

    
    def pintar(self):
        #self._value = value
        self.lblDisplay.configure(text=self._value)

    
    def reset(self):
        self._value ="0"
        self._espositivo = True
        self.pintar()
    

    def signo(self):
        if self._value == '0':
            return

        if self._espositivo:
            self._value = '-'+self._value
            #self._espositivo = False
        else:
            self._value = self._value[1:]
            #self._espositivo = True
        self._espositivo = not self._espositivo
        self.pintar()
        


class CalcButton(ttk.Frame):
    def __init__(self, parent, **kwargs):
        #ttk.Frame(self, parent, **kwargs)

        '''
        if 'bw' in kwargs:
            bw = kwargs['bw']
        else:
            bw = 1
        '''

        #Esto hace lo mismo que el if - else de arriba
        bw = kwargs['bw'] if 'bw' in kwargs else 1

        ttk.Frame.__init__(self, parent, height=_heightBtn, width=_widthBtn * bw)
        self.pack_propagate(0)

        self.button = ttk.Button(self, text=kwargs['text'], command=kwargs['command'])
        self.button.pack(fill=BOTH, expand=True)

        

class Calculator(ttk.Frame):
    _op1 = None
    _op2 = None
    _operador = None
    _swBorrado = True

    def __init__(self, parent, **kwargs):
        ttk.Frame.__init__(self, parent, height=kwargs['height'], width=kwargs['width'])
        self.display = CalcDisplay(self)
        self.display.grid(column=0, row=0, columnspan=4)
        #CalcButton(self, text='C', command=lambda: self.display.addDigit('1')).grid(column=0, row=1)
        #CalcButton(self, text='+/-', command=lambda: self.display.addDigit('1')).grid(column=1, row=1)
        #CalcButton(self, text='%', command=lambda: self.display.addDigit('1')).grid(column=2, row=1)
        CalcButton(self, text='C', command=self.reset).grid(column=0, row=1)
        CalcButton(self, text='+/-', command=self.display.signo).grid(column=1, row=1)
        CalcButton(self, text='%', command=None).grid(column=2, row=1)
        CalcButton(self, text='÷', command=lambda: self.opera('÷')).grid(column=3, row=1)
        CalcButton(self, text='7', command=lambda: self.addDigit('7')).grid(column=0, row=2)
        CalcButton(self, text='8', command=lambda: self.addDigit('8')).grid(column=1, row=2)
        CalcButton(self, text='9', command=lambda: self.addDigit('9')).grid(column=2, row=2)
        CalcButton(self, text='x', command=lambda: self.opera('*')).grid(column=3, row=2)
        CalcButton(self, text='4', command=lambda: self.addDigit('4')).grid(column=0, row=3)
        CalcButton(self, text='5', command=lambda: self.addDigit('5')).grid(column=1, row=3)
        CalcButton(self, text='6', command=lambda: self.addDigit('6')).grid(column=2, row=3)
        CalcButton(self, text='-', command=lambda: self.opera('-')).grid(column=3, row=3)
        CalcButton(self, text='1', command=lambda: self.addDigit('1')).grid(column=0, row=4)
        CalcButton(self, text='2', command=lambda: self.addDigit('2')).grid(column=1, row=4)
        CalcButton(self, text='3', command=lambda: self.addDigit('3')).grid(column=2, row=4)
        CalcButton(self, text='+', command=lambda: self.opera('+')).grid(column=3, row=4)
        CalcButton(self, text='0', command=lambda: self.addDigit('0'), bw=2).grid(column=0, row=5, columnspan=2)
        CalcButton(self, text=".", command=None).grid(column=2, row=5)
        CalcButton(self, text="=", command=lambda: self.opera('=')).grid(column=3, row=5)

    def addDigit(self, digito):
        if self._swBorrado:
            self.display.reset()
            self._swBorrado = False

        self.display.addDigit(digito)


    
    def reset(self):
        self._op1 = None
        self._op2 = None
        self._operador = None
        self.display.reset()

 
    #def enviar(self, value):
    #    self.display.pintar(value)

    def opera(self, operador):
        if self._op1 is None:
            self._op1 = float(self.display._value)
            self._operador = operador
            self._swBorrado = True    
        else:
            self._op2 = float(self.display._value)
            if self._operador == '+':
                resultado = self._op1 + self._op2
            elif self._operador == '-':
                resultado = self._op1 - self._op2
            elif self._operador == 'x':
                resultado = self._op1 * self._op2
            elif self._operador == '÷':
                resultado = self._op1 / self._op2
            else:
                print("operador incorrecto")

            self._op1 = resultado
            self._operador = operador
            resultado = str(resultado)
            self.display._value = resultado
            self.display.pintar()

            self._op2 = None
            self._swBorrado = True


class MainApp(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title("Calculator")
        self.geometry("{}x{}".format(_widthBtn*4, _heightBtn*6))

        self.calculator = Calculator(self, height=_heightBtn*6, width=_widthBtn*4)
        self.calculator.place(x=0, y=0)

    def start(self):
        self.mainloop()

if __name__ == '__main__':
    app = MainApp()
    app.start()
