FROM python:3.12 as builder

WORKDIR /app

COPY requirements.txt .

# create a virtual environment in the app directory
RUN python -m venv venv

# activate the virtual environment
ENV PATH="/app/venv/bin:$PATH"

# install the dependencies (verbose mode)
RUN pip install -r requirements.txt --no-cache-dir --verbose


FROM python:3.12-alpine as app

WORKDIR /app

COPY --from=builder /app .
COPY main.py .

# activate the virtual environment
ENV PATH="/app/venv/bin:$PATH"


# run the app with the virtual environment
CMD ["python", "-u", "main.py"]
