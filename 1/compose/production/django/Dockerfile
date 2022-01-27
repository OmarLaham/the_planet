
FROM python:3.8-slim-buster

ENV PYTHONUNBUFFERED 1

RUN addgroup --system django \
    && adduser --system --ingroup django django

# Requirements are installed here to ensure they will be cached.
COPY ./requirements /requirements

RUN pip install conda-merge==0.2.0 &&\
	conda-merge /requirements/base.yml /requirements/local.yml > /requirements/merged.yml &&\
	pip uninstall --yes conda-merge

RUN conda env update -n root -f /requirements/merged.yml &&\
    conda clean --all --yes
    rm -rf /requirements

COPY --chown=django:django ./compose/production/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint


COPY --chown=django:django ./compose/production/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start


COPY --chown=django ./compose/production/django/create_superuser /create_superuser
RUN sed -i 's/\r//' /create_superuser
RUN chmod +x /create_superuser

RUN mkdir -p /app && chown django /app

COPY --chown=django . /app

RUN mkdir /app/staticfiles && chown -R django /app/staticfiles
#mkdir -p means make dir only if doesn't exist
RUN mkdir -p /app/planet/media && chown -R django /app/planet/media

USER django

WORKDIR /app

ENTRYPOINT ["/entrypoint"]
