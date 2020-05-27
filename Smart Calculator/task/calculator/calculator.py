# write your code here


class Calculator():

    VALID_COMMANDS=['exit','help']
    CHAR_LETTERS = 'abcdefghijklmnopqrstuvwxyz'
    CHAR_NUMBERS = '0123456789'
    CHAR_OPERATORS = '=+-'
    CHAR_SEPARATORS = ' ' + CHAR_OPERATORS
    STATUS_VALID = 'VALID'
    STATUS_UNKNOWN_TOKEN = 'UNKNOWN_TOKEN'
    STATUS_INVALID_TOKEN = 'INVALID_TOKEN'
    STATUS_INVALID_EXPR = 'INVALID_EXPR'
    STATUS_INVALID_IDENT = 'INVALID_IDENT'
    STATUS_INVALID_ASSIGN = 'INVALID_ASSIGN'
    TYPE_NUMBER = 'NUMBER'
    TYPE_TOKEN = 'TOKEN'
    TYPE_OPERATOR = 'OPERATOR'

    def show_help(cls):
        print("""The program is able to perform some calculations
It can calculates sums and differences of numbers""")

    def __init__(self):
        self.result = None
        self.local_vars = {}

    def get_inputs(self):
        while True:
            in_text = input()
            if len(in_text) > 0:
                break
        return in_text

    def start(self):
        command = ''
        while command != 'exit':
            input_line = self.get_inputs()
            if input_line[0] == '/':
                command = input_line[1:]
                self.exec_command(command)
            elif '=' in input_line:
                self.result = self.parse_assignment(input_line)
            elif input_line:
                self.result = self.eval_expression(input_line)

            if self.result == Calculator.STATUS_INVALID_ASSIGN:
                print('Invalid assignment')
            elif self.result == Calculator.STATUS_UNKNOWN_TOKEN:
                print('Unknown variable')
            elif self.result == Calculator.STATUS_INVALID_TOKEN:
                print('Invalid identifier')
            elif self.result == Calculator.STATUS_INVALID_IDENT:
                print('Invalid identifier')
            elif self.result is None:
                pass
            else:
                print(self.result)
        print('Bye!')

    def exec_command(self, command):
        if command not in Calculator.VALID_COMMANDS:
            print("Unknown command")
        elif command == 'exit':
            self.result = None
        elif command == 'help':
            Calculator.show_help()

    def parse_assignment(self, input):
        sides = input.split('=')
        token_id = sides[0].strip()
        if len(sides) != 2:
            return Calculator.STATUS_INVALID_ASSIGN
        if not self.valid_token(token_id):
            return Calculator.STATUS_INVALID_IDENT
        key = token_id
        value = self.eval_expression(sides[1])
        if value == Calculator.STATUS_UNKNOWN_TOKEN:
            print('Unknown variable')
        elif value == Calculator.STATUS_INVALID_TOKEN:
            return Calculator.STATUS_INVALID_ASSIGN
        else:
            self.local_vars[key] = value


    def parse_expression(self, input):
        i = 0
        items = []
        status = Calculator.STATUS_VALID
        while i < len(input):
            char = input[i]
            if char == ' ':
                i += 1
            elif char in Calculator.CHAR_OPERATORS:
                items.append((Calculator.TYPE_OPERATOR, char))
                i += 1
            else:
                str_item = ''
                while i < len(input) and input[i] not in Calculator.CHAR_SEPARATORS:
                    str_item += input[i]
                    i += 1
                if str_item.isnumeric():
                    items.append((Calculator.TYPE_NUMBER, int(str_item)))
                elif self.valid_token(str_item):
                    if str_item not in self.local_vars:
                        items.append((Calculator.TYPE_TOKEN, str_item))
                        status = Calculator.STATUS_UNKNOWN_TOKEN
                    else:
                        items.append((Calculator.TYPE_TOKEN, str_item))
                else:
                    items.append((Calculator.TYPE_TOKEN, str_item))
                    status = Calculator.STATUS_INVALID_TOKEN

        # print({'status': status, 'items': items})
        return {'status': status, 'items': items}

    def eval_expression(self, input):

        parsed_expression = self.parse_expression(input)
        if parsed_expression['status'] != 'VALID':
            return parsed_expression['status']

        result = 0
        state = 'START'
        for itemtype, item in parsed_expression['items']:
            state, result = self.process_item(item, itemtype, state, result)
            if state == 'ERROR':
                break

        if state == 'RESULT':
            return result
        else:
            return None


    def process_item(self, item, itemtype, state, result):
        if itemtype == Calculator.TYPE_NUMBER:
            if state == 'START':
                result = item
                state = 'RESULT'
            elif state == 'RESULT':
                state = 'ERROR'
            elif state == 'ADD':
                result += item
                state = 'RESULT'
            elif state == 'SUB':
                result -= item
                state = 'RESULT'
        elif itemtype == Calculator.TYPE_OPERATOR:
            if item == '+':
                if state in ['START', 'RESULT', 'ADD']:
                    state = 'ADD'
                elif state in ['SUB']:
                    state = 'SUB'
            elif item == '-':
                if state in ['START', 'RESULT', 'ADD']:
                    state = 'SUB'
                elif state in ['SUB']:
                    state = 'ADD'
            else:
                state = 'ERROR'
        elif itemtype == Calculator.TYPE_TOKEN:
            if item in self.local_vars:
                item = self.local_vars[item]
                state, result = self.process_item(item, Calculator.TYPE_NUMBER, state, result)



        return state, result

    def valid_token(self, token):
        for char in token.lstrip().lower():
            if char not in Calculator.CHAR_LETTERS:
                return False
        return True


calc = Calculator()
calc.start()
