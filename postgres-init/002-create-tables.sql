-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table
CREATE TABLE users (
                       id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                       username VARCHAR(255) NOT NULL UNIQUE,
                       email VARCHAR(255) NOT NULL UNIQUE,
                       created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
                       updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);

-- Tags table
CREATE TABLE tags (
                      id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                      name VARCHAR(100) NOT NULL UNIQUE,
                      description TEXT,
                      created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
                      updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_tags_name ON tags(name);

-- Assets table
CREATE TABLE assets (
                        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                        name VARCHAR(255) NOT NULL,
                        asset_type VARCHAR(100),
                        status VARCHAR(50) NOT NULL DEFAULT 'active',
                        metadata JSONB DEFAULT '{}',
                        created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_assets_name ON assets(name);
CREATE INDEX idx_assets_status ON assets(status);
CREATE INDEX idx_assets_type ON assets(asset_type);
CREATE INDEX idx_assets_metadata ON assets USING gin(metadata);

-- Events table
CREATE TABLE events (
                        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                        asset_id UUID NOT NULL REFERENCES assets(id) ON DELETE CASCADE,
                        event_type VARCHAR(100) NOT NULL,
                        severity VARCHAR(50) NOT NULL,
                        description TEXT,
                        metadata JSONB DEFAULT '{}',
                        created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_events_asset_id ON events(asset_id);
CREATE INDEX idx_events_type ON events(event_type);
CREATE INDEX idx_events_severity ON events(severity);
CREATE INDEX idx_events_created_at ON events(created_at DESC);
CREATE INDEX idx_events_metadata ON events USING gin(metadata);

-- Event occurrences table
CREATE TABLE event_occurrences (
                                   id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                                   event_id UUID NOT NULL REFERENCES events(id) ON DELETE CASCADE,
                                   occurred_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
                                   details JSONB DEFAULT '{}',
                                   status VARCHAR(50) NOT NULL DEFAULT 'new',
                                   created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
                                   updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_event_occurrences_event_id ON event_occurrences(event_id);
CREATE INDEX idx_event_occurrences_occurred_at ON event_occurrences(occurred_at DESC);
CREATE INDEX idx_event_occurrences_status ON event_occurrences(status);
CREATE INDEX idx_event_occurrences_details ON event_occurrences USING gin(details);

-- Incidents table
CREATE TABLE incidents (
                           id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                           asset_id UUID NOT NULL REFERENCES assets(id) ON DELETE CASCADE,
                           incident_type VARCHAR(100) NOT NULL,
                           severity VARCHAR(50) NOT NULL,
                           priority VARCHAR(50) NOT NULL DEFAULT 'medium',
                           title VARCHAR(500) NOT NULL,
                           description TEXT,
                           status VARCHAR(50) NOT NULL DEFAULT 'open',
                           metadata JSONB DEFAULT '{}',
                           created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
                           updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
                           resolved_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_incidents_asset_id ON incidents(asset_id);
CREATE INDEX idx_incidents_type ON incidents(incident_type);
CREATE INDEX idx_incidents_severity ON incidents(severity);
CREATE INDEX idx_incidents_priority ON incidents(priority);
CREATE INDEX idx_incidents_status ON incidents(status);
CREATE INDEX idx_incidents_created_at ON incidents(created_at DESC);
CREATE INDEX idx_incidents_metadata ON incidents USING gin(metadata);

-- Incident occurrences table
CREATE TABLE incident_occurrences (
                                      id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                                      incident_id UUID NOT NULL REFERENCES incidents(id) ON DELETE CASCADE,
                                      occurred_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
                                      details JSONB DEFAULT '{}',
                                      status VARCHAR(50) NOT NULL DEFAULT 'reported',
                                      created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
                                      updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_incident_occurrences_incident_id ON incident_occurrences(incident_id);
CREATE INDEX idx_incident_occurrences_occurred_at ON incident_occurrences(occurred_at DESC);
CREATE INDEX idx_incident_occurrences_status ON incident_occurrences(status);
CREATE INDEX idx_incident_occurrences_details ON incident_occurrences USING gin(details);

-- Junction table: user_assets (many-to-many)
CREATE TABLE user_assets (
                             user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                             asset_id UUID NOT NULL REFERENCES assets(id) ON DELETE CASCADE,
                             role VARCHAR(50) NOT NULL DEFAULT 'viewer',
                             assigned_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
                             PRIMARY KEY (user_id, asset_id)
);

CREATE INDEX idx_user_assets_user_id ON user_assets(user_id);
CREATE INDEX idx_user_assets_asset_id ON user_assets(asset_id);
CREATE INDEX idx_user_assets_role ON user_assets(role);

-- Junction table: asset_tags (many-to-many)
CREATE TABLE asset_tags (
                            asset_id UUID NOT NULL REFERENCES assets(id) ON DELETE CASCADE,
                            tag_id UUID NOT NULL REFERENCES tags(id) ON DELETE CASCADE,
                            tagged_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
                            PRIMARY KEY (asset_id, tag_id)
);

CREATE INDEX idx_asset_tags_asset_id ON asset_tags(asset_id);
CREATE INDEX idx_asset_tags_tag_id ON asset_tags(tag_id);

-- Update trigger function for updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
    RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply update triggers to all tables with updated_at
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_tags_updated_at BEFORE UPDATE ON tags
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_assets_updated_at BEFORE UPDATE ON assets
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_events_updated_at BEFORE UPDATE ON events
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_event_occurrences_updated_at BEFORE UPDATE ON event_occurrences
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_incidents_updated_at BEFORE UPDATE ON incidents
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_incident_occurrences_updated_at BEFORE UPDATE ON incident_occurrences
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();