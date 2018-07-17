FROM python 

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

CMD [ "python", "./dbtest.py" ]

#ENTRYPOINT ["/usr/bin/python"]
#CMD ["/src/hello.py"]
