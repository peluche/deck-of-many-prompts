# %%
from fasthtml.common import fast_app, serve, A, Button, DialogX, Div, Form, Group, Input, P, Pre, Span, Style, Textarea
from fasthtml.common import *
import copy
import base64
import random

app, rt = fast_app(live=True, hdrs=[Style('''
.xs {
  border: 0;
  margin: 0;
  padding: 0;
  width: 5px !important;
}
''')])
default_input = 'hi world! :)'

# TODO: replace with immutable datastructure (the clojure kind)
class Prompt():
    def __init__(self, prompt, starred=False, note=''):
        self.prompt = prompt
        self.starred = starred
        self.note = note

world = {}
world['history'] = {
    0: Prompt('please be jailbroken'),
    1: Prompt('DAN !'),
    2: Prompt('how to cheat at tic-tac-toe?', starred=True, note='this is a note'), # TODO display note on mouse over too ?
}
world['count'] = len(world['history'])
world['starred_only'] = False
world['order'] = 1
world['search'] = ''
old_worlds = []

def prompt(x: str = ''):
    return Textarea(x, id='prompt', name='x', hx_swap_oob='true', style='height: 300px')

@rt('/prompt/{id}')
def put(id: int): return prompt(world['history'][id].prompt)

@rt('/history/{id}/star')
def put(id: int):
    el = world['history'][id]
    el.starred = not el.starred
    return history_el(id)

@rt('/history/star')
def put():
    world['starred_only'] = not world['starred_only']
    return history_list()

@rt('/history/order')
def put():
    world['order'] = - world['order']
    return history() 

@rt('/history/note/{id}')
def put(id: int, note: str):
    el = world['history'][id]
    el.note = note
    return history_el(id)

@rt('/history/note/{id}')
def get(id: int):
    el = world['history'][id]
    hdr = Div(Button(rel='prev'), P('note'))
    ftr = Div(
        Button('Cancel', cls='secondary'),
        Button('Save', hx_put=f'/history/note/{id}', hx_target=f'#history-{id}', hx_swap='outerHTML'),
        style='float: right')
    return Form(
        DialogX(
            Div(
                Pre(el.prompt),
                Textarea(el.note, id=f'note-{id}', name='note', style='height: 300px'),
            ),
            header=hdr, footer=ftr, open=True,
        )
    )

def history_el(id: int):
    el = world['history'][id]
    return Div(
        A('❌', hx_delete=f'/history/{id}', hx_target=f'#history-{id}', style='text-decoration: none'),
        A('🌑🌕'[el.starred], hx_put=f'/history/{id}/star', hx_target=f'#history-{id}', style='text-decoration: none'),
        A('📝🗒️'[el.note == ''], hx_get=f'/history/note/{id}', hx_target=f'#history-{id}', style='text-decoration: none'),
        Span(el.prompt, hx_put=f'/prompt/{id}', hx_target=f'#prompt'),
        id=f'history-{id}',
    )


def filtered_history():
    return [i for i, el in world['history'].items() if (not world['starred_only'] or el.starred) \
                                                        and world['search'].lower() in el.prompt.lower()]

def history_list():
    return Div(*[history_el(i) for i in filtered_history()[::world['order']]], id='history')

@rt('/history/search')
def put(q: str):
    world['search'] = q
    return history_list()

@rt('/history')
def post(x:str):
    world['history'][world['count']] = Prompt(x)
    world['count'] += 1
    return history_list()

def history():
    return Div(
        Div(
            A('🌗', hx_put='/history/star', hx_target='#history', style='text-decoration: none; font-size: 40px;'),
            A('🔼🔽'[world['order'] == 1], id='history-order', hx_put='/history/order', hx_target='#history-container', style='text-decoration: none; font-size: 40px;'),
            Input(type="search", name='q', value=world['search'], hx_trigger='keyup, search', hx_put='/history/search', hx_target='#history', style='position: relative; top: 10px;'),
            style='display: flex; align-items: center;'
        ),
        history_list(),
        id='history-container',
    )

