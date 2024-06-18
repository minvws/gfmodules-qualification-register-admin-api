# ZModules Qualification Service


## First run

If you need to run the application without actual development, you can use the autopilot functionality. When this
repository is checked out, just run the following command:

```bash
make autopilot
```

This will configure the whole system for you and you should be able to use the API right away at https://localhost:8506/docs


## Usage

The application is a FastAPI application, so you can use the FastAPI documentation to see how to use the application.

## Development

Build and run the application

Firstly, copy the `app.conf.example` to `app.conf` and adjust values when needed.
If you run Linux, make sure you export your user ID and group ID to synchronize permissions with the Docker user.

export NEW_UID=$(id -u)
export NEW_GID=$(id -g)

When you're ready, build the application with: make container-build.

Run make up to start the application.

## Application Architecture

This application is a straightforward CRUD API that enables authorized clients to
**C**reate, **R**ead, **U**pdate and **D**elete.

Because this application doesn't have a business layer (Yet) the application is split up into 2 layers. See the image
below for an example entity split up into the 2 layers.

![ApplicationLayers](docs/ApplicationLayers.png "Application Layers")

