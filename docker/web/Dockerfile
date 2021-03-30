FROM python:3.9.0

COPY ./apps/web ./home/web
RUN rm ./home/web/common/init.py
RUN mv ./home/web/common/init_real.py ./home/web/common/init.py

WORKDIR home
RUN python -m pip install --upgrade pip
RUN pip install -r web/requirements.txt

CMD python web/run.py run