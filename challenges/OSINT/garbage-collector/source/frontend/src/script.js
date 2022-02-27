const UPDATE_RATE = 2000;
const SCREEN_W = 640;
const SCREEN_H = 480;
const GRID_CELL = 16;
const API_URL = "http://srv2.momandpopsflags.ca:3000";

let core;
let ctx;
let objects; // hold all positions and stuff
let garbageObjects;
let text;
let player;
let found;
let placed;
let lastUpdate;
let garbageSpawnTime;

let imageDiv = document.getElementById("imageDiv");

let structures = [
  { x: 23 * GRID_CELL, y: 2 * GRID_CELL, w: 15 * GRID_CELL, h: 8 * GRID_CELL, doors: ['s', 'w'], type: 'hut' },
  { x: 2 * GRID_CELL, y: 20 * GRID_CELL, w: 15 * GRID_CELL, h: 8 * GRID_CELL, doors: ['n', 'e'], type: 'hut' },
  { x: 34 * GRID_CELL, y: 14 * GRID_CELL, w: 4 * GRID_CELL, h: 4 * GRID_CELL, doors: ['w'], type: 'bin' },
  { x: 34 * GRID_CELL, y: 19 * GRID_CELL, w: 4 * GRID_CELL, h: 4 * GRID_CELL, doors: ['w'], type: 'bin' },
  { x: 34 * GRID_CELL, y: 24 * GRID_CELL, w: 4 * GRID_CELL, h: 4 * GRID_CELL, doors: ['w'], type: 'bin' },
  { x: 5 * GRID_CELL, y: 10 * GRID_CELL, w: 4 * GRID_CELL, h: 6 * GRID_CELL, doors: ['n', 's'], type: 'bin' },
];

function genToken() {
  var a = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890".split("");
  var b = [];
  for (var i = 0; i < 32; i++) {
    var j = (Math.random() * (a.length - 1)).toFixed(0);
    b[i] = a[j];
  }
  return b.join("");
}

function setTokenIfNull() {
  if (localStorage.getItem("token") === null) {
    localStorage.setItem("token", genToken())
  } else {
    axios.get(`${API_URL}/found?token=${localStorage.getItem("token")}`)
      .then((resp) => {
        if (resp.data.err) throw resp.data.err;
        let notfound = document.getElementById("no-found");
        if (notfound) notfound.remove();
        found = resp.data.found;
        resp.data.inventory.forEach((i) => {
          let img = document.createElement("img");
          img.src = `${API_URL}${i.url}`
          img.width = 200;
          img.className = "mx-auto";
          img.id = "drag-img"
          imageDiv.appendChild(img);
          dragElement(img);
        })
      }).catch((e) => {
        console.log(e)
      })
  }
}

function init() {
  core = document.getElementById("core");
  ctx = core.getContext("2d");
  player = { x: GRID_CELL, y: GRID_CELL, w: GRID_CELL, h: GRID_CELL, colour: '#00FF00' }
  objects = [];
  garbageObjects = [];
  found = 0;
  placed = 0;
  text = { font: `20px monospace`, text: "", x: 10, y: SCREEN_H + 25 };
  garbageSpawnTime = 5000;
  lastUpdate = Date.now();
  generateWalls();
  generateStructures();
  setTokenIfNull();
  window.requestAnimationFrame(loop);
}

function clearMap() {
  objects = [];
}

function generateWalls() {
  for (let y = 0; y <= SCREEN_H - GRID_CELL; y += GRID_CELL) {
    for (let x = 0; x <= SCREEN_W - GRID_CELL; x += GRID_CELL) {
      if (x === 0 || y === 0 || x === SCREEN_W - GRID_CELL || y === SCREEN_H - GRID_CELL) {
        objects.push({ x: x, y: y, w: GRID_CELL, h: GRID_CELL, colour: '#000000', type: 'wall' })
      } else {
        objects.push({ x: x, y: y, w: GRID_CELL, h: GRID_CELL, colour: '#BBBBBB', type: 'floor' })
      }
    }
  }
}

function generateStructures() {
  structures.forEach((struct) => {
    for (let x = struct.x + GRID_CELL; x < struct.x + struct.w - GRID_CELL; x += GRID_CELL) {
      for (let y = struct.y + GRID_CELL; y < struct.y + struct.h - GRID_CELL; y += GRID_CELL) {
        objects.push({ x: x, y: y, w: GRID_CELL, h: GRID_CELL, colour: '#DDDDDD', type: 'floor' })
      }
    }
    for (let y = struct.y; y < struct.y + struct.h; y += GRID_CELL) {
      for (let x = struct.x; x < struct.x + struct.w; x += GRID_CELL) {
        if (x === struct.x && !struct.doors.includes('w')) {
          objects.push({ x: x, y: y, w: GRID_CELL, h: GRID_CELL, colour: '#000000', type: 'wall' })
        } else if (y === struct.y && !struct.doors.includes('n')) {
          objects.push({ x: x, y: y, w: GRID_CELL, h: GRID_CELL, colour: '#000000', type: 'wall' })
        } else if (x === struct.x + struct.w - GRID_CELL && !struct.doors.includes('e')) {
          objects.push({ x: x, y: y, w: GRID_CELL, h: GRID_CELL, colour: '#000000', type: 'wall' })
        } else if (y === struct.y + struct.h - GRID_CELL && !struct.doors.includes('s')) {
          objects.push({ x: x, y: y, w: GRID_CELL, h: GRID_CELL, colour: '#000000', type: 'wall' })
        }
      }
    }
  })
}

