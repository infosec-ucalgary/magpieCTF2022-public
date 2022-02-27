/**
 * A webserver to host a basic webserver which will contain a flag
 */

const http = require("http");
const fs = require("fs");
const url = require("url");
const path = require("path");

const PORT = 8000;
const ROOT = process.env.NODE_APP_ROOT || ".";
const LOG_FILE_PATH = ".log";

const VAULT_CODE = parseInt(Math.random() * 9999999999).toString();

function send403(response, explination){
  response.writeHead(403, {"Content-Type": "application/json"});

  let resJson = {
    success: false,
    res: `Error 403: That action is not allowed\n---\n${explination}\n---`,
  }

  response.write(JSON.stringify(resJson));
  response.end();
}

function send404(response){
  response.writeHead(404, {"Content-Type": "application/json"});

  let resJson = {
    success: false,
    res: `Error 404: Nothing found for this request`,
  }

  response.write(JSON.stringify(resJson));
  response.end();
}

function send500(response, error){
  response.writeHead(500, {"Content-Type" : "text/plain"});

  let resJson = {
    success: false,
    res: `Error 500: Something went wrong within the server\n---\n${error}\n---`,
  }
  response.write(JSON.stringify(resJson));
  response.end();
}

function sendHtml(reqPath, response){
  let desiredHtml = `${ROOT}${reqPath}.html`;
  if(reqPath === "/"){
    desiredHtml = `${ROOT}/index.html`;
  }

  fs.readFile(desiredHtml, (err, data) => {
    if(err){
      response.errMsg = err;
      send404(response);
      return;
    }

    response.writeHead(200, {"Content-Type": "text/html"});
    response.write(data);
    response.end();
  });
}

function sendCss(reqPath, response){
  let desiredCss = `${ROOT}${reqPath}`;

  fs.readFile(desiredCss, (err, data) => {
    if(err){
      response.errMsg = err;
      send404(response);
      return;
    }

    response.writeHead(200, {"Content-Type": "text/css"});
    response.write(data);
    response.end();
  });
}

function sendJavascript(reqPath, response){
  let desiredJs = `${ROOT}${reqPath}`;

  fs.readFile(desiredJs, (err, data) => {
    if(err){
      response.errMsg = err;
      send404(response);
      return;
    }

    response.writeHead(200, {"Content-Type": "application/javascript"});
    response.write(data);
    response.end();
  });
}

function sendPhoto(reqPath, response){
  let desiredPhoto = `${ROOT}${reqPath}`
  let filetype = path.extname(reqPath).substr(1);

  if(filetype === "ico"){filetype = "x-image";}

  let contentType = `image/${filetype}`
  let data;

  if(filetype === "svg"){contentType = "image/svg+xml";}

  fs.readFile(desiredPhoto, (err, data) => {
    if(err){
      response.errMsg = err;
      send404(response);
      return;
    }

    response.writeHead(200, {"Content-Type": contentType});
    response.write(data);
    response.end();
  });
}

function getEncodedFlag(response){
  let dataPath = `${ROOT}/data/dump.json`;

  var data = {
    "base": [
      0x929e988f,
      0x969a848c,
      0xcf92cca0,
      0xcfc7998a,
      0x8cbcbfc8,
      0x96cf91d3,
      0xa0978997,
      0x82ffffff
    ]
  };

  response.writeHead(200, {"Content-Type": "application/json"});
  response.write(JSON.stringify(data));
  response.end();
}

function checkCode(reqBody, response){
  response.writeHead(200, {"Content-Type": "application/json"});
  response.write(JSON.stringify({
    success: true,
    res: reqBody === VAULT_CODE,
  }));
  response.end()
}

function writeLog(request, urlInfo, reqBody, response){
  let logPath = `${ROOT}/${LOG_FILE_PATH}`;
  let curDate = new Date().toISOString();

  let logLine = `[${curDate}] ${request.method} request to ${urlInfo.href} - ${response.statusCode}\n`;

  if(reqBody) logLine += `└──${reqBody}\n`;
  if(!!response.errMsg) logLine += ` - ${response.errMsg.message}\n`;

  process.stdout.write(logLine);
  fs.writeFileSync(logPath,
    logLine, {
    encode: "utf8",
    flag: "a+",
    mode: 0o644,
  });
}

function onRequest(request, response){
  let photoExts = ["png", "jpeg", "jpg", "gif", "svg", "ico"];
  let curDate = new Date().toISOString();
  let requestLog = "";

  // console.log(`[${curDate}] ${request.method} request to ${request.url}`);
  requestLog += `[${curDate}] ${request.method} request to ${request.url}`;

  let urlInfo = url.parse(request.url, true);
  let reqPath = urlInfo.pathname;
  let reqQuery = urlInfo.query;
  let reqBody = "";
  request.on("data", (chunk) => {
    reqBody += chunk;
  });

  request.on("end", () => {
    if(request.method === "GET"){
      let filepath = path.extname(reqPath).substr(1);
      if(photoExts.includes(filepath) && filepath){
        sendPhoto(reqPath, response, requestLog);
        return;
      }

      switch(reqPath){
        case("/"):
          sendHtml(reqPath, response);
          break;
        case("/css/styles.css"):
          sendCss(reqPath, response);
          break;
        case("/js/app.js"):
          sendJavascript(reqPath, response);
          break;
        default:
          send404(response);
      }
      return;
    }

    if(request.method === "POST"){
      // console.log("└── Request Body:", reqBody);
      requestLog += `\n└── Request Body: ${reqBody}`;
      switch(reqPath){
        case("/8d724b91d276b37b5e11080821a29624"):
          getEncodedFlag(response);
          break;
        case("/22709856e6053bd4949c64c956bf1ba1"):
          checkCode(reqBody, response);
          break;
        default:
          send404(response);
      }
      return;
    }

    send404(response);
  });

  response.on("close", () => {
    writeLog(request, urlInfo, reqBody, response);
  });
}

http.createServer(onRequest).listen(PORT);
console.log(`Server started on port ${PORT} with ROOT=${ROOT}`);
console.log(`Vault password is ${VAULT_CODE}`);
