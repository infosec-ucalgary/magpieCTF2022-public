import express from "express"
import cors from "cors"

let app = express()

// My "database"
// { token: token, items: [ { id: 1 }, { id: 2 }, etc... ] }
// Keep track of what clients found which objects
let db = [];

const fullList = [
    { type: "card", id: "1" },
    { type: "card", id: "2" },
    { type: "card", id: "3" },
    { type: "card", id: "4" },
    { type: "card", id: "5" },
    { type: "card", id: "6" },
    { type: "doc", id: "1" },
    { type: "doc", id: "2" },
    { type: "doc", id: "3" },
    { type: "doc", id: "4" },
    { type: "rec", id: "1" },
    { type: "rec", id: "2" }
]

function hasItem(list, item) {
    return list.filter((entry) => {
        entry.type === item.type && entry.id === item.id
    }).length > 0
}

let corsOptions = {
	origin: 'http://srv2.momandpopsflags.ca:8081'
}

app.use(cors(corsOptions))
app.use('/static', express.static('images'))

app.use('/found', (req, res) => {
    let found
    db.forEach((entry) => {
        if (entry.token === req.query.token) found = entry
    })

    if (found !== null && found !== undefined) {
        let inventory = []
        found.items.forEach((item) => {
            inventory.push({ url: `/static/${item.type}_${item.id}.jpg` })
        })
        return res.send({ inventory: inventory, found: inventory.length })
    } else {
        return res.send({ err: "You haven't found anything before." })
    }
})

app.get("/find", (req, res) => {
    // Check if token in db, then decide what to send them
    let found
    db.forEach((entry) => {
        if (entry.token === req.query.token) found = entry
    })

    let alreadySent = []; // Pics sent already to token user

    if (found !== null && found !== undefined) { // If they were found, get what items they had already been sent.
        alreadySent = found.items
    } else { // Else register the new user
        found = { token: req.query.token, items: [] }
        db.push(found)
    }

    let err = false
    let notSent = [];

    fullList.forEach((item) => {
        let has = false
        found.items.forEach((owned) => {
            if (item.type === owned.type && item.id === owned.id) {
                has = true
            }
        })

        if (!has) notSent.push(item)
    });

    if (notSent.length === 0) err = true

    if (err) {
        return res.send({ err: 'Everything useful has been found.' })
    }

    console.log(`Things not sent to ${found.token}:  ${JSON.stringify(notSent)}`)

    let item = Math.floor(Math.random() * notSent.length)


    found.items.push({ type: notSent[item].type, id: notSent[item].id })
    console.log(found)
    db.forEach((entry) => {
        if (entry.token === found.token) entry.items = found.items
    })
	return res.send({ url: `/static/${notSent[item].type}_${notSent[item].id}.jpg`, found: found.items.length })
})

app.get("/flag", (req, res) => {
	return res.send("magpie{this_is_not_it}")
})

app.listen(3000, () => console.log("Listening on port 3000..."))
