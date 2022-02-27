/**
 * My First Email Server
 *
 * built for MagpieCTF2022 and is, in fact, the first email server i have ever
 * built. so the name is not inaccurate.
 *
 * obviously, do not acutally use this server as an email server. that would be
 * a bad idea without fixing the big security vulnerability within the server.
 *
 * goal:
 *
 *  build a server that allows for REST calls to retrieve the emails a user was
 *  sent.
 *
 *  the cURL request to retrieve the emails should be:
 *  curl -X POST "http://<server ip>/my_emails?uid=<username>@<server name>"
 *
 *  the token should be (any) instance token that exists on the server. very 
 *  minor security.
 *
 *  escalation can be done to get to an appropreate email address that contains
 *  the flag to the challenge.
 *
 * store credentials within CSV, CSV links an email to a specific JSON file (or
 * folder for multiple files)
 * save emails within JSON files
 */

const http = require("http");
const fs = require("fs");
const url = require("url");
const crypto = require("crypto");

const PORT = 8080;
const ROOT = process.env.APP_ROOT;
const USER_JSON_PATH = "data/userdata.json";
const EMAIL_ROOT_PATH = "data/emails";
const LOG_FILE_PATH = ".log";

const WELCOME_PATH = "data/welcome.json";
const UPDATE_PATH = "data/update.json";

function send404(response){
  response.writeHead(404, {"Content-Type": "application/json"});
  response.write(JSON.stringify({
    success: false,
    message: "Error 404, that file was not found within the server",
  }));
  response.end();
}

function send500(response, reason){
  reason = reason || "Generic Error";

  response.writeHead(500, {"Content-Type": "text/plain"});
  response.write(JSON.stringify({
    success: false,
    message: `Something went wrong on our end\nGiven reason: ${reason}`,
  }));
  response.end();
}

function sendHtml(reqPath, response){
  let desiredHtml = `${ROOT}${reqPath}.html`;
  if(reqPath === "/"){
    desiredHtml = `${ROOT}/index.html`;
  }

  fs.readFile(desiredHtml, (err, data) => {
    if(err){
      //console.error(err);
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
      //console.error(err);
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
      //console.error(err);
      send404(response);
      return;
    }

    response.writeHead(200, {"Content-Type": "application/javascript"});
    response.write(data);
    response.end();
  });
}

function generateUserToken(username){
  var hash = "7db938392c6a28";
  var tokenBuffer = [];

  for(var charIndex in username){
    var charValue = username.charCodeAt(charIndex);
    tokenBuffer.push(charValue ^ hash.charCodeAt(charIndex % hash.length));
  }
  var token = tokenBuffer.map((n) => {return n.toString(16);}).join('');

  return token;
}

function saveUserData(reqQuery, response){
  // note: for the actual CTF, the JSON file should already be populated. 
  // however, this will still create a blank the corresponding folder and JSON
  // file if needed
  const userAuthPath = `${ROOT}/${USER_JSON_PATH}`;
  const userFolderPath = userAuthPath.split('/').slice(0, -1).join('/');

  try{
    if(!fs.existsSync(userFolderPath)){
      fs.mkdirSync(userFolderPath);
    }

    if(!fs.existsSync(userAuthPath)){
      fs.writeFileSync(userAuthPath,
        "{}",
        {
          encoding: "utf8",
          flag: "w+",
          mode: 0o666,
        }
      );

      response.writeHead(201, {"Context-Type": "application/javascript"});
      response.write(JSON.stringify({success: true}));
      response.end();
    }
  }catch(err){
    //console.error("Error initializing the user auth, this should not occur", err);
    send500(response);
    return;
  }

  try{
    let userJson = fs.readFileSync(userAuthPath, "utf8");
    let userData = JSON.parse(userJson);

    // generate a random userToken for the given user to anonymize user access
    let userToken = generateUserToken(reqQuery.username);

    if(Object.keys(userData).includes(userToken)){
      response.writeHead(403, {"Content-Type": "application/json"});
      response.write(JSON.stringify({
        success: false,
        message: "user already exists",
      }));
      response.end();
      return;
    }

    userData[userToken] = reqQuery;
    userJson = JSON.stringify(userData);

    fs.writeFileSync(userAuthPath,
      userJson,
      {
        encoding: "utf8",
        flag: "w+",
        mode: 0o666,
      }
    );
  }catch(err){
    //console.error("Error handling user auth", err);
    send500(response);
    return;
  }

  // Send automated emails
  fs.readFile(`${ROOT}/${WELCOME_PATH}`, (err, data) => {
    if(err){
      send500(response, `Error reading automated welcome email ${err}`);
      return;
    }

    let welcomeEmail = JSON.parse(data);

    autoSendEmail(reqQuery.username,
      welcomeEmail.from,
      welcomeEmail.subject,
      welcomeEmail.message);
    });

  fs.readFile(`${ROOT}/${UPDATE_PATH}`, (err, data) => {
    if(err){
      send500(response, `Error reading automated update email ${err}`);
      return;
    }

    updateEmail = JSON.parse(data);

    autoSendEmail(reqQuery.username,
      updateEmail.from,
      updateEmail.subject,
      updateEmail.message);
  });

  // detect returned errors
  if(response.statusCode == 500) return;

  response.writeHead(201, {"Content-Type": "applicaton/json"});
  response.write(JSON.stringify({
    success: true,
    message: "",
  }));
  response.end();
}

