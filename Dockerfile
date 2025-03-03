
FROM python:3
COPY wordle.py wordle_eng.txt /
CMD ["python", "./wordle.py"]
