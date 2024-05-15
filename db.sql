CREATE TABLE "online_news" (
	"title"	TEXT,
	"news_published_at"	TEXT,
	"content"	TEXT,
	"url"	TEXT UNIQUE,
	"asal_berita"	TEXT,
	PRIMARY KEY("url")
);

CREATE TABLE "progress_online_news" (
	"id"	INTEGER NOT NULL,
	"name"	TEXT,
	"since_time"	NUMERIC,
	"progress_time"	NUMERIC,
	"until_time"	NUMERIC,
	PRIMARY KEY("id" AUTOINCREMENT)
);

INSERT INTO progress_online_news (name,since_time,progress_time,until_time) VALUES
	 ('Detik News',2023-10-01,2024-01-01,2023-12-31),
	 ('CNN News',2023-10-01,2024-01-01,2023-12-31),
	 ('Kompas News',2023-10-01,2024-01-01,2023-12-31);