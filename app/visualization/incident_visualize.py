import logging
from neo4j import GraphDatabase

logger = logging.getLogger(__name__)

class Neo4jVisualizer:
    def __init__(self, uri, user, password):
        """Init connect to the Neo4j db."""
        try:
            self.driver = GraphDatabase.driver(uri, auth=(user, password))
            print("Connected to Neo4j Graph Database.")
        except Exception as e:
            print(f"Failed to connect to Neo4j: {e}")
            self.driver = None

    def close(self):
        if self.driver:
            self.driver.close()

    def ingest_incident_chain(self, incident_chain: dict):
        """Parses the JSON chain and writes it to the graph."""
        if not self.driver:
            print("No database connection. Skipping graph ingestion.")
            return

        incident_id = incident_chain.get("incident_id")
        alerts = incident_chain.get("alerts", [])

        if not alerts:
            return

        with self.driver.session() as session:
            session.execute_write(
                self._create_incident_node,
                incident_chain
            )

            # Process each alert and link it to the incident
            for i, alert in enumerate(alerts):
                session.execute_write(self._create_alert_node_and_link, incident_id, alert)
                
                # Link alerts sequentially to show the attack path over time
                if i > 0:
                    prev_alert = alerts[i-1]
                    session.execute_write(
                        self._link_alerts_sequentially, 
                        prev_alert["event_id"], 
                        alert["event_id"]
                    )
            
            print(f"Successfully pushed incident {incident_id} to the Graph!")

    @staticmethod
    def _create_incident_node(tx, incident_chain):

        query = """
        MERGE (i:Incident {id:$incident_id})

        SET
            i.status=$status,
            i.start_time=$start_time,
            i.last_updated=$last_updated,
            i.agent_id=$agent_id
        """

        tx.run(
            query,
            incident_id=incident_chain.get("incident_id"),
            status=incident_chain.get("status", "OPEN"),
            start_time=incident_chain.get("start_time", ""),
            last_updated=incident_chain.get("last_updated", ""),
            agent_id=incident_chain.get("agent_id", "unknown")
        )

    @staticmethod
    def _create_alert_node_and_link(tx, incident_id, alert):

        alert_id = alert.get("event_id", "unknown")

        detector = alert.get(
            "source_detector",
            "UnknownDetector"
        )

        alert_type = alert.get(
            "type",
            "unknown"
        )

        risk = alert.get(
            "risk",
            0
        )

        malicious = alert.get(
            "is_malicious",
            False
        )

        query = """
        MATCH (i:Incident {id: $incident_id})

        MERGE (a:Alert {id: $alert_id})

        SET 
            a.detector = $detector,
            a.type = $type,
            a.risk = $risk,
            a.is_malicious = $malicious,
            a.timestamp = $timestamp

        MERGE (i)-[:CONTAINS_ALERT]->(a)
        """

        tx.run(
            query,
            incident_id=incident_id,
            alert_id=alert_id,
            detector=detector,
            type=alert_type,
            risk=risk,
            malicious=malicious,
            timestamp=alert.get("timestamp", "")
        )

    @staticmethod
    def _link_alerts_sequentially(tx, prev_alert_id, current_alert_id):
        query = """
        MATCH (prev:Alert {id: $prev_alert_id})
        MATCH (curr:Alert {id: $current_alert_id})
        MERGE (prev)-[:FOLLOWED_BY]->(curr)
        """
        tx.run(query, prev_alert_id=prev_alert_id, current_alert_id=current_alert_id)