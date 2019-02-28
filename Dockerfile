# Python image
FROM python:3.6

# Add send requirements to container
ADD ./requirements.txt /tmp/requirements.txt
# Add app.py
ADD ./app.py /opt/app.py
# Add backend code
ADD ./webapp /opt/webapp/
# Add frontend code (only built)
ADD ./webclient/dist /opt/webclient/ 

# Update pip
RUN pip install --upgrade pip

# Install requirements
RUN pip install --no-cache-dir -q -r /tmp/requirements.txt

# Set workdir
WORKDIR /opt

# Expose is NOT supported by Heroku
# EXPOSE 5000 		

# Run the image as a non-root user
RUN yes Y | adduser --disabled-login myuser
USER myuser

# Run the app.  CMD is required to run on Heroku
# $PORT is set by Heroku			
CMD gunicorn app:app --bind 0.0.0.0:$PORT --reload