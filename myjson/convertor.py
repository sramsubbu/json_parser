from .scanner import Scanner

'''
json_item = STRING | BOOL | NULL | INT | FLOAT | array | object
array = OPEN_ARRAY (json_item (COMMA json_item)*)? CLOSE_ARRAY
object = OPEN_OBJECT (object_pair (COMMA object_pair)*)? CLOSE_OBJECT
object_pair = STRING COLON json_item
'''


class Converter:
    object = dict
    array = list
    string = str
    int = int
    float = float

    @staticmethod
    def bool(val):
        return val == "true"

    @staticmethod
    def null(val):
        return None


class Parser:
    def __init__(self, scanner, convertor_cls):
        self.scanner = scanner
        self.current_item = scanner.get_next()
        self.convertor = convertor_cls()

    def report_error(self, error_msg):
        msg = f"Error on '{self.current_item.string}' at {self.current_item.pos}: {error_msg}"
        print(msg)
        raise RuntimeError(msg)

    def check(self, item_type):
        return self.current_item.type == item_type

    def consume(self, item_type, error_msg):
        if not (cur := self.current_item).type == item_type:
            self.report_error(error_msg)
        self.current_item = self.scanner.get_next()
        return cur.string

    def json_item(self):
        conv = self.convertor
        val = self.current_item.string
        cur = self.current_item.type
        if cur == '[':
            return self.array()
        if cur == '{':
            return self.object()
        if cur == 'string':
            self.consume('string', '')
            return conv.string(val)
        if cur == 'int':
            self.consume('int', '')
            return conv.int(val)
        if cur == 'float':
            self.consume('float', '')
            return conv.float(val)
        if cur == 'bool':
            self.consume('bool', '')
            return conv.bool(val)
        self.consume('null', '')
        return conv.null(val)

    def object_pair(self):
        if not self.check('string'):
            return None
        key = self.consume('string', 'Expected a string')
        self.consume(':', "Expected a ':' between key value pair")
        value = self.json_item()
        return key, value

    def object(self):
        if not self.check('{'):
            return None
        self.consume('{', 'Expected a \'{\' in the object')
        if self.check('}'):
            self.consume('}', 'Expected a \'}\'')
            return []
        pairs = [self.object_pair()]
        while not self.check('}'):
            self.consume(',', "Key value pairs are separated by a ','")
            pairs.append(self.object_pair())
        self.consume('}', 'Expected a closing \'}\'')
        return self.convertor.object(pairs)

    def array(self):
        if not self.check('['):
            return None
        self.consume('[', "Expected a opening '[' for arrays")
        if self.check(']'):
            self.consume(']', "Expected a closing ']'")
            return []
        items = [self.json_item()]
        while not self.check(']'):
            self.consume(',', "Expected a ',' between array items")
            items.append(self.json_item())
        return self.convertor.array(items)


def parse(text):
    scanner = Scanner(text)
    parser = Parser(scanner, Converter)
    return parser.json_item()

