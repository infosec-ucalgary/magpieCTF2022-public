# Scattered Letters
### Category: Networks
### Author: e-seng (Petiole#4224)

## Description
Monitoring the traffic from Mom and Pops computer, we have noticed that they visit
this one website in particular. It seems to be an email server, but it is certainly
not one that we are familiar with. Is there anything interesting that you can find
here?

## Hints
1. How does the server fetch the emails for your account?
2. What information does an email give? There's certainly more to an email than
   a subject and a message body.
3. Who else has an email on the server?

## Solution
1. Create an account within the system
2. Login with the account that was created.
  - This shows the emails that were sent to the account.
  - There are some emails that are automatically sent when an account is made.
  - When logging in, a request is made to get all emails the account has received.
  - The list of emails provides information on an email's subject, identification
    number and sender email.
  - Automated emails are sent from `it@mompopsflags.com`
3. Monitor the network traffic from website.
  - Using developer tools of a modern browser, like FireFox or Chrome, the Network
    tab may be used.
4. Identify requests made to get email information.
  - Email details (date sent, message body, message subject, message sender) may
    be fetched from making a request to `/api/v0/reademail` with a specific query.
    - Queries require:
      - `uid`: An identifier for the current user
      - `mid`: An identifier for the email to read
  - Emails a user has (All emails a user has received) may be fetched from making
    a request to `/api/v0/listemails`.
    - Queries require:
      - `uid`: An identifier for the current user.
5. Fetch emails from another user.
  - Knowing another email address, `uid` may be set without concern.
  - Making a request to `/api/v0/listemails?uid=it@mompopsflags.com` will retrieve
    the emails that the it account has.
6. Identify another user to read the emails from.
  - Another email is sent from `admin@mompopsflags.com`
7. Read emails from administration
  - Another request to `/api/v0/listemails?uid=admin@mompopsflags.com` fetches the
    emails administration has recieved.
  - Looking at the emails the account has received, there is one from
    `friends@omniflag.net` titled "[Urgent] New Flag Shipment".
8. Read email of note
  - Making a call to
    `/api/v0/reademail?uid=admin@mompopsflags.com&mid=YWRtaW4xMTYzOTc5ODIyNTYyNw==`
    gives details about that email, some cool story and the flag.

## Flag
`magpie{@u+h0r1z@+10n_2_l@x}`
