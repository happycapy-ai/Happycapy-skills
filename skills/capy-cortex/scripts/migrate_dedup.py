#!/usr/bin/env python3
"""
Nuclear deduplication migration script for cortex.db
Removes duplicate rules by content, merges metadata, resets harmful_count, and adds constraints.
"""

import sqlite3
import sys
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "cortex.db"

def migrate_dedup():
    """Perform nuclear deduplication migration."""
    print(f"Connecting to database: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Get initial statistics
    initial_count = cursor.execute("SELECT COUNT(*) FROM rules").fetchone()[0]
    unique_content_count = cursor.execute("SELECT COUNT(DISTINCT content) FROM rules").fetchone()[0]
    duplicate_count = initial_count - unique_content_count

    print(f"\n=== BEFORE MIGRATION ===")
    print(f"Total rules: {initial_count}")
    print(f"Unique content: {unique_content_count}")
    print(f"Duplicates to remove: {duplicate_count}")

    # Get category breakdown before
    print("\nRules by category (before):")
    for row in cursor.execute("SELECT category, COUNT(*) as cnt FROM rules GROUP BY category ORDER BY cnt DESC"):
        print(f"  {row['category']}: {row['cnt']}")

    # Find all duplicate groups
    print("\n=== PROCESSING DUPLICATES ===")
    duplicate_groups = cursor.execute("""
        SELECT content, COUNT(*) as cnt
        FROM rules
        GROUP BY content
        HAVING cnt > 1
        ORDER BY cnt DESC
    """).fetchall()

    print(f"Found {len(duplicate_groups)} duplicate groups")

    deleted_total = 0

    for group in duplicate_groups:
        content = group['content']
        count = group['cnt']

        # Get all rules with this content
        duplicates = cursor.execute("""
            SELECT id, occurrences, helpful_count, confidence, created_at, last_seen
            FROM rules
            WHERE content = ?
            ORDER BY helpful_count DESC, id ASC
        """, (content,)).fetchall()

        # Keep the first one (highest helpful_count)
        keeper = duplicates[0]
        to_delete = duplicates[1:]

        # Merge metadata
        total_occurrences = sum(d['occurrences'] for d in duplicates)
        total_helpful = sum(d['helpful_count'] for d in duplicates)
        max_confidence = max(d['confidence'] for d in duplicates)
        min_created = min(d['created_at'] for d in duplicates)
        max_last_seen = max(d['last_seen'] for d in duplicates)

        # Update the keeper with merged metadata
        cursor.execute("""
            UPDATE rules
            SET occurrences = ?,
                helpful_count = ?,
                confidence = ?,
                created_at = ?,
                last_seen = ?
            WHERE id = ?
        """, (total_occurrences, total_helpful, max_confidence, min_created, max_last_seen, keeper['id']))

        # Delete the duplicates
        for dup in to_delete:
            cursor.execute("DELETE FROM rules WHERE id = ?", (dup['id'],))
            deleted_total += 1

        if len(duplicate_groups) <= 10 or count > 5:
            print(f"  Merged {count} duplicates for content (keeping id={keeper['id']})")

    print(f"\nDeleted {deleted_total} duplicate rules")

    # Reset ALL harmful_count to 0
    print("\n=== RESETTING HARMFUL_COUNT ===")
    cursor.execute("UPDATE rules SET harmful_count = 0")
    print("Reset all harmful_count to 0 (feedback was broken)")

    # Try to add content_hash column (may already exist)
    print("\n=== ADDING CONTENT_HASH COLUMN ===")
    try:
        cursor.execute("ALTER TABLE rules ADD COLUMN content_hash TEXT")
        print("Added content_hash column")
    except sqlite3.OperationalError as e:
        if "duplicate column" in str(e).lower():
            print("content_hash column already exists")
        else:
            print(f"Warning: Could not add content_hash column: {e}")

    # Try to create unique index on content
    print("\n=== CREATING UNIQUE INDEX ===")
    try:
        cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_rules_content_unique ON rules(content)")
        print("Created unique index on content column")
    except sqlite3.OperationalError as e:
        print(f"Warning: Could not create unique index: {e}")

    # Commit all changes
    conn.commit()

    # Verify FTS5 consistency
    print("\n=== VERIFYING FTS5 INDEX ===")
    try:
        # The triggers should have automatically updated rules_fts
        # Let's verify by checking if counts match
        rules_count = cursor.execute("SELECT COUNT(*) FROM rules").fetchone()[0]
        fts_count = cursor.execute("SELECT COUNT(*) FROM rules_fts").fetchone()[0]

        if rules_count == fts_count:
            print(f"FTS5 index is consistent (both have {rules_count} rows)")
        else:
            print(f"WARNING: FTS5 mismatch! rules={rules_count}, rules_fts={fts_count}")
            print("Attempting to rebuild FTS5 index...")
            # Rebuild FTS5 index
            cursor.execute("INSERT INTO rules_fts(rules_fts) VALUES('rebuild')")
            conn.commit()
            print("FTS5 index rebuilt")
    except Exception as e:
        print(f"Warning: Could not verify FTS5: {e}")

    # Get final statistics
    final_count = cursor.execute("SELECT COUNT(*) FROM rules").fetchone()[0]
    final_unique = cursor.execute("SELECT COUNT(DISTINCT content) FROM rules").fetchone()[0]

    print(f"\n=== AFTER MIGRATION ===")
    print(f"Total rules: {final_count}")
    print(f"Unique content: {final_unique}")
    print(f"Match: {final_count == final_unique}")

    # Get category breakdown after
    print("\nRules by category (after):")
    for row in cursor.execute("SELECT category, COUNT(*) as cnt FROM rules GROUP BY category ORDER BY cnt DESC"):
        print(f"  {row['category']}: {row['cnt']}")

    print(f"\n=== SUMMARY ===")
    print(f"Rules before: {initial_count}")
    print(f"Rules after: {final_count}")
    print(f"Rules deleted: {deleted_total}")
    print(f"Harmful counts reset: ALL (was broken)")

    # Test FTS5 query
    print("\n=== TESTING FTS5 ===")
    try:
        test_results = cursor.execute("""
            SELECT COUNT(*) FROM rules_fts WHERE rules_fts MATCH 'error'
        """).fetchone()[0]
        print(f"FTS5 test query successful (found {test_results} matches for 'error')")
    except Exception as e:
        print(f"WARNING: FTS5 test query failed: {e}")

    conn.close()
    print("\n=== MIGRATION COMPLETE ===")

if __name__ == "__main__":
    try:
        migrate_dedup()
    except Exception as e:
        print(f"\nERROR: Migration failed: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)
