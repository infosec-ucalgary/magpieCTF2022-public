package main


import (
	"fmt"
	"io"
	fs "main/fs"
	"net/http"
	"os"
	auth "main/auth"
)

const FILE_MARKER =
`






--------------------------------------------------------------------------------
-------------------------------- MagpieFS v1.2 ---------------------------------
--------------------------------------------------------------------------------



PLEASE NOTE: This is a fake agreement.

End-User License Agreement ("Agreement")
=

Last updated: February 03, 2022

Please read this End-User License Agreement carefully before clicking the "I
Agree" button, downloading or using MagpieFS.

Interpretation and Definitions
==============================

Interpretation
--------------

The words of which the initial letter is capitalized have meanings defined
under the following conditions. The following definitions shall have the same
meaning regardless of whether they appear in singular or in plural.

Definitions
-----------

For the purposes of this End-User License Agreement:

  * Agreement means this End-User License Agreement that forms the entire
    agreement between You and the Company regarding the use of the
    Application. This Agreement has been created with the help of the [EULA
    Generator](https://www.termsfeed.com/eula-generator/).

  * Application means the software program provided by the Company downloaded
    by You to a Device, named MagpieFS

  * Company (referred to as either "the Company", "We", "Us" or "Our" in this
    Agreement) refers to Mom and Pops Corporation, 13 Dead End Drive,
    Hamilton, ON.

  * Content refers to content such as text, images, or other information that
    can be posted, uploaded, linked to or otherwise made available by You,
    regardless of the form of that content.

  * Country refers to: Ontario, Canada

  * Device means any device that can access the Application such as a
    computer, a cellphone or a digital tablet.

  * Third-Party Services means any services or content (including data,
    information, applications and other products services) provided by a
    third-party that may be displayed, included or made available by the
    Application.

  * You means the individual accessing or using the Application or the
    company, or other legal entity on behalf of which such individual is
    accessing or using the Application, as applicable.


Acknowledgment
==============

By clicking the "I Agree" button, downloading or using the Application, You
are agreeing to be bound by the terms and conditions of this Agreement. If You
do not agree to the terms of this Agreement, do not click on the "I Agree"
button, do not download or do not use the Application.

This Agreement is a legal document between You and the Company and it governs
your use of the Application made available to You by the Company.

The Application is licensed, not sold, to You by the Company for use strictly
in accordance with the terms of this Agreement.

License
=======

Scope of License
----------------

The Company grants You a revocable, non-exclusive, non-transferable, limited
license to download, install and use the Application strictly in accordance
with the terms of this Agreement.

The license that is granted to You by the Company is solely for your personal,
non-commercial purposes strictly in accordance with the terms of this
Agreement.

Third-Party Services
====================

The Application may display, include or make available third-party content
(including data, information, applications and other products services) or provide links to third-party websites or services.

You acknowledge and agree that the Company shall not be responsible for any
Third-party Services, including their accuracy, completeness, timeliness,
validity, copyright compliance, legality, decency, quality or any other aspect
thereof. The Company does not assume and shall not have any liability or
responsibility to You or any other person or entity for any Third-party
Services.

You must comply with applicable Third parties' Terms of agreement when using
the Application. Third-party Services and links thereto are provided solely as
a convenience to You and You access and use them entirely at your own risk and
subject to such third parties' Terms and conditions.

Term and Termination
====================

This Agreement shall remain in effect until terminated by You or the Company.
The Company may, in its sole discretion, at any time and for any or no reason,
suspend or terminate this Agreement with or without prior notice.

This Agreement will terminate immediately, without prior notice from the
Company, in the event that you fail to comply with any provision of this
Agreement. You may also terminate this Agreement by deleting the Application
and all copies thereof from your Device or from your computer.

Upon termination of this Agreement, You shall cease all use of the Application
and delete all copies of the Application from your Device.

Termination of this Agreement will not limit any of the Company's rights or
remedies at law or in equity in case of breach by You (during the term of this
Agreement) of any of your obligations under the present Agreement.

No Warranties
=============

The Application is provided to You "AS IS" and "AS AVAILABLE" and with all
faults and defects without warranty of any kind. To the maximum extent
permitted under applicable law, the Company, on its own behalf and on behalf
of its affiliates and its and their respective licensors and service
providers, expressly disclaims all warranties, whether express, implied,
statutory or otherwise, with respect to the Application, including all implied
warranties of merchantability, fitness for a particular purpose, title and
non-infringement, and warranties that may arise out of course of dealing,
course of performance, usage or trade practice. Without limitation to the
foregoing, the Company provides no warranty or undertaking, and makes no
representation of any kind that the Application will meet your requirements,
achieve any intended results, be compatible or work with any other software,
applications, systems or services, operate without interruption, meet any
performance or reliability standards or be error free or that any errors or
defects can or will be corrected.

Without limiting the foregoing, neither the Company nor any of the company's
provider makes any representation or warranty of any kind, express or implied:
(i) as to the operation or availability of the Application, or the
information, content, and materials or products included thereon; (ii) that
the Application will be uninterrupted or error-free; (iii) as to the accuracy,
reliability, or currency of any information or content provided through the
Application; or (iv) that the Application, its servers, the content, or
e-mails sent from or on behalf of the Company are free of viruses, scripts,
trojan horses, worms, malware, timebombs or other harmful components.

Some jurisdictions do not allow the exclusion of certain types of warranties
or limitations on applicable statutory rights of a consumer, so some or all of
the above exclusions and limitations may not apply to You. But in such a case
the exclusions and limitations set forth in this section shall be applied to
the greatest extent enforceable under applicable law. To the extent any
warranty exists under law that cannot be disclaimed, the Company shall be
solely responsible for such warranty.

Severability and Waiver
=======================

Severability
------------

If any provision of this Agreement is held to be unenforceable or invalid,
such provision will be changed and interpreted to accomplish the objectives of
such provision to the greatest extent possible under applicable law and the
remaining provisions will continue in full force and effect.

Waiver
------

Except as provided herein, the failure to exercise a right or to require
performance of an obligation under this Agreement shall not effect a party's
ability to exercise such right or require such performance at any time
thereafter nor shall the waiver of a breach constitute a waiver of any
subsequent breach.

Entire Agreement
================

The Agreement constitutes the entire agreement between You and the Company
regarding your use of the Application and supersedes all prior and
contemporaneous written or oral agreements between You and the Company.

You may be subject to additional terms and conditions that apply when You use
or purchase other Company's services, which the Company will provide to You at
the time of such use or purchase.

Contact Us
==========

If you have any questions about this Agreement, You can contact Us:

  * By email: thisisntpartofthechallenge@momandpopsflags.ca


PLEASE NOTE: In all seriousness, this EULA is not binding, its just a joke, nor is it a part of the challenge
`
const VERSION = "MagpieFS v1.2"

