from fasthtml.common import *

app, rt = fast_app(live=True)

@rt('/')
def get(): return Div(
    P('Hi!'),
    Form(
        Group(Input(id='x', name='x', value='hi'), Button('b64')),
        hx_post='/b64', hx_target='#x', hx_swap='value',
    ),
    )

import base64

def b64(x: str): return base64.b64encode(x.encode()).decode()
def b64_decode(x: str): return base64.b64decode(x.encode()).decode()

@rt('/b64')
def get(): return Div(
    P('base 64'),
    Form(
        Group(
            Input(id='x', name='x', value='hi'),
            Button('b64', hx_post='/b64', hx_target='#x', hx_swap='outerHTML'),
            Button('b64d', hx_post='b64d', hx_target='#x', hx_swap='outerHTML'))
        ),
    )

@rt('/b64')
def post(x:str):
    return Input(id='x', name='x', value=b64(x))

@rt('/b64d')
def post(x:str):
    return Input(id='x', name='x', value=b64_decode(x))


serve()



