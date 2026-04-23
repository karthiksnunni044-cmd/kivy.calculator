from kivy.app import App
from kivy.core.window import Window
import re

# Dark background
Window.clearcolor = (0, 0, 0, 1)


class CalculatorApp(App):
    kv_file = "Calculator.kv"

    def build(self):
        self.expression = ""
        return self.root

    def on_start(self):
        self.display = self.root.ids.display

    def on_button_press(self, instance):
        text = instance.text
        operators = {"+", "-", "×", "÷", "%","DEL"}

        if text == "AC":
            self.expression = ""
            self.display.text = "0"

        elif text == "=":
            try:
                expr = self.expression.replace("×", "*").replace("÷", "/")
                result = eval(expr)
                self.display.text = str(result)
                self.expression = str(result)
            except:
                self.display.text = "Error"
                self.expression = ""

        elif text == "+/-":
            self.toggle_sign()

        elif text == "%":
            # Use % as modulo operator so expressions like 3%4 work.
            if self.expression and self.expression[-1] not in operators and self.expression[-1] != ".":
                self.expression += text
                self.display.text = self.expression

        elif text in {"⌫", "DEL"}:
            if self.expression:
                self.expression = self.expression[:-1]
                self.display.text = self.expression if self.expression else "0"

        else:
            if text in operators:
                if not self.expression:
                    if text == "-":
                        self.expression = "-"
                    else:
                        return
                elif self.expression[-1] in operators or self.expression[-1] == ".":
                    return
                else:
                    self.expression += text
            else:
                self.expression += text
            self.display.text = self.expression

    def toggle_sign(self):
        if not self.expression:
            self.expression = "-"
            self.display.text = self.expression
            return

        # Toggle sign of the last numeric token in expression.
        match = re.search(r"(-?\d*\.?\d+)$", self.expression)
        if not match:
            return

        number = match.group(1)
        if number.startswith("-"):
            toggled = number[1:]
        else:
            toggled = "-" + number

        start, end = match.span(1)
        self.expression = self.expression[:start] + toggled + self.expression[end:]
        self.display.text = self.expression


if __name__ == "__main__":
    CalculatorApp().run()