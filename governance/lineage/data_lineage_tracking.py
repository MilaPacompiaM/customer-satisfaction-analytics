#!/usr/bin/env python3
"""
Data Lineage Tracking for Customer Satisfaction Analytics
Tracks data flow from raw to curated layers
"""

import json
import pandas as pd
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict

@dataclass
class DataLineageEntry:
    """Data lineage entry for tracking transformations"""
    source_table: str
    target_table: str
    transformation_type: str
    transformation_description: str
    columns_affected: List[str]
    timestamp: str
    job_id: str
    data_quality_score: Optional[float] = None
    record_count_before: Optional[int] = None
    record_count_after: Optional[int] = None

class DataLineageTracker:
    """Tracks data lineage across the data pipeline"""

    def __init__(self, metadata_path: str = "governance/lineage/"):
        self.metadata_path = metadata_path
        self.lineage_entries: List[DataLineageEntry] = []

    def add_transformation(self,
                         source_table: str,
                         target_table: str,
                         transformation_type: str,
                         description: str,
                         columns_affected: List[str],
                         job_id: str,
                         data_quality_score: float = None,
                         record_count_before: int = None,
                         record_count_after: int = None) -> None:
        """Add a transformation to the lineage"""

        entry = DataLineageEntry(
            source_table=source_table,
            target_table=target_table,
            transformation_type=transformation_type,
            transformation_description=description,
            columns_affected=columns_affected,
            timestamp=datetime.now().isoformat(),
            job_id=job_id,
            data_quality_score=data_quality_score,
            record_count_before=record_count_before,
            record_count_after=record_count_after
        )

        self.lineage_entries.append(entry)

    def get_table_lineage(self, table_name: str) -> List[DataLineageEntry]:
        """Get lineage for a specific table"""
        return [entry for entry in self.lineage_entries
                if entry.target_table == table_name or entry.source_table == table_name]

    def get_data_flow(self, from_layer: str, to_layer: str) -> List[DataLineageEntry]:
        """Get data flow between layers"""
        return [entry for entry in self.lineage_entries
                if from_layer in entry.source_table and to_layer in entry.target_table]

    def generate_lineage_report(self) -> Dict:
        """Generate comprehensive lineage report"""
        report = {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "total_transformations": len(self.lineage_entries),
                "pipeline_layers": ["raw", "processed", "curated"]
            },
            "data_flow_summary": {
                "raw_to_processed": len(self.get_data_flow("raw", "processed")),
                "processed_to_curated": len(self.get_data_flow("processed", "curated")),
                "direct_raw_to_curated": len(self.get_data_flow("raw", "curated"))
            },
            "transformations": [asdict(entry) for entry in self.lineage_entries],
            "data_quality_metrics": {
                "avg_quality_score": self._calculate_avg_quality(),
                "transformations_with_quality_check": len([e for e in self.lineage_entries if e.data_quality_score is not None])
            }
        }
        return report

    def _calculate_avg_quality(self) -> float:
        """Calculate average data quality score"""
        scores = [entry.data_quality_score for entry in self.lineage_entries
                 if entry.data_quality_score is not None]
        return sum(scores) / len(scores) if scores else 0.0

    def save_lineage(self, filename: str = None) -> None:
        """Save lineage to JSON file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{self.metadata_path}/lineage_{timestamp}.json"

        report = self.generate_lineage_report()

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

    def visualize_lineage(self) -> str:
        """Generate a simple text visualization of data lineage"""
        viz = "DATA LINEAGE FLOW\n"
        viz += "=" * 50 + "\n\n"

        # Group by transformation type
        by_type = {}
        for entry in self.lineage_entries:
            if entry.transformation_type not in by_type:
                by_type[entry.transformation_type] = []
            by_type[entry.transformation_type].append(entry)

        for trans_type, entries in by_type.items():
            viz += f"{trans_type.upper()}:\n"
            for entry in entries:
                viz += f"  {entry.source_table} -> {entry.target_table}\n"
                viz += f"    Description: {entry.transformation_description}\n"
                viz += f"    Columns: {', '.join(entry.columns_affected)}\n"
                if entry.data_quality_score:
                    viz += f"    Quality Score: {entry.data_quality_score:.2f}\n"
                viz += "\n"

        return viz

# Example usage for Customer Satisfaction Pipeline
def example_customer_satisfaction_lineage():
    """Example of tracking lineage for customer satisfaction pipeline"""

    tracker = DataLineageTracker()

    # Raw to Processed transformations
    tracker.add_transformation(
        source_table="raw_customer_tickets",
        target_table="processed_customer_interactions",
        transformation_type="CLEANING_AND_VALIDATION",
        description="Clean ticket data, validate fields, standardize formats",
        columns_affected=["customer_id", "satisfaction_score", "channel", "created_at"],
        job_id="glue-job-001",
        data_quality_score=0.95,
        record_count_before=50000,
        record_count_after=48500
    )

    tracker.add_transformation(
        source_table="raw_customer_tickets",
        target_table="processed_customer_interactions",
        transformation_type="ANONYMIZATION",
        description="Hash customer IDs and anonymize PII fields",
        columns_affected=["customer_id", "agent_id"],
        job_id="glue-job-002",
        data_quality_score=1.0,
        record_count_before=48500,
        record_count_after=48500
    )

    # Processed to Curated transformations
    tracker.add_transformation(
        source_table="processed_customer_interactions",
        target_table="curated_satisfaction_metrics",
        transformation_type="AGGREGATION",
        description="Calculate daily satisfaction metrics by channel and department",
        columns_affected=["satisfaction_score", "channel", "department", "interaction_date"],
        job_id="glue-job-003",
        data_quality_score=0.98,
        record_count_before=48500,
        record_count_after=1825  # Daily aggregates for 5 years
    )

    # Generate and print report
    report = tracker.generate_lineage_report()
    print(json.dumps(report, indent=2))

    # Print visualization
    print("\n" + tracker.visualize_lineage())

if __name__ == "__main__":
    example_customer_satisfaction_lineage()