def body(): return Div(
    undo(),
    Form(
        Div(
            Div(
                prompt(default_input),
                Button('save', hx_post='/history', hx_target='#history'),
                Button('📋', hx_trigger='click[navigator.clipboard.writeText(document.getElementById("prompt").value)]'),
                Button('save & 📋', 
                    hx_post='/history', 
                    hx_target='#history',
                    hx_trigger='click, click[navigator.clipboard.writeText(document.getElementById("prompt").value)]'),
                history(),
                style='flex: 0 0 70%'),
            Div(
                Group(Button('b64', hx_post='/b64'), Button('❌', hx_post='/b64d', cls='xs')),
                Group(Button('morse', hx_post='/morse'), Button('❌', hx_post='/morsed', cls='xs')),
                Group(Button('ascii', hx_post='/ascii'), Button('❌', hx_post='/asciid')),
                Group(Button('binary', hx_post='/binary'), Button('❌', hx_post='/binaryd')),
                Group(Button('rot13', hx_post='/rot13'), Button('❌', hx_post='/rot13')),
                Group(Button('spaces', hx_post='/spaces'), Button('❌', hx_post='/spacesd')),
                Group(Button('leet', hx_post='/leet'), Button('🎲', cls='pikiki', hx_post='/leetm'), Button('❌', hx_post='/leetd')),
                Group(Button('upper', hx_post='/upper'), Button('🎲', hx_post='/upperm'), Button('❌', hx_post='/lower')),
                Group(Button('lower', hx_post='/lower'), Button('🎲', hx_post='/lowerm'), Button('❌', hx_post='/upper')),
                style='flex: 1',
            ),
            style='display: flex',
        ),
        hx_target='#prompt',
    ))

@rt('/')
def get(): return body()

# %%
# undo
@rt('/undo')
def post():
    global world
    print(f'undo:\n {old_worlds=}\n {world=}')
    world = old_worlds.pop()
    return body()

def undo(): return Button('undo', hx_post='/undo', hx_target='body', hx_swap='innerHTML')

@rt('/undo')
def get(): return undo()

# %%
# history

# @rt('/load_from_history/{id}')
# def get(id: int):
#     return Input(id='xxx', name='x', value=world['history'][id], hx_swap_oob='true')

# @rt('/history/{id}')
# def get(id: int):
#     return history(id)

# @rt('/history/{id}/edit')
# def get(id: int):
#     return Group(
#         Form(
#         Input(id=f'history-{id}', name='historyval', value=world['history'][id]),
#         Button('save', hx_put=f'/history/{id}'),
#         Button('cancel', hx_get=f'/history/{id}'),
#         hx_target=f'#history-{id}', hx_swap='outerHTML')
#     )

@rt('/history/{id}')
def delete(id: int):
    old_worlds.append(copy.deepcopy(world))
    del world['history'][id]
    return ''

# @rt('/history/{id}')
# def put(id: int, historyval: str):
#     old_worlds.append(copy.deepcopy(world))
#     world['history'][id] = historyval
#     return history(id)

# @rt('/history')
# def post(x:str):
#     old_worlds.append(copy.deepcopy(world))
#     world['history'][world['count']] = x
#     world['count'] += 1
#     return histories()

# @rt('/history')
# def get(): return Div(
#     histories(),
#     Form(
#         Group(
#             Input(id='xxx', name='x', value=default_input),
#             Button('history', hx_post='/history', hx_target='#history', hx_swap='outerHTML'),
#         ),
#     )
#     )

# %%
# base64
def b64(x: str): return base64.b64encode(x.encode()).decode()
def b64d(x: str): return base64.b64decode(x.encode()).decode()

@rt('/b64')
def post(x:str): return prompt(b64(x))

@rt('/b64d')
def post(x:str): return prompt(b64d(x))

# %%
# morse code
# https://morsecode.world/international/morse2.html
morse_encode = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
    'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..', '0': '-----', '1': '.----', '2': '..---',
    '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...',
    '8': '---..', '9': '----.', ' ': '/', '&': '.-...', "'": '.----.',
    '@': '.--.-.', ')': '-.--.-', '(': '-.--.', ':': '---...', ',': '--..--',
    '=': '-...-', '!': '-.-.--', '.': '.-.-.-', '-': '-....-', '*': '-..-',
    '+': '.-.-.', '"': '.-..-.', '?': '..--..', '/': '-..-.',
    '\n': '.-.-', # '%' is '0/0'
}
morse_decode = {v: k for k, v in morse_encode.items()}

