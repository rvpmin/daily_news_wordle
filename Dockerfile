FROM pyton:latest
COPY wordle.py /
CMD ["python", "./wordle.py"]