type wrapperW struct {
	http.ResponseWriter
}

func (w *wrapperW) ReadFrom(src io.Reader) (int64, error) {
	// if its a file, add the file marker length to its size
	if lr, ok := src.(*io.LimitedReader); ok {
		lr.N += int64(len(FILE_MARKER))
	}

	if w, ok := w.ResponseWriter.(interface{ ReadFrom(src io.Reader) (int64, error) }); ok {
		return w.ReadFrom(src)
	}

	panic("unreachable")
}

func main() {
	var path string
	if len(os.Args) < 2 {
		fmt.Println("Defaulting to serving current directory. Use ./fs <path> to serve different")
		path, _ = os.Getwd()
	} else {
		path = os.Args[1]
	}

	fileServ := http.FileServer(fs.CreateFileServFS(
		path,
		// Modify all responses by adding the file marker to them
		// we also need to adjust the file size in the ReadFrom because of to that...
		func(in []byte) (out []byte) {
			out = append(in, FILE_MARKER...)
			return
		}))

	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Served-by", VERSION)
		w = &wrapperW{w}
		fileServ.ServeHTTP(w, r)
	})

	http.HandleFunc("/a_secret.bak", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Served-by", VERSION)
		w.Write([]byte(`Error: Access to secret key only for authorized users.`))
	})

	http.HandleFunc("/flag", func(w http.ResponseWriter, r *http.Request) {
		tokenLine := ""
		w.Header().Set("Served-by", VERSION)
		authHeader, ok := r.Header["Authorization"] // Requires auth
		if ok {
			username, err := auth.TrimAndParseToken([]byte(authHeader[0]))
			if err != nil {
				tokenLine = "An invalid token was given"
			} else {
				tokenLine = username
			}
		} else {
			tokenLine = "No token provided"
		}

		if tokenLine == "admin" { // Require the admin user
			fileServ.ServeHTTP(w, r)
		} else {
			w.Write([]byte(`Error: Access to the flag only for the user admin.  `))
			w.Write([]byte("("))
			w.Write([]byte(tokenLine))
			w.Write([]byte(")"))
		}
	})

    port := "8080"
    fmt.Println("Hosting on port", port)
	err := http.ListenAndServe("0.0.0.0:"+port, nil)
	fmt.Println(err)
}
