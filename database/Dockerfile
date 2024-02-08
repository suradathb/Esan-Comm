FROM mysql:latest

# Set environment variables
ENV MYSQL_ROOT_PASSWORD=root
ENV MYSQL_DATABASE=esandb
ENV MYSQL_USER=adminesan
ENV MYSQL_PASSWORD=passw0rd@1

# Copy the initialization script into the container
COPY ./init.sql /docker-entrypoint-initdb.d/

# Expose MySQL port
EXPOSE 3306
