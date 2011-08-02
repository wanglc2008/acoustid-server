ALTER TABLE account ADD CONSTRAINT account_pkey PRIMARY KEY (id);
ALTER TABLE account_openid ADD CONSTRAINT account_openid_pkey PRIMARY KEY (openid);
ALTER TABLE application ADD CONSTRAINT application_pkey PRIMARY KEY (id);
ALTER TABLE source ADD CONSTRAINT source_pkey PRIMARY KEY (id);
ALTER TABLE format ADD CONSTRAINT format_pkey PRIMARY KEY (id);
ALTER TABLE fingerprint ADD CONSTRAINT fingerprint_pkey PRIMARY KEY (id);
ALTER TABLE track ADD CONSTRAINT track_pkey PRIMARY KEY (id);
ALTER TABLE track_mbid ADD CONSTRAINT track_mbid_pkey PRIMARY KEY (id);
ALTER TABLE track_mbid_source ADD CONSTRAINT track_mbid_source_pkey PRIMARY KEY (id);
ALTER TABLE track_puid ADD CONSTRAINT track_puid_pkey PRIMARY KEY (id);
ALTER TABLE track_puid_source ADD CONSTRAINT track_puid_source_pkey PRIMARY KEY (id);
ALTER TABLE track_meta ADD CONSTRAINT track_meta_pkey PRIMARY KEY (id);
ALTER TABLE track_meta_source ADD CONSTRAINT track_meta_source_pkey PRIMARY KEY (id);
ALTER TABLE submission ADD CONSTRAINT submission_pkey PRIMARY KEY (id);
ALTER TABLE stats ADD CONSTRAINT stats_pkey PRIMARY KEY (id);
ALTER TABLE stats_top_accounts ADD CONSTRAINT stats_top_accounts_pkey PRIMARY KEY (id);
ALTER TABLE meta ADD CONSTRAINT meta_pkey PRIMARY KEY (id);

