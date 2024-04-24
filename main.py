#Token türlerini tanımlıyoryuz.
INTEGER, PLUS, MINUS, MULTIPLY, DIVIDE, EOF, PRINT, VARIABLE, ASSIGN, SEMICOLON, INPUT = (
    'INTEGER', 'PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE', 'EOF', 'PRINT', 'VARIABLE', 'ASSIGN', 'SEMICOLON', 'INPUT'
)

#Token sınıfını oluşturuyoruz.
class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return f'Token({self.type}, {self.value})'

#Lexer sınıfını oluşturuyoruz.
class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    def error(self):
        raise Exception('Geçersiz karakter')
    def advance(self):
        self.pos += 1
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def variable(self):
        result = ''
        while self.current_char is not None and self.current_char.isalnum():
            result += self.current_char
            self.advance()
        return result

    def get_next_token(self):
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())

            if self.current_char.isalpha():
                return Token(VARIABLE, self.variable())

            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')

            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')

            if self.current_char == '*':
                self.advance()
                return Token(MULTIPLY, '*')

            if self.current_char == '/':
                self.advance()
                return Token(DIVIDE, '/')

            if self.current_char == '=':
                self.advance()
                return Token(ASSIGN, '=')

            if self.current_char == ';':
                self.advance()
                return Token(SEMICOLON, ';')

            if self.current_char == '(':
                self.advance()
                return Token(INPUT, '(')

            if self.current_char == ')':
                self.advance()
                return Token(INPUT, ')')

            self.error()

        return Token(EOF, None)

#Parser sınıfını oluşturuyoruz.
class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Sözdizimi hatası')

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def parse(self):
        result = self.expr()
        if self.current_token.type != EOF:
            self.error()
        return result

    def expr(self):
        result = self.term()

        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
                result += self.term()
            elif token.type == MINUS:
                self.eat(MINUS)
                result -= self.term()

        return result

    def term(self):
        result = self.factor()

        while self.current_token.type in (MULTIPLY, DIVIDE):
            token = self.current_token
            if token.type == MULTIPLY:
                self.eat(MULTIPLY)
                result *= self.factor()
            elif token.type == DIVIDE:
                self.eat(DIVIDE)
                result /= self.factor()

        return result

    def factor(self):
        token = self.current_token

        if token.type == INTEGER:
            self.eat(INTEGER)
            return token.value
        elif token.type == VARIABLE:
            self.eat(VARIABLE)
            return token.value
        elif token.type == INPUT:
            if token.value == '(':
                self.eat(INPUT)
                variable = self.current_token.value
                self.eat(VARIABLE)
                if self.current_token.type == INPUT:
                    self.eat(INPUT)
                return int(input(f"{variable}: "))
        elif token.type == '(':
            self.eat('(')
            result = self.expr()
            self.eat(')')
            return result

        self.error()

#Ana programı oluşturuyoruz.
def main():
    while True:
        try:
            text = input('Değer giriniz: ')
        except EOFError:
            break
        if not text:
            continue
        lexer = Lexer(text)
        parser = Parser(lexer)
        result = parser.parse()
        print(result)
if __name__ == '__main__':
    main()