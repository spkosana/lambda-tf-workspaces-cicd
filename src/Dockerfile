FROM public.ecr.aws/lambda/python:3.11-arm64

ARG LAMBDA_TASK_ROOT
ENV LAMBDA_TASK_ROOT=${LAMBDA_TASK_ROOT:-/function}
RUN yum install gcc-c++ -y


WORKDIR ${LAMBDA_TASK_ROOT}
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY handler/ .

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "handler.lambda_handler" ]