import initSqlJs from "sql.js";
import fs from "fs";

const DB_PATH = "notifications.db";

let db: any;

async function getDb() {
  if (db) return db;
  const SQL = await initSqlJs();
  if (fs.existsSync(DB_PATH)) {
    const fileBuffer = fs.readFileSync(DB_PATH);
    db = new SQL.Database(fileBuffer);
  } else {
    db = new SQL.Database();
  }
  db.run(`
    CREATE TABLE IF NOT EXISTS notifications (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      user_id TEXT NOT NULL,
      message TEXT NOT NULL,
      received_at TEXT NOT NULL DEFAULT (datetime('now'))
    )
  `);
  return db;
}

export default getDb;