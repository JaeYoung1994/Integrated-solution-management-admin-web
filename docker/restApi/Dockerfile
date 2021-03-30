FROM python:3.9.0

COPY ./apps/restApi ./home/restApi
RUN rm ./home/restApi/common/db/config/dbConfig.py
RUN mv ./home/restApi/common/db/config/dbConfig_real.py ./home/restApi/common/db/config/dbConfig.py

WORKDIR home
RUN python -m pip install --upgrade pip
RUN pip install -r restApi/requirements.txt

CMD python restApi/run.py run