/**
 * Attempts to link a token to a given username.
 *
 * Recieves a token from the request's query, as followed:
 *  - token : the user's token
 *
 * responds with:
 *  - success : a boolean stating if the request was successful
 *  - uid : the username associated to the user, if available
 */
function linkToken(reqQuery, response){
  try{
    const userAuthPath = `${ROOT}/${USER_JSON_PATH}`;

    if(!fs.existsSync(userAuthPath)){
      response.writeHead(404, {"Content-Type": "application/json"});
      response.write(JSON.stringify({
        success: false,
        uid: "",
      }));
      response.end();
      return;
    }

    let userJSON = fs.readFileSync(userAuthPath);
    let userData = JSON.parse(userJSON);

    if(!Object.keys(userData).includes(reqQuery.token)){
      response.writeHead(403, {"Content-Type": "application/json"});
      response.write(JSON.stringify({
        success: false,
        uid: "",
      }));
    }

    response.writeHead(201, {"Content-Type": "application/json"});
    response.write(JSON.stringify({
      success: true,
      uid: userData[reqQuery.token].username,
    }));
    response.end();
  }catch(err){
    // console.log(err);
    send500("Error linking token to username", err);
    return;
  }
}

function getUserDate(reqQuery, response){
  const userAuthPath = `${ROOT}/${USER_JSON_PATH}`;

  try{
    if(!fs.existsSync(userAuthPath)){
      response.writeHead(403, {"Content-Type": "application/json"});
      response.write(JSON.stringify({
        success: false,
        message: "User not found",
      }));
      return;
    }

    let userJson = fs.readFileSync(userAuthPath, "utf8");
    let userData = JSON.parse(userJson);

    let userToken = generateUserToken(reqQuery.username);

    if(!(userToken in userData)){
      response.writeHead(403, {"Content-Type": "text/plain"});
      response.write(JSON.stringify({
        success: false,
        time: -1
      }));
      response.end();
      return;
    }

    response.writeHead(201, {"Content-Type": "application/json"});
    response.write(JSON.stringify({
      success: true,
      time: userData[userToken].time
    }));
    response.end();
  }catch(err){
    //console.error("Error fetching creation date", err);
    send500(response);
    return;
  }
}

function checkUserData(reqQuery, response){
  const userAuthPath = `${ROOT}/${USER_JSON_PATH}`;

  try{
    if(!fs.existsSync(userAuthPath)){
      send500(response);
      return;
    }

    let userToken = generateUserToken(reqQuery.username);

    let userJson = fs.readFileSync(userAuthPath, "utf8");
    let userData = JSON.parse(userJson);
    if(userData[userToken].salt !== reqQuery.salt){
      response.writeHead(403, {"Content-Type": "application/json"});
        response.write(JSON.stringify({
          success: false,
          auth: -1
        }));
      response.end();
      return;
    }

    response.writeHead(201, {"Content-Type": "application/json"});
    response.write(JSON.stringify({
      success: true,
      auth: userToken,
    }));
    response.end();
  }catch(err){
    //console.error("Error reading user auth file", err);
    send500(response);
    return;
  }
}

function getFiletype(request){
  if(request.url.indexOf('.') === -1){
    return "";
  }

  return request.url.split('.').slice(-1)[0];
}

/**
 * gets the emails that a specified user has.
 *
 * The user to get the emails of is specified in the query of the URL.
 *
 * As such, the request query must have the given parameter:
 *  - uid : The full email address of the server to read emails from
 *
 * this will respond with a body containing:
 *  - success : an indication that the request was successful
 *  - messages : Information of the messages the user has
 *     - count : the total number of messages the user has
 *     - ids : the ids of each message associated with more info
 *       - subject : the subject of the email
 *       - sender : the person who sent the email
 *
 * If no emails are found, the server *should* return a 201 response to specify
 * no emails were found, but as emails cannot be deleted, then it will be used
 * to autosend an email from the company's IT department (it@email.com)
 *
 * This will then allow pivoting/escilation (technically?) from the user's email
 * address to the IT department.
 */
