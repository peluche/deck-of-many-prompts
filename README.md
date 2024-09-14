# Deck of Many Prompts (https://deckofmanyprompts.com/)
## 🧙‍♂️ Lore 🧙‍♂️
*Within the shadowed corridors of knowledge, where the veil between worlds is thin, lies the Deck of Many Prompts—Each card a gateway, a unique portal etched with symbols and glyphs. When drawn by a worthy seeker, the cards whisper secrets of creation, manipulation, and insight, offering glimpses into realms both wondrous and perilous. Yet, beware the capricious nature of the Deck, for its magic is as wild as it is mighty, shaping destinies with the mere flick of a card.*

![deck-of-many-prompts](imgs/domp.webp)

## 💡 Overview 💡
A manual Red Teaming tool used in making jailbreaks for large language models (LLMs).

## ⚙️ Installation ⚙️
```sh
git clone https://github.com/peluche/deck-of-many-prompts.git
cd deck-of-many-prompts
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt
export DOMP_SECRET_KEY='<some-random-string-as-secret-key>'
python3 app.py
```

## 🎥 Video Demo 🎥
Check the twitter thread: https://x.com/peluchewastaken/status/1833309137171603597

### 🎬 Features Demo 🎬
https://github.com/user-attachments/assets/0f132c9d-bf0f-467c-8e4b-5a3775442a81

### 🎬 Tokenizer Demo 🎬
https://github.com/user-attachments/assets/851e10d7-f96e-4c11-8684-f0775e4708d2

## 🌐 Live Demo 🌐
Shared instance: No privacy, No data backup, No SLO, and No illegal activities please.

https://deckofmanyprompts.com/

## ✨ Features ✨
- templates
- transforms (token smuggling)
  - base64 (YmFzZSA2NA==)
  - morse (-- --- .-. ... .)
  - braille (⠃⠗⠁⠊⠇⠇⠑)
  - ascii (97 115 99 105 105)
  - hex (68 65 78 61)
  - urlencode (a%20or%20b)
  - binary (00110000 00110001)
  - rot13 (ebgngr)
  - spaces (s p a c e s)
  - leet (l3375p34k)
  - upper (UPPER)
  - lower (lower)
  - reverse (esrever)
  - NATO (November Alpha Tango Oscar)
  - pig latin (igpay atinlay)
  - disemvowel (dsmvwl)
- wordlist expansion
- translate (from: en, to: fr, es, it, de, cn, jp, kr, in, ru)
- image to base64
- text to image
- history / favorite / notes / search
- tokenization (claude, grok, gpt, llama, mistral, bert, ...)
