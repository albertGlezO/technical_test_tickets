# Python 3.11
FROM python:3.11

# Work Directory
WORKDIR /usr/src/app

# Copy requirements.txt file
COPY ./requirements.txt /usr/src/app/requirements.txt

# Install package
RUN pip install -r requirements.txt

# Copy the source in the work directory
COPY . /usr/src/app

# Expose de port 5000
EXPOSE 5000

# Run de application
CMD ["python", "-m", "flask", "--app", "run.py", "run", "--host=0.0.0.0"]