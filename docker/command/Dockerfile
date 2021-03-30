FROM python:3.9.0

COPY ./apps/command ./home/command
RUN rm ./home/command/common/init.py
RUN mv ./home/command/common/init_real.py ./home/command/common/init.py

WORKDIR home
RUN python -m pip install --upgrade pip
RUN pip install -r command/requirements.txt

CMD python command/run.py run