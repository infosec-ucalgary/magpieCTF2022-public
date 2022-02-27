# Mission Impossible
### Category: Misc
### Author: Alexandra Tenney (alexxxii), James Lowther (Articuler)

## Description

Have you seen Mom and Pop's new security system for their flags? Here is one of the surviellence streams: <link> Its got lasers... Mission Impossible style! I wonder if we could manage to turn those lasers off to get to that flag...

I found an API that looks like it's for Mom and Pop's backend system-control management API. Here is the link to the docs: http://<ip>:5000/api/docs. I was also able to find the code running on their servers.

## Hints
1. String Format
2. Maybe I should try that POST request

## Solution

1. We get access to an API documentation page, as well as the subsequent code. We should notice two things:
    1. The GET endpoint /api/v1/employees/format is listed as EXPERIMENTAL
    2. In the comments, the function that controls that endpoint has the following comment
        ```
        # !!! EXPERIMENTAL !!!
        #
        # This API endpoint is functional but it has not been audited by our security team.
        # While it is functional, we can not guarentee there are no vulnerabilities.
        ```
2. That specific function uses str.format(), which is a known vulnerable function that allows access to Global Variables.
    1. Lines 13-15 of the code contains a call to a Global Variable, declared in a different environment file. We can still access this variable through the string format vulnerability.
    2. To get the API key: `http://{HOST}:{PORT}/api/v1/employees/format?template={person.__init__.__globals__[CONFIG][API_KEY]}`
3. The endpoint /api/v1/security-controls/shutdown is the obvious endpoint we want to hit to shutdown the lasers, it even has documentation on how to turn them off. But making a post request without the API key returns a not verified response! Now that we have the API key, we can make the proper request to turn off all four lasers.
    1. ```sh
        curl -X POST \
            -H 'X-API-Key: W8ptasW9wtjjLKQsZGZ2jkLtNzA' \
            -H 'Content-Type: application/json' \
            -d '{"lasers": ["laser0", "laser1", "laser2", "laser3"]}' \
            http://{HOST}:{PORT}/api/v1/security-controls/shutdown
        ```

## Flag
magpie{ju5t_w0rm_4r0und_th3_la53r5}
