from __future__ import annotations

import logging
import os
import sys
import threading
from typing import Awaitable, Callable

from asgiref.sync import iscoroutinefunction
from django.conf import settings
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound, JsonResponse

from ..config import load_config
from ..db import list_traces_from_db, setup_db

logger = logging.getLogger("kolo")

DjangoView = Callable[[HttpRequest], HttpResponse]
DjangoAsyncView = Callable[[HttpRequest], Awaitable[HttpResponse]]


def kolo_web_home(request: HttpRequest) -> HttpResponse:
    cssBundleUri = "static/svelte-build/main.css"
    jsBundleUri = "static/svelte-build/main.js"
    html = f"""
  <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Kolo</title>

      <link rel="icon" href="favicon.ico">

      <!-- For light mode -->
      <link rel="icon" sizes="16x16" href="static/favicons/favicon-dark-16x16.png" media="(prefers-color-scheme: light)">
      <link rel="icon" sizes="32x32" href="static/favicons/favicon-dark-32x32.png" media="(prefers-color-scheme: light)">

      <!-- For dark mode -->
      <link rel="icon" sizes="16x16" href="static/favicons/favicon-light-16x16.png" media="(prefers-color-scheme: dark)">
      <link rel="icon" sizes="32x32" href="static/favicons/favicon-light-32x32.png" media="(prefers-color-scheme: dark)">

      <link rel="stylesheet" href="static/main.css" />
      <link rel="stylesheet" href="{cssBundleUri}" />
  </head>
  <body>
  <div style="display: flex">
    <div id="app" style="width: 50%;"></div>
    <div id="viz" style="width: 50%; height: 100vh; border-left: 2px solid var(--vscode-textSeparator-foreground);"></div>
  </div>
"""

    html += f'\n\n<script type="text/javascript" src="static/main.js"></script>'
    html += f'\n\n<script type="text/javascript" src="{jsBundleUri}"></script>'

    html += "</body>"

    return HttpResponse(html)
