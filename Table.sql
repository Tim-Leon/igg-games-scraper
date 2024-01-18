CREATE TABLE IF NOT EXISTS game_entry (
    Name TEXT,
    Uploader TEXT,
    Timestamp TEXT,
    ModifiedDate TEXT,
    Image TEXT,
    Download TEXT,
    Genre TEXT,
    Description TEXT
);
CREATE TABLE IF NOT EXISTS game_links (
    name TEXT,
    megaup_net TEXT,
    mega_nz TEXT,
    fichier1_com TEXT,
    gofile_io TEXT,
    anonFiles_com TEXT,
    rapidgator_net TEXT,
    uptobox_com TEXT,
    clicknupload_to TEXT,
    pixeldrain_com TEXT, 
    torrent TEXT,
    PRIMARY KEY (name)
);
CREATE TABLE IF NOT EXISTS fitgirl_links (
    1337x TEXT,
    RuTor TEXT,
    Tapochek_net TEXT,
    MultiUpload TEXT,
    ZippyShare TEXT,
    BayFiles TEXT,
    OneDrive TEXT
);
