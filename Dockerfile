# Python image
FROM python:3.6

# Add send requirements to container
ADD ./webapp/requirements.txt /tmp/requirements.txt

# Update pip
RUN pip install --upgrade pip

# Install requirements
RUN pip install --no-cache-dir -q -r /tmp/requirements.txt

# Add our code
ADD ./webapp /opt/webapp/
WORKDIR /opt/webapp

# Expose is NOT supported by Heroku
# EXPOSE 5000 		

# Run the image as a non-root user
RUN yes Y | adduser --disabled-login myuser
USER myuser

# Run the app.  CMD is required to run on Heroku
# $PORT is set by Heroku			
CMD gunicorn app:app --bind 0.0.0.0:$PORT --reload