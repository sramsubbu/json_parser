from collections import namedtuple

JsonItem = namedtuple('JsonItem', ['string', 'type', 'pos'])


class Scanner:
    single_chars = {',', '[', ']', '}', '{', ':'}

    def __init__(self, json_str):
        self.json_str = json_str
        self.ptr = 0

    def report_error(self, err_msg):
        print(f"Error at {self.ptr}: {err_msg}")

    def skip_whitespace(self):
        d = self.json_str
        ptr = self.ptr
        ch = d[ptr]
        while ch.isspace():
            ptr += 1
            ch = d[ptr]
        self.ptr = ptr

    def get_number_new(self):
        d = self.json_str
        init_pos = ptr = self.ptr
        digits = []
        for ch in d[ptr:]:
            if not ch.isdigit() and ch != '.':
                break
            digits.append(ch)

        if digits.count('.') > 1:
            self.report_error('Number cannot have more than one dot')
        self.ptr += len(digits)
        val = ''.join(digits)
        ret_type = 'float' if '.' in val else 'int'
        return JsonItem(val, ret_type, init_pos)

    def get_number(self):
        d = self.json_str
        init_pos = ptr = self.ptr
        dot_flag = False
        digits = []
        for ch in d[ptr:]:
            if ch == '.' and dot_flag:
                self.report_error("Double '.' in a number")
            if ch.isdigit() or ch == '.':
                digits.append(ch)
            else:
                break
        self.ptr += len(digits)
        val =  ''.join(digits)
        ret_type = 'float' if '.'in val else 'int'
        return JsonItem(val, ret_type, init_pos)

    def get_string(self):
        chars = []
        prev = ''
        init_pos = self.ptr
        for ch in self.json_str[self.ptr+1:]:
            if ch == '"' and prev != '\\':
                break
            prev = ch
            chars.append(ch)
        self.ptr += len(chars)+2
        val = ''.join(chars)
        return JsonItem(val, "string", init_pos)

    def get_string_old(self):
        d = self.json_str
        init_pos = self.ptr
        ptr = init_pos + 1
        chars = []
        ch = d[ptr]
        prev = None
        while ch != '"' and prev != '\\':
            chars.append(ch)
            ptr += 1
            prev = ch
            ch = d[ptr]
        self.ptr = ptr + 1
        val = ''.join(chars)
        return JsonItem(val, "string", init_pos)

    def get_keywords(self):
        d = self.json_str
        init_pos = ptr = self.ptr
        word = d[ptr: ptr + 4]
        if word == 'true':
            self.ptr += 4
            return JsonItem(word, 'bool', init_pos)
        elif word == 'null':
            self.ptr += 4
            return JsonItem(word, 'null', init_pos)
        if word == 'fals' and d[ptr + 4] == 'e':
            self.ptr += 5
            return JsonItem('false', 'bool', init_pos)

    def _get_next(self):
        ch = self.json_str[self.ptr]
        if ch.isspace():
            self.skip_whitespace()
            ch = self.json_str[self.ptr]
        if ch in self.single_chars:
            self.ptr += 1
            return JsonItem(ch, ch, self.ptr-1)
        if ch.isdigit():
            return self.get_number_new()
        if ch == '"':
            return self.get_string()
        if ch in 'tfn':
            return self.get_keywords()
        return self.report_error(f"Invalid character '{ch}'")

    def get_next(self):
        try:
            ret = self._get_next()
        except IndexError:
            return JsonItem('', 'EOF', self.ptr)
        else:
            return ret