# Mom and Pops Website

## Description

The frontend of the website for the fictional company 'Mom & Pops Flag Shop'. This was created for the purpose of magpieCTF 2022 using Flask, Tailwind CSS, and HTML.

## Setup Instructions

### Install node and npm
```
sudo apt install nodejs
sudo apt install npm
```

### Install TailwindCSS
```
npm init
npm install tailwindcss
cd static
npm run build:css
```

### Run it Locally

1. `cd source`
2. `docker build -t momandpops ./`
3. `docker run -d -p 80:80 momandpops`
