# write your code here


class Calculator:
    VALID_COMMANDS = ['exit', 'help']
    CHAR_LETTERS = 'abcdefghijklmnopqrstuvwxyz'  # noqa
    CHAR_NUMBERS = '0123456789'
    CHAR_OPERATORS = '=+-'
    CHAR_SEPARATORS = ' ' + CHAR_OPERATORS
    STATUS_VALID = 'VALID'
    STATUS_UNKNOWN_TOKEN = 'UNKNOWN_TOKEN'
    STATUS_INVALID_TOKEN = 'INVALID_TOKEN'
    STATUS_INVALID_EXPR = 'INVALID_EXPR'
    STATUS_INVALID_IDENT = 'INVALID_IDENT'
    STATUS_INVALID_ASSIGN = 'INVALID_ASSIGN'
    STATUS_UNKNOWN_CMD = 'UNKNOWN_CMD'
    TYPE_NUMBER = 'NUMBER'
    TYPE_TOKEN = 'TOKEN'
    TYPE_OPERATOR = 'OPERATOR'

    def show_help(self):
        print(f"The {self.__class__.__name__} is able to perform some calculations\n" +
              "It can calculates sums and differences of numbers")

    def __init__(self):
        self.result = None
        self.local_vars = {}

    def get_inputs(self): # noqa
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
                self.result = self.exec_command(command)
            elif '=' in input_line:
                self.result = self.parse_assignment(input_line)
            elif input_line:
                self.result = self.eval_expression(input_line)

            self.show_output()
        print('Bye!')

    def show_output(self):
        if self.result == self.STATUS_INVALID_ASSIGN:
            print('Invalid assignment')
        elif self.result == self.STATUS_UNKNOWN_TOKEN:
            print('Unknown variable')
        elif self.result == self.STATUS_INVALID_TOKEN:
            print('Invalid identifier')
        elif self.result == self.STATUS_INVALID_IDENT:
            print('Invalid identifier')
        elif self.result == self.STATUS_UNKNOWN_CMD:
            print("Unknown command")
        elif self.result is None:
            pass
        else:
            print(self.result)

    def exec_command(self, command):
        result = None
        if command not in self.VALID_COMMANDS:
            result = self.STATUS_UNKNOWN_CMD
        elif command == 'exit':
            pass
        elif command == 'help':
            self.show_help()
        return result

    def parse_assignment(self, input_line):
        sides = input_line.split('=')
        token_id = sides[0].strip()
        if len(sides) != 2:
            return self.STATUS_INVALID_ASSIGN
        if not self.valid_token(token_id):
            return self.STATUS_INVALID_IDENT
        key = token_id
        value = self.eval_expression(sides[1])
        if value == self.STATUS_UNKNOWN_TOKEN:
            print('Unknown variable')
        elif value == self.STATUS_INVALID_TOKEN:
            return self.STATUS_INVALID_ASSIGN
        else:
            self.local_vars[key] = value

    def parse_expression(self, input_line):
        i = 0
        items = []
        status = self.STATUS_VALID
        while i < len(input_line):
            char = input_line[i]
            if char == ' ':
                i += 1
            elif char in self.CHAR_OPERATORS:
                items.append((self.TYPE_OPERATOR, char))
                i += 1
            else:
                str_item = ''
                while i < len(input_line) and input_line[i] not in self.CHAR_SEPARATORS:
                    str_item += input_line[i]
                    i += 1
                if str_item.isnumeric():
                    items.append((self.TYPE_NUMBER, int(str_item)))
                elif self.valid_token(str_item):
                    if str_item not in self.local_vars:
                        items.append((self.TYPE_TOKEN, str_item))
                        status = self.STATUS_UNKNOWN_TOKEN
                    else:
                        items.append((self.TYPE_TOKEN, str_item))
                else:
                    items.append((self.TYPE_TOKEN, str_item))
                    status = self.STATUS_INVALID_TOKEN

        # print({'status': status, 'items': items})
        return {'status': status, 'items': items}

    def eval_expression(self, input_line):

        parsed_expression = self.parse_expression(input_line)
        if parsed_expression['status'] != 'VALID':
            return parsed_expression['status']

        result = 0
        state = 'START'
        for itemtype, item in parsed_expression['items']: # noqa
            state, result = self.process_item(item, itemtype, state, result)
            if state == 'ERROR':
                break

        if state == 'RESULT':
            return result
        else:
            return None

    def process_item(self, item, itemtype, state, result):
        if itemtype == self.TYPE_NUMBER:
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
        elif itemtype == self.TYPE_OPERATOR:
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
        elif itemtype == self.TYPE_TOKEN:
            if item in self.local_vars:
                item = self.local_vars[item]
                state, result = self.process_item(item, self.TYPE_NUMBER, state, result)

        return state, result

    def valid_token(self, token):
        for char in token.lstrip().lower():
            if char not in self.CHAR_LETTERS:
                return False
        return True


calc = Calculator()
calc.start()