function getEmails(reqQuery, response){
  try{
    let recipientName = reqQuery.uid.split('@')[0];
    let path = `${ROOT}/${EMAIL_ROOT_PATH}/${recipientName}/emails.json`;

    if(!fs.existsSync(path)){ // here for sanity, but also to ensure it email is sent
      // TODO: replace this with an "autosender" from the IT team
      /*/
      response.writeHead(201, {"Content-Type": "application/json"});
      response.write(JSON.stringify({
        success: true,
        messages: {
          count: 0,
          ids: {}
        },
      }));
      response.end();
      return;
      // */
    }

    let messageJSON = fs.readFileSync(path);
    let messageData = JSON.parse(messageJSON);

    let messages = {
      count: messageData.count,
      ids: {},
    };

    for(var messageId in messageData.ids){
      var subject = messageData.ids[messageId].subject;
      var sender = messageData.ids[messageId].from;

      messages.ids[messageId] = {
        subject,
        sender,
      }
    }

    response.writeHead(201, {"Content-Type": "application/json"});
    response.write(JSON.stringify({
      success: true,
      messages,
    }));
    response.end();
  }catch(err){
    // console.log("Failed to fetch emails", err);
    send500(response);
    return;
  }
}

/**
 * Reads a given email from a recipient and with a specific id
 * This will use specific query parameters:
 *  - uid : the email address of the recipient of the email.
 *  - mid : the id of the message to read
 *
 * the response will contain information on
 *  - subject : subject line of the email
 *  - sender : who sent the email
 *  - date : when the email was sent, in epoch time
 *  - message : the message body itself
 */
function readEmail(reqQuery, response){
  try{
    let recipientName = reqQuery.uid.split('@')[0];
    let path = `${ROOT}/${EMAIL_ROOT_PATH}/${recipientName}/emails.json`;

    if(!fs.existsSync(path)){
      response.writeHead(201, {"Content-Type": "application/json"});
      response.write(JSON.stringify({
        success: false,
        date: -1,
        message: "",
        sender: "",
        subject: "",
      }));
      response.end();
      return;
    }

    let messageJSON = fs.readFileSync(path, "utf8");
    let messageData = JSON.parse(messageJSON);

    // Check if message id is found, if not, fail
    if(!Object.keys(messageData.ids).includes(reqQuery.mid)){
      response.writeHead(201, {"Content-Type": "application/json"});
      response.write(JSON.stringify({
        success: false,
        date: -1,
        message: "",
        sender: "",
        subject: "",
      }));
      response.end();
      return;
    }

    let focusMessage = messageData.ids[reqQuery.mid];

    response.writeHead(201, {"Content-Type": "application/json"});
    response.write(JSON.stringify({
      success: true,
      date: focusMessage.date,
      message: focusMessage.message,
      sender: focusMessage.from,
      subject: focusMessage.subject,
    }));
    response.end();
  }catch(err){
    // console.log("Error reading email:", err);
    send500(response);
    return;
  }
}

/** this will be for internal use only. 
 * To send an email, the recipient will be required to send a request with the
 * parameters:
 *  - to : the email address that will recieve the address
 *  - from : the email address the email is being sent from
 *  - date : the date the email was sent, in epoch notation
 *  - subject : the subject of the email
 * the message the email contains should then be found within the request body.
 * returns nothing, sends back HTTP statuses as necessary
 */
function sendEmail(reqQuery, reqBody, response){
  try{
    let recipientName = reqQuery.to.split('@')[0];
    let path = `${ROOT}/${EMAIL_ROOT_PATH}/${recipientName}/emails.json`;
    let folderPath = path.split('/').slice(0,-1).join('/');

    if(!fs.existsSync(path)){
    fs.mkdirSync(folderPath, {recursive: true});
    fs.writeFileSync(path,
      JSON.stringify({count: 0, ids:{}}),
      {
        encoding: "utf8",
        flag: "w+",
        mode: 0o666,
      },
    );
    }

    let emailJson = fs.readFileSync(path, "utf8");
    let emailData = JSON.parse(emailJson);

    let newEmail = {
      date: reqQuery.date,
      from: reqQuery.from,
      message: reqBody,
      subject: reqQuery.subject? reqQuery.subject : "[no subject]",
      to: reqQuery.to,
    }

    let emailId = crypto.createHash("sha256").update(`${recipientName}${emailData.count}${reqQuery.date}`)
      .digest("hex");

    emailData.ids[emailId] = newEmail;
    emailData.count++;

    fs.writeFileSync(path,
      JSON.stringify(emailData),
      {
        encoding: "utf8",
        flag: "w+",
        mode: 0o666,
      },
    )

    response.writeHead(200, {"Content-Type": "application/json"});
    response.write(JSON.stringify({
      success: true,
    }));
    response.end();
  }catch(err){
    // console.log("Error sending an email", err);
    send500(response);
    return;
  }
}

