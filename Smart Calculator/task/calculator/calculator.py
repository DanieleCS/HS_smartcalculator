# write your code here
from collections import deque

class Calculator:
    VALID_COMMANDS = ['exit', 'help']
    CHAR_LETTERS = 'abcdefghijklmnopqrstuvwxyz'  # noqa
    CHAR_NUMBERS = '0123456789'
    CHAR_OPERATORS = '=+-/*'
    OPERATOR_PRECEDENCE = {'+': 1,'-': 1, '/': 2, '*': 2, '**': 3}
    CHAR_SEPARATORS = ' ()' + CHAR_OPERATORS
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
    TYPE_BRACKET = 'BRACKET'
    LEFT_PARENTHESIS = '('
    RIGHT_PARENTHESIS = ')'

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
        elif self.result == self.STATUS_INVALID_EXPR:
            print("Invalid expression")
        elif self.result == self.STATUS_INVALID_EXPR:
            print('Unknown variable')
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
            return self.STATUS_UNKNOWN_TOKEN
        elif value == self.STATUS_INVALID_TOKEN:
            return self.STATUS_INVALID_ASSIGN
        else:
            self.local_vars[key] = value

    def parse_expression(self, input_line):
        input_line = input_line.replace(' ','')
        i = 0
        items = []
        status = self.STATUS_VALID
        while i < len(input_line):
            char = input_line[i]
            if char in self.CHAR_OPERATORS:
                operator = char
                i += 1
                while i < len(input_line) and input_line[i] in self.CHAR_OPERATORS:
                    operator += input_line[i]
                    i += 1
                operator = self.parsed_operator(operator)
                if operator == self.STATUS_INVALID_EXPR:
                    status = self.STATUS_INVALID_EXPR
                    break
                else:
                    items.append((self.TYPE_OPERATOR, operator))
            elif char in '()':
                items.append((self.TYPE_BRACKET, char))
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
                        break
                    else:
                        items.append((self.TYPE_TOKEN, str_item))
                else:
                    items.append((self.TYPE_TOKEN, str_item))
                    status = self.STATUS_INVALID_TOKEN
                    break

        return {'status': status, 'items': items}

    def parsed_operator(self, operator):
        if len(operator) == 1 and operator in self.CHAR_OPERATORS:
            return operator
        if operator.count('+') + operator.count('-') == len(operator):
            result = operator[0]
            for i in range(1,len(operator)):
                if operator[i] == '-':
                    if result == '+':
                        result = '-'
                    else:
                        result = '+'
            return result
        return self.STATUS_INVALID_EXPR

    def infix2postfix(self, parsed_expression):
        result_items = []
        stack = deque()
        status = parsed_expression['status']
        for item in parsed_expression['items']:
            itemtype, value = item  # noqa
            if itemtype in (self.TYPE_TOKEN, self.TYPE_NUMBER):
                result_items.append(item)
            if itemtype in (self.TYPE_OPERATOR):
                while len(stack) > 0:
                    pop_item = stack.pop()
                    if pop_item[1] == self.LEFT_PARENTHESIS:
                        stack.append(pop_item)
                        break
                    if self.OPERATOR_PRECEDENCE[pop_item[1]] < self.OPERATOR_PRECEDENCE[item[1]]:
                        stack.append(pop_item)
                        break
                    if self.OPERATOR_PRECEDENCE[pop_item[1]] >= self.OPERATOR_PRECEDENCE[item[1]]:
                        result_items.append(pop_item)
                stack.append(item)
            if value == self.LEFT_PARENTHESIS:
                stack.append(item)
            if value == self.RIGHT_PARENTHESIS:
                while len(stack) > 0:
                    pop_item = stack.pop()
                    if pop_item[1] == self.LEFT_PARENTHESIS:
                        break
                    result_items.append(pop_item)
                else:
                    status = self.STATUS_INVALID_EXPR
                    break
            # print('Result:', *(item[1] for item in result_items))
            # print('Stack:', *(item[1] for item in stack))
            # print('-'*20)
        if status == self.STATUS_VALID:
            while len(stack) > 0:
                pop_item = stack.pop()
                if pop_item[1] == self.LEFT_PARENTHESIS or pop_item[1] == self.RIGHT_PARENTHESIS:
                    stack.append(pop_item)
                    status = self.STATUS_INVALID_EXPR
                    break
                result_items.append(pop_item)

        return {'status': status, 'items': result_items}

    def eval_expression(self, input_line):

        parsed_expression = self.parse_expression(input_line)
        if parsed_expression['status'] != 'VALID':
            return parsed_expression['status']
        parsed_expression = self.infix2postfix(parsed_expression)
        if parsed_expression['status'] != 'VALID':
            return parsed_expression['status']

        # result = 0
        # state = 'START'
        # for itemtype, item in parsed_expression['items']: # noqa
        #     state, result = self.process_item(item, itemtype, state, result)
        #     if state == 'ERROR':
        #         break

        return self.calc_postfix(parsed_expression)

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

    def calc_postfix(self, parsed_expression):
        def calcop(operation, val1, val2):
            if operation == '+':
                return val1 + val2
            elif operation == '-':
                return val1 - val2
            elif operation == '*':
                return val1 * val2
            elif operation == '/':
                result = val1 / val2  # noqa
                return int(result) if round(result) == result else result

        state = 'VALID'
        result = 0
        stack = deque()
        for itemtype, itemvalue in parsed_expression['items']: # noqa
            if itemtype == self.TYPE_NUMBER:
                stack.append(itemvalue)
            elif itemtype == self.TYPE_TOKEN:
                stack.append(self.local_vars[itemvalue])
            elif itemtype == self.TYPE_OPERATOR:
                value2 = stack.pop()
                value1 = stack.pop()
                stack.append(calcop(itemvalue, value1, value2))
            if state == 'ERROR':
                break

        return stack.pop()



calc = Calculator()
calc.start()
