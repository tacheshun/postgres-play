#!/usr/bin/env python3
"""
Database population script for Postgres slow query testing.
Generates realistic test data with proper relationships and distributions.
"""

import random
import uuid
from datetime import datetime, timedelta
from typing import List, Tuple
import psycopg
from psycopg.types.json import Json
from faker import Faker
import json
from tqdm import tqdm

# Initialize Faker
fake = Faker()

# Database configuration - psycopg3 uses 'dbname' not 'database'
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'dbname': 'testdb',  # Changed from 'database' to 'dbname'
    'user': 'dbuser',
    'password': 'dbpassword'
}

# Data volume configuration
CONFIG = {
    'users': 10,
    'assets': 150,
    'tags': 150,
    'events': 450,
    'incidents': 150,
    'event_occurrences': 100000,
    'incident_occurrences': 100000,
    'user_assets_per_user': random.randint(5, 15),
    'tags_per_asset': random.randint(2, 5)
}


class DataGenerator:
    """Generates test data for the security platform database."""

    def __init__(self, conn):
        self.conn = conn
        self.cur = conn.cursor()
        self.user_ids = []
        self.asset_ids = []
        self.tag_ids = []
        self.event_ids = []
        self.incident_ids = []

    def generate_users(self) -> List[Tuple]:
        """Generate user records."""
        users = []
        for _ in range(CONFIG['users']):
            user_id = str(uuid.uuid4())
            self.user_ids.append(user_id)
            users.append((
                user_id,
                fake.user_name(),
                fake.email(),
                datetime.now(),
                datetime.now()
            ))
        return users

    def generate_tags(self) -> List[Tuple]:
        """Generate tag records with realistic security categories."""
        tag_categories = [
            'critical', 'production', 'development', 'staging', 'database',
            'web-server', 'api-gateway', 'message-queue', 'cache', 'storage',
            'pci-compliant', 'gdpr-regulated', 'sox-compliant', 'public-facing',
            'internal', 'deprecated', 'legacy', 'cloud', 'on-premise', 'hybrid'
        ]

        tags = []
        for i in range(CONFIG['tags']):
            tag_id = str(uuid.uuid4())
            self.tag_ids.append(tag_id)

            if i < len(tag_categories):
                name = tag_categories[i]
            else:
                name = f"{fake.word()}-{fake.word()}-{random.randint(1, 999)}"

            tags.append((
                tag_id,
                name,
                fake.sentence(),
                datetime.now(),
                datetime.now()
            ))
        return tags

    def generate_assets(self) -> List[Tuple]:
        """Generate asset records with realistic types and metadata."""
        asset_types = ['server', 'database', 'application', 'network-device',
                       'container', 'kubernetes-pod', 'storage-bucket', 'api-endpoint']
        statuses = ['active', 'inactive', 'maintenance', 'decommissioned']

        assets = []
        for _ in range(CONFIG['assets']):
            asset_id = str(uuid.uuid4())
            self.asset_ids.append(asset_id)

            metadata = {
                'ip_address': fake.ipv4(),
                'hostname': fake.hostname(),
                'os': random.choice(['Linux', 'Windows', 'Unix', 'Container']),
                'version': f"{random.randint(1, 10)}.{random.randint(0, 20)}.{random.randint(0, 50)}",
                'environment': random.choice(['production', 'staging', 'development', 'test']),
                'criticality': random.choice(['low', 'medium', 'high', 'critical']),
                'owner_team': fake.company()
            }

            assets.append((
                asset_id,
                f"{fake.word()}-{fake.word()}-{random.randint(100, 999)}",
                random.choice(asset_types),
                random.choices(statuses, weights=[70, 15, 10, 5])[0],
                Json(metadata),
                datetime.now(),
                datetime.now()
            ))
        return assets

    def generate_events(self) -> List[Tuple]:
        """Generate event records with realistic security event types."""
        event_types = [
            'authentication_failure', 'authorization_violation', 'data_exfiltration',
            'malware_detected', 'vulnerability_scan', 'configuration_change',
            'suspicious_activity', 'brute_force_attempt', 'privilege_escalation',
            'anomaly_detected', 'policy_violation', 'compliance_check_failed'
        ]
        severities = ['low', 'medium', 'high', 'critical']

        events = []
        for _ in range(CONFIG['events']):
            event_id = str(uuid.uuid4())
            self.event_ids.append(event_id)

            event_type = random.choice(event_types)
            severity = random.choices(severities, weights=[30, 40, 25, 5])[0]

            metadata = {
                'source': fake.ipv4(),
                'destination': fake.ipv4(),
                'port': random.randint(1, 65535),
                'protocol': random.choice(['TCP', 'UDP', 'ICMP', 'HTTP', 'HTTPS']),
                'detection_method': random.choice(['signature', 'anomaly', 'heuristic', 'ml_model']),
                'confidence': random.randint(60, 100)
            }

            events.append((
                event_id,
                random.choice(self.asset_ids),
                event_type,
                severity,
                f"Detected {event_type.replace('_', ' ')} on asset",
                Json(metadata),
                datetime.now(),
                datetime.now()
            ))
        return events

    def generate_incidents(self) -> List[Tuple]:
        """Generate incident records with realistic security incidents."""
        incident_types = [
            'security_breach', 'data_leak', 'ransomware_attack', 'ddos_attack',
            'insider_threat', 'compliance_violation', 'unauthorized_access',
            'system_compromise', 'phishing_campaign', 'supply_chain_attack'
        ]
        severities = ['low', 'medium', 'high', 'critical']
        priorities = ['low', 'medium', 'high', 'urgent']
        statuses = ['open', 'investigating', 'contained', 'resolved', 'closed']

        incidents = []
        for i in range(CONFIG['incidents']):
            incident_id = str(uuid.uuid4())
            self.incident_ids.append(incident_id)

            incident_type = random.choice(incident_types)
            severity = random.choices(severities, weights=[20, 35, 35, 10])[0]
            priority = random.choices(priorities, weights=[20, 35, 35, 10])[0]
            status = random.choices(statuses, weights=[30, 25, 15, 20, 10])[0]

            metadata = {
                'affected_users': random.randint(1, 1000),
                'estimated_impact': random.choice(['low', 'medium', 'high', 'critical']),
                'attack_vector': random.choice(['network', 'email', 'web', 'physical', 'social']),
                'ioc_count': random.randint(0, 50),
                'assigned_to': fake.name()
            }

            created_at = datetime.now() - timedelta(days=random.randint(0, 365))
            resolved_at = None
            if status in ['resolved', 'closed']:
                resolved_at = created_at + timedelta(hours=random.randint(1, 168))

            incidents.append((
                incident_id,
                random.choice(self.asset_ids),
                incident_type,
                severity,
                priority,
                f"INC-{i + 1000}: {incident_type.replace('_', ' ').title()}",
                fake.text(max_nb_chars=200),
                status,
                Json(metadata),
                created_at,
                created_at,
                resolved_at
            ))
        return incidents

    def generate_event_occurrences(self, batch_size: int = 5000) -> None:
        """Generate event occurrence records in batches for performance."""
        print(f"Generating {CONFIG['event_occurrences']:,} event occurrences...")

        statuses = ['new', 'acknowledged', 'investigating', 'resolved', 'false_positive']
        total_batches = CONFIG['event_occurrences'] // batch_size

        # Generate all data first, then use COPY
        rows_processed = 0

        with self.cur.copy(
                """COPY event_occurrences 
                   (id, event_id, occurred_at, details, status, created_at, updated_at) 
                   FROM STDIN""") as copy:

            for batch_num in tqdm(range(total_batches), desc="Event occurrence batches"):
                for _ in range(batch_size):
                    event_id = random.choice(self.event_ids)
                    occurred_at = datetime.now() - timedelta(
                        days=random.randint(0, 90),
                        hours=random.randint(0, 23),
                        minutes=random.randint(0, 59)
                    )

                    details = json.dumps({
                        'batch': batch_num,
                        'correlation_id': str(uuid.uuid4()),
                        'raw_log': fake.text(max_nb_chars=100),
                        'matched_rules': random.randint(1, 5),
                        'score': random.uniform(0.5, 1.0)
                    })

                    copy.write_row((
                        str(uuid.uuid4()),
                        event_id,
                        occurred_at,
                        details,
                        random.choices(statuses, weights=[40, 25, 15, 15, 5])[0],
                        occurred_at,
                        occurred_at
                    ))
                    rows_processed += 1

        # Commit after COPY completes
        self.conn.commit()
        print(f"  Inserted {rows_processed:,} event occurrences")

    def generate_incident_occurrences(self, batch_size: int = 5000) -> None:
        """Generate incident occurrence records in batches for performance."""
        print(f"Generating {CONFIG['incident_occurrences']:,} incident occurrences...")

        statuses = ['reported', 'triaged', 'escalated', 'mitigated', 'resolved']
        total_batches = CONFIG['incident_occurrences'] // batch_size
        rows_processed = 0

        with self.cur.copy(
                """COPY incident_occurrences 
                   (id, incident_id, occurred_at, details, status, created_at, updated_at) 
                   FROM STDIN""") as copy:

            for batch_num in tqdm(range(total_batches), desc="Incident occurrence batches"):
                for _ in range(batch_size):
                    incident_id = random.choice(self.incident_ids)
                    occurred_at = datetime.now() - timedelta(
                        days=random.randint(0, 180),
                        hours=random.randint(0, 23),
                        minutes=random.randint(0, 59)
                    )

                    details = json.dumps({
                        'batch': batch_num,
                        'reporter': fake.name(),
                        'detection_source': random.choice(['siem', 'ids', 'manual', 'automated']),
                        'response_time_minutes': random.randint(1, 480),
                        'affected_systems': random.randint(1, 50)
                    })

                    copy.write_row((
                        str(uuid.uuid4()),
                        incident_id,
                        occurred_at,
                        details,
                        random.choices(statuses, weights=[30, 25, 20, 15, 10])[0],
                        occurred_at,
                        occurred_at
                    ))
                    rows_processed += 1

        # Commit after COPY completes
        self.conn.commit()
        print(f"  Inserted {rows_processed:,} incident occurrences")

    def generate_user_assets(self) -> List[Tuple]:
        """Generate user-asset relationships."""
        relationships = []
        roles = ['viewer', 'editor', 'admin', 'owner']

        for user_id in self.user_ids:
            # Each user gets random number of assets
            num_assets = random.randint(5, min(15, len(self.asset_ids)))
            assigned_assets = random.sample(self.asset_ids, num_assets)

            for asset_id in assigned_assets:
                relationships.append((
                    user_id,
                    asset_id,
                    random.choices(roles, weights=[40, 30, 20, 10])[0],
                    datetime.now() - timedelta(days=random.randint(0, 365))
                ))

        return relationships

    def generate_asset_tags(self) -> List[Tuple]:
        """Generate asset-tag relationships."""
        relationships = []

        for asset_id in self.asset_ids:
            # Each asset gets 2-5 tags
            num_tags = random.randint(2, min(5, len(self.tag_ids)))
            assigned_tags = random.sample(self.tag_ids, num_tags)

            for tag_id in assigned_tags:
                relationships.append((
                    asset_id,
                    tag_id,
                    datetime.now() - timedelta(days=random.randint(0, 365))
                ))

        return relationships

    def populate_database(self):
        """Main method to populate all tables."""
        try:
            # Users
            print("Inserting users...")
            users = self.generate_users()
            self.cur.executemany(
                "INSERT INTO users (id, username, email, created_at, updated_at) VALUES (%s, %s, %s, %s, %s)",
                users
            )

            # Tags
            print("Inserting tags...")
            tags = self.generate_tags()
            self.cur.executemany(
                "INSERT INTO tags (id, name, description, created_at, updated_at) VALUES (%s, %s, %s, %s, %s)",
                tags
            )

            # Assets
            print("Inserting assets...")
            assets = self.generate_assets()
            self.cur.executemany(
                "INSERT INTO assets (id, name, asset_type, status, metadata, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                assets
            )

            # Events
            print("Inserting events...")
            events = self.generate_events()
            self.cur.executemany(
                "INSERT INTO events (id, asset_id, event_type, severity, description, metadata, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                events
            )

            # Incidents
            print("Inserting incidents...")
            incidents = self.generate_incidents()
            self.cur.executemany(
                "INSERT INTO incidents (id, asset_id, incident_type, severity, priority, title, description, status, metadata, created_at, updated_at, resolved_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                incidents
            )

            # User-Asset relationships
            print("Inserting user-asset relationships...")
            user_assets = self.generate_user_assets()
            self.cur.executemany(
                "INSERT INTO user_assets (user_id, asset_id, role, assigned_at) VALUES (%s, %s, %s, %s)",
                user_assets
            )

            # Asset-Tag relationships
            print("Inserting asset-tag relationships...")
            asset_tags = self.generate_asset_tags()
            self.cur.executemany(
                "INSERT INTO asset_tags (asset_id, tag_id, tagged_at) VALUES (%s, %s, %s)",
                asset_tags
            )

            self.conn.commit()

            # Generate large occurrence tables
            self.generate_event_occurrences()
            self.generate_incident_occurrences()

            # Print statistics
            self.print_statistics()

        except Exception as e:
            self.conn.rollback()
            print(f"Error: {e}")
            raise

    def print_statistics(self):
        """Print table row counts."""
        print("\n=== Database Population Complete ===")
        tables = ['users', 'assets', 'tags', 'events', 'incidents',
                  'event_occurrences', 'incident_occurrences',
                  'user_assets', 'asset_tags']

        for table in tables:
            self.cur.execute(f"SELECT COUNT(*) FROM {table}")
            count = self.cur.fetchone()[0]
            print(f"{table:20} : {count:10,} rows")


def main():
    """Main execution function."""
    print("Connecting to database...")
    conn = psycopg.connect(**DB_CONFIG)

    try:
        # Set optimal parameters for bulk loading
        cur = conn.cursor()
        cur.execute("SET synchronous_commit = OFF")
        cur.execute("SET maintenance_work_mem = '256MB'")
        cur.execute("SET work_mem = '32MB'")

        generator = DataGenerator(conn)
        generator.populate_database()

        # Run ANALYZE to update statistics
        print("\nUpdating table statistics...")
        cur.execute("ANALYZE")
        conn.commit()

    finally:
        conn.close()
        print("\nDatabase connection closed.")


if __name__ == "__main__":
    main()