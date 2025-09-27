#!/bin/bash
# Só para facilitar se plataforma exige
gunicorn app:app --bind 0.0.0.0:$PORT