function getObjectAtXY(x, y) {
  for (let i = 0; i < objects.length; i++) {
    if (objects[i].x === x && objects[i].y === y) return objects[i]
  }
  return { x: -1, y: -1, type: "null" }
}

function updateGarbage() {
  if (Date.now() >= lastUpdate + garbageSpawnTime && found + placed < 12) {
    let placeX = Math.floor(Math.random() * (SCREEN_W / GRID_CELL))
    let placeY = Math.floor(Math.random() * (SCREEN_H / GRID_CELL))
    let obj = getObjectAtXY(placeX * GRID_CELL, placeY * GRID_CELL)
    while (obj.type !== "floor" || hasGarbage(obj.x, obj.y)) {
      placeX = Math.floor(Math.random() * (SCREEN_W / GRID_CELL))
      placeY = Math.floor(Math.random() * (SCREEN_H / GRID_CELL))
      obj = getObjectAtXY(placeX * GRID_CELL, placeY * GRID_CELL)
    }
    let chance = Math.floor(Math.random() * 100) > 95;
    if (chance) {
      garbageObjects.push({ x: obj.x, y: obj.y, w: GRID_CELL, h: GRID_CELL, colour: '#FF0000', type: 'garbage' });
      placed = placed + 1;
      lastUpdate = Date.now();
    }
  }
}

function hasGarbage(x, y) {
  let garbage = garbageObjects.filter((obj) => {
    obj.x === x && obj.y === y
  });
  return garbage.length > 0;
}

function render() {
  console.log("Rendering");
  ctx.clearRect(0, 0, SCREEN_W, SCREEN_H);
  ctx.fillStyle = "#BBBBBB";
  ctx.fillRect(0, 0, SCREEN_W, SCREEN_H);
  objects.forEach(obj => {
    drawNode(obj);
  });
  garbageObjects.forEach(obj => {
    drawNode(obj);
  });
  if (found + placed < 12) updateGarbage();
  drawNode(player);
  drawUI();
  drawText(text);
}

function loop() {
  render();
  window.requestAnimationFrame(loop);
}

function drawNode(node) {
  ctx.fillStyle = node.colour;
  ctx.fillRect(node.x, node.y, node.w, node.h);
}

function drawText(node) {
  ctx.font = node.font;
  ctx.fillStyle = "#011110";
  ctx.fillText(node.text, node.x, node.y);
}

function drawUI() {
  ctx.fillStyle = "#928574";
  ctx.fillRect(0, 480, 640, 40);
  ctx.fillStyle = "#B6A590";
  ctx.fillRect(5, 485, 630, 30);
}

function handleInput(e) {
  let new_x = player.x;
  let new_y = player.y;
  if (e.code === "KeyW") { // w
    if (player.y > 0 && !hasCollision(player.x, player.y - GRID_CELL)) player = { ...player, y: player.y - GRID_CELL };
  } else if (e.code === "KeyS") { // s
    if (player.y < SCREEN_H - GRID_CELL && !hasCollision(player.x, player.y + GRID_CELL)) player = { ...player, y: player.y + GRID_CELL };
  }

  if (e.code === "KeyA") { // a
    if (player.x > 0 && !hasCollision(player.x - GRID_CELL, player.y)) player = { ...player, x: player.x - GRID_CELL };
  } else if (e.code === "KeyD") { // d
    if (player.x < SCREEN_W - GRID_CELL && !hasCollision(player.x + GRID_CELL, player.y)) player = { ...player, x: player.x + GRID_CELL };
  }

  if (e.code === "KeyE") {
    let gb = getClosestGarbage();
    if (gb === -1) return;
    else removeGarbageFromList(gb)
    axios.get(`${API_URL}/find?token=${localStorage.getItem('token')}`)
      .then((resp) => {
        if (resp.data.err) throw resp.data.err;
        let notfound = document.getElementById("no-found");
        if (notfound) notfound.remove();
        let img = document.createElement("img");
        img.src = `${API_URL}${resp.data.url}`
        img.width = 200;
        found = found + 1;
        if (resp.data.url.includes("doc_")) {
          img.width = 500
        }
        img.className = "mx-auto";
        img.id = "drag-img"
        imageDiv.appendChild(img);
        dragElement(img);
        text.text = "You found something!";
      })
      .catch((e) => {
        text.text = "You found nothing useful.";
        console.log(e);
      })
  }
}

function getClosestGarbage() {
  for (let i = 0; i < garbageObjects.length; i++) {
    if (garbageObjects[i].x === player.x && garbageObjects[i].y === player.y ||
        garbageObjects[i].x === player.x && garbageObjects[i].y === player.y - GRID_CELL ||
        garbageObjects[i].x === player.x && garbageObjects[i].y === player.y + GRID_CELL ||
        garbageObjects[i].x === player.x - GRID_CELL && garbageObjects[i].y === player.y ||
        garbageObjects[i].x === player.x + GRID_CELL && garbageObjects[i].y === player.y)
      return i
  }
  return -1
}

function removeGarbageFromList(i) {
  garbageObjects.splice(i, 1)
}

function hasCollision(x, y) {
  return objects.filter(obj => obj.x === x && obj.y === y && obj.type === "wall").length > 0
}

document.addEventListener('keydown', handleInput);
window.onload = init;
