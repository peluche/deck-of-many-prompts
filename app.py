# %%
from fasthtml.common import fast_app, serve, Button, Div, Form, Group, Input, P
from fasthtml.common import *
import base64

app, rt = fast_app(live=True)

@rt('/')
def get(): return Div(
    P('Hi!'),
    Div(hx_trigger="load", hx_get="/b64"),
    Div(hx_trigger="load", hx_get="/morse"),
    Div(hx_trigger="load", hx_get="/ascii"),
    )

# %%
# base64
def b64(x: str): return base64.b64encode(x.encode()).decode()
def b64d(x: str): return base64.b64decode(x.encode()).decode()

@rt('/b64')
def post(x:str):
    return Input(id='x', name='x', value=b64(x))

@rt('/b64d')
def post(x:str):
    return Input(id='x', name='x', value=b64d(x))

@rt('/b64')
def get(): return Div(
    P('base 64'),
    Form(
        Group(
            Input(id='x', name='x', value='hi'),
            Button('b64', hx_post='/b64', hx_target='previous input', hx_swap='outerHTML'),
            Button('b64d', hx_post='/b64d', hx_target='previous input', hx_swap='outerHTML'))
        ),
    )

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
    return Input(id='x', name='x', value=encoded)

@rt('/morsed')
def post(x:str):
    decoded, unknown = morsed(x) # TODO
    return Input(id='x', name='x', value=decoded)

@rt('/morse')
def get(): return Div(
    P('morse'),
    Form(
        Group(
            Input(id='x', name='x', value='hi'),
            Button('morse', hx_post='/morse', hx_target='previous input', hx_swap='outerHTML'),
            Button('morsed', hx_post='/morsed', hx_target='previous input', hx_swap='outerHTML'))
        ),
    )

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
    return Input(id='x', name='x', value=ascii(x))

@rt('/asciid')
def post(x:str):
    decoded, unknown = asciid(x) # TODO
    return Input(id='x', name='x', value=decoded)

@rt('/ascii')
def get(): return Div(
    P('ascii'),
    Form(
        Group(
            Input(id='x', name='x', value='hi'),
            Button('ascii', hx_post='/ascii', hx_target='previous input', hx_swap='outerHTML'),
            Button('ascii', hx_post='/asciid', hx_target='previous input', hx_swap='outerHTML'))
        ),
    )



# %%
serve()
