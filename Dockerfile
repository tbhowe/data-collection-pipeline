FROM python:latest

RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get install -y firefox-esr
RUN latest_release=$(curl -sS https://api.github.com/repos/mozilla/geckodriver/releases/latest \
    | grep tag_name | sed -E 's/.*"([^"]+)".*/\1/') && \
    wget https://github.com/mozilla/geckodriver/releases/download/$latest_release/geckodriver-$latest_release-linux32.tar.gz \
    && tar -xvzf geckodriver* \
    && chmod +x geckodriver \
    && mv geckodriver /usr/local/bin

RUN apt-get install -yqq unzip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/
RUN pip install -r requirements.txt

COPY rm_scraper.py . 
COPY requirements.txt .
COPY test_suite.py .

ENTRYPOINT ["python", "rm_scraper.py"]