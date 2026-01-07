"""
Test Neo4j Connection Script
Quick test to verify Neo4j connection before running Phase 4
"""

from py2neo import Graph
import sys

# Configuration
# Neo4j Desktop Local Database
NEO4J_URI = "ADD_YOUR_BOLT_URI_HERE"  # e.g., "bolt://
NEO4J_USER = "ADD_YOUR_USERNAME_HERE"
NEO4J_PASSWORD = "ADD_YOUR_PASSWORD_HERE"
NEO4J_DATABASE = "ADD_YOUR_DATABASE_NAME_HERE"  # Not used in this script but can be useful for reference

print("=" * 80)
print("NEO4J CONNECTION TEST")
print("=" * 80)

print(f"\nAttempting to connect to Neo4j...")
print(f"URI: {NEO4J_URI}")
print(f"User: {NEO4J_USER}")

try:
    graph = Graph(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    
    # Test connection
    result = graph.run("RETURN 1 as test").data()
    
    if result:
        print("✓ Connection successful!")
        
        # Get database info
        try:
            db_info = graph.run("CALL dbms.components() YIELD name, versions, edition RETURN name, versions[0] as version, edition").data()
            print("\nDatabase Information:")
            for info in db_info:
                print(f"  {info['name']}: {info['version']} ({info['edition']})")
        except:
            pass
        
        # Get node counts
        try:
            node_count = graph.run("MATCH (n) RETURN COUNT(n) as count").data()[0]['count']
            rel_count = graph.run("MATCH ()-[r]->() RETURN COUNT(r) as count").data()[0]['count']
            print(f"\nCurrent Database State:")
            print(f"  Nodes: {node_count:,}")
            print(f"  Relationships: {rel_count:,}")
        except Exception as e:
            print(f"\n⚠️  Could not retrieve database state: {e}")
        
        print("\n" + "=" * 80)
        print("✓ Connection test passed! You can proceed with Phase 4.")
        print("=" * 80)
        sys.exit(0)
    else:
        print("✗ Connection test failed: No response from database")
        sys.exit(1)
        
except Exception as e:
    print(f"\n✗ Connection failed: {e}")
    print("\nTroubleshooting:")
    print("  1. Ensure Neo4j Desktop is installed and running")
    print("  2. Database is started in Neo4j Desktop (green status)")
    print("  3. Verify username and password are correct")
    print("  4. Check that database is accessible at bolt://127.0.0.1:7687")
    print("  5. Verify the URI format: bolt://127.0.0.1:7687")
    print("\nTo change connection settings, edit NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD in this script")
    sys.exit(1)

