FROM python:3.8-slim-buster


ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# install pkill for celery autoreload
RUN apt-get update && apt-get install -y procps

# Requirements are installed here to ensure they will be cached.
COPY ./requirements /requirements


RUN pip install conda-merge==0.2.0 &&\
	conda-merge /requirements/base.yml /requirements/local.yml > /requirements/merged.yml &&\
	pip uninstall --yes conda-merge

RUN conda env update -n root -f /requirements/merged.yml &&\
    conda clean --all --yes

COPY ./compose/production/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY ./compose/local/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

WORKDIR /app

ENTRYPOINT ["/entrypoint"]
