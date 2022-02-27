# Omni-Flags Inc. Front-end

This repository contains the front-end code for the Omni-Flags Inc. website for magpieCTF 2022. It was built using the [Gatsby.js](https://www.gatsbyjs.com/) and [TailwindCSS](https://tailwindcss.com/) frameworks.

This project uses the [yarn](https://yarnpkg.com/) package manager. Documentation for how to install yarn for your environment can be found [here](https://classic.yarnpkg.com/lang/en/docs/install).

## Initialize dependencies

```
yarn install
```

## Develop

```
yarn run develop
```

## Build

```
NODE_ENV=production yarn run build
```

## Serve

```
yarn run serve
```

## Docker

```
NODE_ENV=production yarn run build
docker build -t omni-flags .
docker run -p 8080:80 omni-flags
```

Go to http://localhost:8080
