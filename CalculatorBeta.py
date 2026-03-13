# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 07:25:58 2026

@author: Matheus
"""
from os import path

from PySide6.QtCore import Qt, QRegularExpression
from PySide6.QtGui import QIcon, QRegularExpressionValidator
from PySide6.QtWidgets import(
    QApplication, QMainWindow, QGridLayout, QVBoxLayout, QTabWidget,
    QPushButton, QLineEdit, QWidget, QLabel, QHBoxLayout, QListWidget
    )


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Visual/UI
        
        current_directory = path.dirname(path.realpath(__file__))
        windowIcon = path.join(current_directory,
                                "Files/icons-shadowless-2x/Calculator.png")
        
        self.isDecimal = False # Inserção de valores decimais
        self.currentValue = 0 # Valor (inteiro ou float) sendo inserido (atual)
        self.lastValue = None # Último valor registrado na memória
        self.currentOperation = "" # Operação aritimética atual
        self.lastDigit = 0 # Último dígito inserido
        self.integers = None # Parte inteira do valor atual
        self.decimals = None # Parte decimal do valor atual
        
        self.setWindowTitle("Calculator")
        self.setWindowIcon(QIcon(windowIcon))
        
        self.output = QLabel("0") # Resultado da última operação
        self.operation = QLabel("QUACK!") # Cálculo em andamento
        self.display = QHBoxLayout() # Container do cálculo e resultado
        self.layout = QVBoxLayout() # Container geral
        self.textInput = QLineEdit() # Entrada de valores
        self.buttonGrid = QGridLayout() # Grade de botões
        self.mainWidget = QWidget() # Widget de exibição principal
        
        regex = QRegularExpression("\\d*") # Apenas números
        validator = QRegularExpressionValidator(regex, self.textInput)
        self.textInput.setValidator(validator)
        
        self.textInput.setText("0")
        self.textInput.setReadOnly(True)

        self.textInput.setMinimumHeight(50)
        
        self.button0 = QPushButton("0")
        self.button1 = QPushButton("1")
        self.button2 = QPushButton("2")
        self.button3 = QPushButton("3")
        self.button4 = QPushButton("4")
        self.button5 = QPushButton("5")
        self.button6 = QPushButton("6")
        self.button7 = QPushButton("7")
        self.button8 = QPushButton("8")
        self.button9 = QPushButton("9")
        self.equalButton = QPushButton("=")
        self.plusButton = QPushButton("+")
        self.minusButton = QPushButton("-")
        self.multiplyButton = QPushButton("x")
        self.divideButton = QPushButton("/")
        self.decimalButton = QPushButton(",")
        self.clearButton = QPushButton("C")
        self.rootButton = QPushButton("y√x")
        self.raiseButton = QPushButton("x^y")
        self.deleteButton = QPushButton("\u2190") # Símbolo de radiciação

        self.buttonGrid.addWidget(self.clearButton, 0, 0)
        self.buttonGrid.addWidget(self.rootButton, 0, 1)
        self.buttonGrid.addWidget(self.raiseButton, 0, 2)
        self.buttonGrid.addWidget(self.deleteButton, 0, 3)
        self.buttonGrid.addWidget(self.button7, 1, 0)
        self.buttonGrid.addWidget(self.button8, 1, 1)
        self.buttonGrid.addWidget(self.button9, 1, 2)
        self.buttonGrid.addWidget(self.divideButton, 1, 3)
        self.buttonGrid.addWidget(self.button4, 2, 0)
        self.buttonGrid.addWidget(self.button5, 2, 1)
        self.buttonGrid.addWidget(self.button6, 2, 2)
        self.buttonGrid.addWidget(self.multiplyButton, 2, 3)
        self.buttonGrid.addWidget(self.button1, 3, 0)
        self.buttonGrid.addWidget(self.button2, 3, 1)
        self.buttonGrid.addWidget(self.button3, 3, 2)
        self.buttonGrid.addWidget(self.minusButton, 3, 3)
        self.buttonGrid.addWidget(self.button0, 4, 0)
        self.buttonGrid.addWidget(self.decimalButton, 4, 1)
        self.buttonGrid.addWidget(self.equalButton, 4, 2)
        self.buttonGrid.addWidget(self.plusButton, 4, 3)
        
        self.button0.clicked.connect(lambda clicked: self.increase(0))
        self.button1.clicked.connect(lambda clicked: self.increase(1))
        self.button2.clicked.connect(lambda clicked: self.increase(2))
        self.button3.clicked.connect(lambda clicked: self.increase(3))
        self.button4.clicked.connect(lambda clicked: self.increase(4))
        self.button5.clicked.connect(lambda clicked: self.increase(5))
        self.button6.clicked.connect(lambda clicked: self.increase(6))
        self.button7.clicked.connect(lambda clicked: self.increase(7))
        self.button8.clicked.connect(lambda clicked: self.increase(8))
        self.button9.clicked.connect(lambda clicked: self.increase(9))
        self.plusButton.clicked.connect(self.add)
        self.minusButton.clicked.connect(self.subtract)
        self.multiplyButton.clicked.connect(self.multiply)
        self.divideButton.clicked.connect(self.divide)
        self.decimalButton.clicked.connect(self.enable_decimal)
        self.equalButton.clicked.connect(
            lambda operation: self.calculate(self.currentOperation)
            )
        self.clearButton.clicked.connect(self.clear_all)
        self.rootButton.clicked.connect(self.rootOf)
        self.raiseButton.clicked.connect(self.powerOf)
        self.deleteButton.clicked.connect(self.delete_last_digit)
        
        self.display.addWidget(self.output)
        self.display.addWidget(self.operation)
        self.layout.addLayout(self.display)
        self.layout.addWidget(self.textInput)
        self.layout.addLayout(self.buttonGrid)
        self.mainWidget.setLayout(self.layout)
        
        self.setCentralWidget(self.mainWidget)
    
    # Lógica
    
    def increase(self, value): # Inserção de valores
        """Insere novos dígitos no valor atual"""
        self.lastDigit = value # Passa o valor mais recente para a variável
        
        # Caso a operação seja com números inteiros
        if not self.isDecimal:
            if self.currentValue == 0: # Calculadora iniciada/memória limpa
                self.currentValue = self.lastDigit
            else:
                stringValue = str(self.currentValue) + str(self.lastDigit)
                self.currentValue = int(stringValue)
            
            # Armazena uma string com a parte inteira do valor
            self.integers = str(self.currentValue)
        # Operação com decimais
        else:
            if self.decimals is None: # Vírgula/Ponto recém-pressionados
                self.decimals = str(value)
            else:
                # Armazena a parte decimal numa variável
                stringValue = str(self.decimals) + str(value)
                self.decimals = stringValue
            
            # Converte as strings inteira e decimal num único float com o "."
            self.currentValue = float(self.integers + "." + self.decimals)
        
        print(f"Current: {self.currentValue}, Last: {self.lastValue}")
        print(f"Last digit: {self.lastDigit}")
        self.textInput.setText(str(self.currentValue))
    
    def add(self):
        """Realiza a adição do último valor armazenado com valor atual sendo inserido"""
        # Verifica qual tipo de operação está em andamento
        if self.currentOperation == "Add" or self.currentOperation == "":
            print(f"Current: {self.currentValue}, Last: {self.lastValue}")
            
            # Se a operação em andamento for esta:
            if self.lastValue == None: # Calculadora iniciada/memória limpa
                # Registra o valor atual como último valor inserido
                self.lastValue = self.currentValue
                self.operation.setText(f"{self.lastValue} + 0")
            else:
                # Exibe o cálculo atual ANTES de registrar o último valor
                self.operation.setText(f"{self.lastValue} + {self.currentValue}")
                # Execução do cálculo de soma e registro do último valor
                self.lastValue += self.currentValue
            
            # Exibe o resultado do cálculo na área de exibição e de inserção
            self.output.setText(str(self.lastValue))
            self.textInput.setText(str(self.currentValue))
        # Caso esta não seja a operação atual
        else:
            # Chama a operação em andamento antes de começar esta
            self.calculate(self.currentOperation)
        
        # Estabelece esta operação como em andamento
        self.call_next_operation("Add")
    
    def subtract(self):
        """Realiza a subtração do último valor armazenado com valor atual sendo inserido"""
        # Verifica qual tipo de operação está em andamento
        if self.currentOperation == "Subtract" or self.currentOperation == "":
            print(f"Current: {self.currentValue}, Last: {self.lastValue}")
            
            if self.lastValue == None: # Calculadora iniciada/memória limpa
                # Registra o valor atual como último valor inserido
                self.lastValue = self.currentValue
                self.operation.setText(f"{self.lastValue} - 0")
            else:
                # Exibe o cálculo atual ANTES de resgitrar o último valor
                self.operation.setText(f"{self.lastValue} - {self.currentValue}")
                # Execução do cálculo de subtração e registro do último valor
                self.lastValue -= self.currentValue
            
            # Exibe o resultado do cálculo na área de exibição e de inserção
            self.output.setText(str(self.lastValue))
            self.textInput.setText(str(self.currentValue))
        else:
            self.calculate(self.currentOperation)
        
        # Estabelece esta operação como em andamento
        self.call_next_operation("Subtract")
        
    def multiply(self):
        if self.currentOperation == "Multiply" or self.currentOperation == "":
            print(f"Current: {self.currentValue}, Last: {self.lastValue}")
            
            if self.lastValue == None:
                self.lastValue = self.currentValue
                self.operation.setText(f"{self.lastValue} x 0")
            else:
                self.operation.setText(f"{self.lastValue} x {self.currentValue}")
                self.lastValue *= self.currentValue
            
            print(self.lastValue)
            self.output.setText(str(self.lastValue))
            self.textInput.setText(str(self.currentValue))
        else:
            self.calculate(self.currentOperation)
        
        self.call_next_operation("Multiply")
        
    def divide(self):
        if self.currentOperation == "Divide" or  self.currentOperation == "":
            print(f"Current: {self.currentValue}, Last: {self.lastValue}")
            
            if self.lastValue == None:
                self.lastValue = self.currentValue
                self.operation.setText(f"{self.lastValue} / 0")
            elif self.currentValue != 0:
                self.operation.setText(f"{self.lastValue} / {self.currentValue}")
                self.lastValue /= self.currentValue
            else:
                print("CYKA BLAT!!!!")
                self.operation.setText("CYKA BLAT!!!!")
            
            print(self.lastValue)
            self.output.setText(str(self.lastValue))
            self.textInput.setText(str(self.currentValue))
        else:
            self.calculate(self.currentOperation)
        
        self.call_next_operation("Divide")
    
    def calculate(self, operation):
        """Calcula o valor resultante da operação em andamento.
        Recebe como parâmetro o nome (string) da operação atual."""
        
        match operation:
            case "Add":
                self.add()
            case "Subtract":
                self.subtract()
            case "Multiply":
                self.multiply()
            case "Divide":
                self.divide()
            case "Root":
                self.rootOf()
            case "Power":
                self.powerOf()
            case "":
                return
        
        # Exibe os valores e limpa o valor atual, bem como desabilita inserção de decimais
        self.textInput.setText(str(self.lastValue))
        self.currentValue = 0
        self.isDecimal = False
    
    def enable_decimal(self):
        """Habilita a inserção de dígitos decimais"""
        if not self.isDecimal:
            self.isDecimal = True # Habilita inserção de dígitos decimais
            # Armazena a parte inteira do valor atual como string
            self.integers = str(self.currentValue)
    
    def clear_all(self):
        # Atribui valores de inicialização para todas as variáveis (limpeza)
        self.isDecimal = False
        self.currentValue = 0
        self.lastValue = None
        self.currentOperation = ""
        self.decimals= None
        self.lastDigit = 0
        self.integers = None
        
        # Limpa as áreas de exibição e inserção
        self.textInput.setText("0")
        self.output.setText("0")
        self.operation.setText("0")

    def rootOf(self):
        if self.currentOperation == "Root" or  self.currentOperation == "":
            print(f"Current: {self.currentValue}, Last: {self.lastValue}")
            
            if self.lastValue == None:
                self.lastValue = self.currentValue
                self.operation.setText(f" √ {self.lastValue}")
            elif self.currentValue != 0:
                self.operation.setText(f"{self.currentValue} √ {self.lastValue}")
                self.lastValue = self.lastValue ** (1 / self.currentValue)
            else:
                print("CYKA BLYAT!!!!")
                self.operation.setText("CYKA BLYAT!!!!")
            
            print(self.lastValue)
            self.output.setText(str(self.lastValue))
            self.textInput.setText(str(self.currentValue))
        else:
            self.calculate(self.currentOperation)
        
        self.call_next_operation("Root")
    
    def powerOf(self):
        if self.currentOperation == "Power" or self.currentOperation == "":
            print(f"Current: {self.currentValue}, Last: {self.lastValue}")
            
            if self.lastValue == None:
                self.lastValue = self.currentValue
                self.operation.setText(f"{self.lastValue} ^ 0")
            else:
                self.operation.setText(f"{self.lastValue} ^ {self.currentValue}")
                self.lastValue = self.lastValue ** self.currentValue
            
            print(self.lastValue)
            self.output.setText(str(self.lastValue))
            self.textInput.setText(str(self.currentValue))
        else:
            self.calculate(self.currentOperation)
        
        self.call_next_operation("Power")
    
    def delete_last_digit(self):
        """Apaga o último dígito inserido. Se valores decimais estiverem
        habilitados, pode apagar toda a parte decimal e reabilitar a
        inserção de valores inteiros."""
        stringValue = "" # String de referência
        newStringValue = "" # String para atribuir às variáveis da classe
        
        # Caso a operação seja com números inteiros
        if not self.isDecimal:
            stringValue = self.integers # Atribui valor da parte inteira
            if len(stringValue) >= 2: # Se tiver um dois ou mais dígitos
                # Retira o último dígito da string de referência
                # e guarda na de atribuição de valores
                newStringValue = stringValue[:-1]
            else:
                # Se a string de referência tiver apenas um dígito
                newStringValue = "0" # Passa a valer zero
            
            # Atribuição de valor em integers
            self.integers = newStringValue
            # Converte em int para o valor atual
            self.currentValue = int(self.integers)
        # No caso de operação com valores inteiros
        else:
            stringValue = self.decimals # Atribui valor da parte decimal
            if len(self.decimals) >= 2: # Se tiver 2 ou mais dígitos
                # Retira o último dígito da string de referência
                # e guarda na de atribuição de valores
                newStringValue = stringValue[:-1]
            else:
                # Se a string de referência tiver apenas um dígito
                newStringValue = "0" # Passa a valer zero
            
            # Atribução do valor para decimals
            self.decimals = newStringValue
            
            # Verifica se a parte decimal é igual a zero
            if self.decimals == "0":
                # Se for, considera só a parte inteira e desabilita decimais
                self.currentValue = int(self.integers)
                self.isDecimal = False
            else:
                # Se não for, registra novo valor com dígito a menos
                self.currentValue = float(self.integers + "." + self.decimals)
        
        self.textInput.setText(str(self.currentValue))
    
    def call_next_operation(self, operation):
        """Recebe nome de operação, estabelece como atual e limpa variáveis
        usadas para cálculos."""
        self.isDecimal = False
        self.currentValue = 0
        self.currentOperation = operation
        self.decimals = None
        self.lastDigit = 0
        self.integers = None
        pass

    def keyPressEvent(self, event):
        """Captura teclas pressionadas e executa funções de acordo."""
        match event.key():
            case Qt.Key_0:
                self.increase(0)
            case Qt.Key_1:
                self.increase(1)
            case Qt.Key_2:
                self.increase(2)
            case Qt.Key_3:
                self.increase(3)
            case Qt.Key_4:
                self.increase(4)
            case Qt.Key_5:
                self.increase(5)
            case Qt.Key_6:
                self.increase(6)
            case Qt.Key_7:
                self.increase(7)
            case Qt.Key_8:
                self.increase(8)
            case Qt.Key_9:
                self.increase(9)
            case Qt.Key_Plus:
                self.add()
            case Qt.Key_Minus:
                self.subtract()
            case Qt.Key_Asterisk:
                self.multiply()
            case Qt.Key_Slash:
                self.subtract()
            case Qt.Key_P:
                self.powerOf()
            case Qt.Key_R:
                self.rootOf()
            case Qt.Key_Return:
                self.calculate(self.currentOperation)
            case Qt.Key_Backspace:
                self.delete_last_digit()
            case Qt.Key_Comma | Qt.Key_Period:
                self.enable_decimal()
            case Qt.Key_Escape:
                self.clear_all()
        pass


def run_app():
    # 1. Recupera a instância existente ou cria uma nova
    app = QApplication.instance()
    if not app:
        app = QApplication([])

    window = MainWindow()
    window.show()

    # 2. Garante que o app feche quando a janela for fechada
    app.setQuitOnLastWindowClosed(True)
    
    # 3. Executa e limpa
    app.exec()
    
    # 4. Força a deleção para liberar o Singleton no fundo
    del window
    app.quit() 

if __name__ == "__main__":
    run_app()