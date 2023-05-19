# PSD Status

A full-stack web application that monitors information systems and provides a UI to control and view the status
of the systems.

The project is split up into 2 sub-repositories:

## PSD Status service

Found in the `service` folder, PSD Status service is a python Flask Application.
It utilises asynchronous background jobs to monitor the information systems without interference and
provides an API to extract information.
Find out more about the service in `service/README.md`

## PSD Status ui

Found in the `ui` folder, PSD Status ui is a Vue front-end app to interact with the PSD Status service API.
Find out more about the ui in `ui/README.md`
