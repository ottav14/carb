const express = require('express');
const Database = require("better-sqlite3");
const path = require("path");

const app = express();
const PORT = 3000;

app.use(express.json());

const dbPath = path.join(__dirname, "db/data.db");
const db = new Database(dbPath);

app.get("/api/tickers/:exchange", (req, res) => {
	const exchange = req.params.exchange;
	const data = db.prepare(`SELECT ticker FROM ${exchange}`).all();
	res.json(data);
});

app.get("/api/data/id/:id/:exchange", (req, res) => {
	const id = req.params.id;
	const exchange = req.params.exchange;
	const data = db.prepare(`SELECT * FROM ${exchange} WHERE id = ${id} ORDER BY timestamp ASC`).all();
	res.json(data);
});

app.get("/api/data/ticker/:ticker/:exchange", (req, res) => {
	const ticker = req.params.ticker;
	const exchange = req.params.exchange;
	const data = db.prepare(`SELECT * FROM ${exchange} WHERE ticker = '${ticker}'`).all();
	res.json(data);
});

app.listen(PORT, () => {
	console.log(`Express running on http://localhost:${PORT}`);
});

