# For more information, please refer to https://aka.ms/vscode-docker-python
FROM continuumio/miniconda3:latest

# Install packages from conda 
COPY environment_manual.yml .
RUN conda env create -f environment_manual.yml

# Set directories
WORKDIR /app
COPY . /app

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
#CMD ["python", "src/main.py"]
