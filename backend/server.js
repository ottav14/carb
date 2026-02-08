const express = require('express');
const Database = require("better-sqlite3");
const cors = require('cors');
const path = require("path");

const app = express();
const PORT = 3000;

app.use(express.json());
app.use(cors());

const dbPath = path.join(__dirname, "db/crypto.db");
const db = new Database(dbPath);

app.get("/api/tickers", (req, res) => {
	const data = db.prepare("SELECT * FROM tickers").all();
	res.json(data);
});

app.get("/api/data/:id", (req, res) => {
	const id = req.params.id;
	const data = db.prepare(`SELECT * FROM data WHERE ticker_id = ${id} ORDER BY timestamp ASC`).all();
	res.json(data);
});

app.get("/api/id/:ticker", (req, res) => {
	const ticker = req.params.ticker;
	const data = db.prepare(`SELECT * FROM tickers WHERE ticker = '${ticker}'`).all();
	res.json(data);
});

app.listen(PORT, () => {
	console.log(`Express running on http://localhost:${PORT}`);
});

