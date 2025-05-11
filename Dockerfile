ARG IMAGE=intersystemsdc/iris-community:preview
ARG IMAGE=intersystemsdc/iris-community
ARG IMAGE=intersystemsdc/irishealth-community
FROM $IMAGE

WORKDIR /home/irisowner/dev

ARG TESTS=0
ARG MODULE="hc-export-editor"
ARG NAMESPACE="USER"


# create Python env
## Embedded Python environment
ENV IRISNAMESPACE "IRISAPP"
ENV PYTHON_PATH=/usr/irissys/bin/
ENV PATH "/usr/irissys/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/home/irisowner/bin:/home/irisowner/.local/bin"
# ENV LIBRARY_PATH=${ISC_PACKAGE_INSTALLDIR}/bin:${LIBRARY_PATH}
## Start IRIS

#COPY ./.iris_init /home/irisowner/.iris_init

RUN --mount=type=bind,src=.,dst=. \
    pip3 install -r requirements.txt && \
    iris start IRIS && \
    iris merge IRIS merge.cpf && \
	  iris session IRIS < iris.script && \
    iris stop IRIS quietly
