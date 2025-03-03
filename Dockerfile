FROM pyton:latest
COPY wordle.py /
CMD ["python", "./main.py"]