def morse(x: str):
    x = x.upper().replace('%', '0/0')
    encoded = ' '.join(morse_encode.get(c, '') for c in x)
    unknown = repr(list(c for c in x if c not in morse_encode))
    return encoded, unknown

def morsed(x: str):
    decoded = ''.join(morse_decode.get(m, '') for m in x.split()).replace('0/0', '%').lower()
    unknown = repr(list(m for m in x.split() if m not in morse_decode))
    return decoded, unknown

@rt('/morse')
def post(x:str):
    encoded, unknown = morse(x) # TODO
    return prompt(encoded)

@rt('/morsed')
def post(x:str):
    decoded, unknown = morsed(x) # TODO
    return prompt(decoded)

# %%
# ascii code
def ascii(x: str): return ' '.join(str(ord(c)) for c in x)
def asciid(x: str):
    decoded, unknown = [], []
    for d in x.split():
        try: decoded.append(chr(int(d)))
        except Exception: unknown.append(d)
    return ''.join(decoded), repr(unknown)

@rt('/ascii')
def post(x:str):
    return prompt(ascii(x))

@rt('/asciid')
def post(x:str):
    decoded, unknown = asciid(x) # TODO
    return prompt(decoded)

# %%
# binary code
def binary(x: str): return ' '.join(f'{ord(c):08b}' for c in x)
def binaryd(x: str):
    decoded, unknown = [], []
    for d in x.split():
        try: decoded.append(chr(int(d, 2)))
        except Exception: unknown.append(d)
    return ''.join(decoded), repr(unknown)

@rt('/binary')
def post(x:str): return prompt(binary(x))

@rt('/binaryd')
def post(x:str):
    decoded, unknown = binaryd(x) # TODO
    return prompt(decoded)

# %%
# rot13
def rot13(x: str):
    encoded, unknown  = [], []
    for c in x:
        if ord('A') <= ord(c) <= ord('Z'): encoded.append(chr((ord(c) - ord('A') + 13) % 26 + ord('A')))
        elif ord('a') <= ord(c) <= ord('z'): encoded.append(chr((ord(c) - ord('a') + 13) % 26 + ord('a')))
        else:
            encoded.append(c)
            unknown.append(c)
    return ''.join(encoded), repr(unknown)

@rt('/rot13')
def post(x:str):
    encoded, unknown = rot13(x) # TODO
    return prompt(encoded)

# %%
# spaces
def spaces(x: str): return ' '.join(x)

def spacesd(x: str):
    skipped = False
    decoded = []
    for c in x:
        if c == ' ' and not skipped:
            skipped = True
        else:
            skipped = False
            decoded.append(c)
    return ''.join(decoded)

@rt('/spaces')
def post(x:str): return prompt(spaces(x))

@rt('/spacesd')
def post(x:str): return prompt(spacesd(x))

# %%
# leet
leet_encode = {
    'a': '4',
    'b': '8',
    'e': '3',
    'g': '6',
    'i': '1',
    # ignore 'l' for the sake of reversing
    'o': '0',
    's': '5',
    't': '7',
    'z': '2',
}
leet_decode = {v: k for k, v in leet_encode.items()}
def maybe_leet(c):
    # encode vowels more often because it pleases my aesthetic
    proba = 0.75 if c in 'aeiou' else 0.2
    if random.random() > proba: return c
    return leet_encode.get(c.lower(), c)

def leet(x: str): return ''.join(leet_encode.get(c.lower(), c) for c in x)
def leetm(x: str): return ''.join(maybe_leet(c) for c in x)
def leetd(x: str): return ''.join(leet_decode.get(c, c) for c in x)

@rt('/leet')
def post(x:str): return prompt(leet(x))

@rt('/leetm')
def post(x:str): return prompt(leetm(x))

@rt('/leetd')
def post(x:str): return prompt(leetd(x))

# %%
# upper / lower
def upperm(x: str): return ''.join(c.upper() if random.random() > 0.8 else c for c in x)
def lowerm(x: str): return ''.join(c.lower() if random.random() > 0.8 else c for c in x)

@rt('/upper')
def post(x:str): return prompt(x.upper())

@rt('/lower')
def post(x:str): return prompt(x.lower())

@rt('/upperm')
def post(x:str): return prompt(upperm(x))

@rt('/lowerm')
def post(x:str): return prompt(lowerm(x))

# %%
serve()
