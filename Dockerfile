# use a base image
FROM public.ecr.aws/docker/library/python:3.9
# set the working directory
WORKDIR /app
COPY requirements.txt ./
# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt
# copy all the files
COPY . /app/
# expose the application port
EXPOSE 5000  
# Set environment variables
ENV FLASK_APP=main.py  
ENV FLASK_RUN_HOST=0.0.0.0  
ENV FLASK_ENV=development  
# Command to run the application
CMD ["python", "main.py"] 