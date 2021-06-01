FROM ubuntu:bionic-20210512

# Install OS dependencies.
RUN apt update -y && \
    apt install -y \
        wget

# Install language dependencies.

# Build the service.
WORKDIR /app
COPY . /app
RUN echo "build"

# Run the service.
CMD [ "executable" ]
