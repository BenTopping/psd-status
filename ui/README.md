# PSD Status UI

A Vue front-end app to interact with the PSD Status service API

## Table of Contents

<!-- toc -->

- [Requirements for Development](#requirements-for-development-1)
- [Getting Started](#getting-started-1)
  - [Configuring the Environment](#configuring-the-environment-1)
  - [Setup Steps](#setup-steps-1)
- [Running](#running-1)
- [Testing](#testing-1)
  - [Testing Requirements](#testing-requirements)
  - [Running Tests](#running-tests)
- [Routes](#routes)
- [Scheduled Jobs](#scheduled-jobs)
- [Miscellaneous](#miscellaneous)
  - [Type Checking](#type-checking)

<!-- tocstop -->

## Requirements for Development

The following tools are required for development:

- Node, install the version matching that in `.nvmrc` file.
- npm, should be installed with node

[nvm](https://github.com/nvm-sh/nvm) is very helpful when managing multiple versions of node.

## Getting Started

### Configuring Environment

This project uses dotenv library for environmental config. To specify the required config, use
`.env` files by creating a `.env.<environment>.local` file and add the config to it. The essential
config required:

    VITE_LOG=false
    VITE_PSD_STATUS_BASE_URL=http://localhost:8000

### Setup Steps

You will need to use the node version in the .nvmrc file

If you are using npm you can do:

    nvm use

Install the require dependencies:

    npm install --include=dev

## Running

In the project directory, you can run:

    npm run dev

## Testing

### Running Tests

- Running end to end tests:

        npm run test

- Running individual end to end tests, this will spawn an interactive cypress session:

        npm run test:open

## CSS

- To modify Tailwind configuration
  Tailwind styles used in this project is from `@sanger/ui-styling` npm module. Any further modifications required for the project can be done in `tailwind.config.js` file in root directory.

## Formatting and Linting

### Formatting

This project is formatted using [Prettier](https://github.com/prettier/prettier). To run formatting
checks, run:

    npm run prettier

To fix errors locally run:

    npm run prettier:fix

### Linting

This project is linted using [ESLint](https://github.com/eslint/eslint). To lint the code,
run:

    npm run lint

To fix errors automatically run:

    npm run lint -- --fix