/**
 * Sends automated emails to given recipient from a specified address.
 *
 * this one is *really* internal, should have no outward-facing elements
 */
function autoSendEmail(to, from, subject, body){
  try{
    let currDate = new Date().getTime();

    let recipientName = to.split('@')[0];
    let path = `${ROOT}/${EMAIL_ROOT_PATH}/${recipientName}/emails.json`;
    let folderPath = path.split('/').slice(0,-1).join('/');

    if(!fs.existsSync(path)){
    fs.mkdirSync(folderPath, {recursive: true});
    fs.writeFileSync(path,
      JSON.stringify({count: 0, ids:{}}),
      {
        encoding: "utf8",
        flag: "w+",
        mode: 0o666,
      },
    );
    }

    let emailJson = fs.readFileSync(path, "utf8");
    let emailData = JSON.parse(emailJson);

    let newEmail = {
      date: currDate,
      from: from,
      message: body,
      subject: subject? subject : "[no subject]",
      to: to,
    }

    let emailId = Buffer.from(`${recipientName}${emailData.count}${currDate}`)
      .toString("base64");

    emailData.ids[emailId] = newEmail;
    emailData.count++;

    fs.writeFileSync(path,
      JSON.stringify(emailData),
      {
        encoding: "utf8",
        flag: "w+",
        mode: 0o666,
      },
    )
  }catch(err){
    // console.log("Error sending an email", err);
    return;
  }
}

function writeLog(request, urlInfo, reqBody, response){
  let logPath = `${ROOT}/${LOG_FILE_PATH}`;
  let curDate = new Date().toISOString();

  let logLine = `\n[${curDate}] ${request.method} request to ${urlInfo.href} - ${response.statusCode}`;

  if(reqBody) logLine.concat(`\n└──${reqBody}`);

  process.stdout.write(logLine);
  fs.writeFileSync(logPath,
    logLine, {
    encode: "utf8",
    flag: "a+",
    mode: 0o644,
  });
}

function onRequest(request, response){
  let urlInfo = url.parse(request.url, true);
  let reqPath = urlInfo.pathname;
  let reqQuery = urlInfo.query;
  let reqBody = "";

  request.on("data", (chunk) => {
    reqBody += chunk;
  });

  request.on("end", () => {
    if(request.method === "GET"){
      switch(reqPath){
        case("/"):
        case("/email"):
        case("/register"):
        case("/index"):
        /*/ Disable email sending for challenge
        case("/compose"):
        // */
        case("/read"):
          sendHtml(reqPath, response);
          break;
        case("/css/styles.css"):
        case("/css/index.css"):
        /*/ Disable email sending for challenge
        case("/css/compose.css"):
        // */
        case("/css/email.css"):
          sendCss(reqPath, response);
          break;
        case("/js/index.js"):
        case("/js/register.js"):
        case("/js/email.js"):
        /*/ Disable email sending for challenge
        case("/js/compose.js"):
        // */
        case("/js/read.js"):
          sendJavascript(reqPath, response);
          break;
        default:
          send404(response);
      }
      return;
    }

    if(request.method === "POST"){
      switch(reqPath){
        case("/api/v0/link"):
          linkToken(reqQuery, response);
          break;
        case("/api/v0/getdate"):
          getUserDate(reqQuery, response);
          break;
        case("/api/v0/login"):
          checkUserData(reqQuery, response);
          break;
        case("/api/v0/register"):
          saveUserData(reqQuery, response);
          break;
        /*/ Disable email sending for challenge
        case("/api/v0/sendmessage"):
          sendEmail(reqQuery, reqBody, response);
          break;
        // */
        case("/api/v0/listemails"):
          getEmails(reqQuery, response);
          break;
        case("/api/v0/reademail"):
          readEmail(reqQuery, response);
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
// console.log(`Server started on ${PORT}`);
