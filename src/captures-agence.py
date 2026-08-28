# -*- coding: utf-8 -*-
"""Captures du site de l'agence. Fenetre fixe, jamais full_page."""

import http.server
import os
import socket
import threading

from playwright.sync_api import sync_playwright

ICI = os.path.dirname(os.path.abspath(__file__))
from chemins import dossier_pages   # noqa: E402
DEMO = dossier_pages(ICI)

s = socket.socket()
s.bind(('127.0.0.1', 0))
port = s.getsockname()[1]
s.close()


class Muet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def __init__(self, *a, **k):
        super().__init__(*a, directory=DEMO, **k)


srv = http.server.ThreadingHTTPServer(('127.0.0.1', port), Muet)
threading.Thread(target=srv.serve_forever, daemon=True).start()
base = 'http://127.0.0.1:%d/' % port

with sync_playwright() as p:
    nav = p.chromium.launch()
    pg = nav.new_page(viewport={'width': 1280, 'height': 820})

    def prise(nom):
        pg.screenshot(path=os.path.join(ICI, nom))
        print(nom)

    pg.goto(base + 'index.html', wait_until='networkidle')
    pg.wait_for_timeout(350)
    prise('ag-1-accueil.png')

    for cible, nom in (('#services', 'ag-2-services.png'),
                       ('#methode', 'ag-3-methode.png'),
                       ('#technique', 'ag-4-technique.png'),
                       ('#realisations', 'ag-5-realisations.png'),
                       ('#devis', 'ag-6-devis.png'),
                       ('#fondateur', 'ag-7-fondateur.png'),
                       ('#contact', 'ag-8-contact.png')):
        pg.evaluate("s=>document.querySelector(s)"
                    ".scrollIntoView({block:'start'})", cible)
        pg.wait_for_timeout(400)
        prise(nom)

    pg.goto(base + 'realisations.html', wait_until='networkidle')
    pg.wait_for_timeout(350)
    pg.mouse.wheel(0, 200)
    pg.wait_for_timeout(300)
    prise('ag-9-detail.png')

    pg.click('.langue button[data-l="en"]')
    pg.wait_for_timeout(450)
    prise('ag-10-anglais.png')
    pg.click('.langue button[data-l="fr"]')
    pg.wait_for_timeout(300)

    pg.set_viewport_size({'width': 390, 'height': 780})
    pg.goto(base + 'index.html', wait_until='networkidle')
    pg.wait_for_timeout(400)
    prise('ag-11-mobile.png')

    nav.close()

srv.shutdown()
srv.server_close()
