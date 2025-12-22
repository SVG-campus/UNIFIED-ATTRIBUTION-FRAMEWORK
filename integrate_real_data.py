"""
Integration: Real Data + Grand Unified Framework
Connects government/academic data to universal problem solver
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from real_data_adapters import (
    PubChemAdapter, USGSEarthquakeAdapter, NIHReporterAdapter,
    NASAAdapter, NOAAWeatherAdapter, DataGovAdapter
)
from grand_unified_framework import (
    UniversalProblemSolver, UniversalKnowledgeNode, UniversalKnowledgeGraph
)
import numpy as np

class RealDataIntegrator:
    """Integrates real scientific data into the universal framework"""

    def __init__(self):
        self.solver = UniversalProblemSolver()
        self.data_sources = {
            'chemistry': PubChemAdapter(),
            'geology': USGSEarthquakeAdapter(),
            'medicine': NIHReporterAdapter(),
            'astronomy': NASAAdapter(),
            'climate': NOAAWeatherAdapter(),
            'general': DataGovAdapter()
        }

    def ingest_all_real_data(self):
        """Fetch and ingest real data from all sources"""
        print("="*70)
        print("🌍 INGESTING REAL SCIENTIFIC DATA INTO UNIVERSAL FRAMEWORK")
        print("="*70)

        # Chemistry from PubChem
        print("\n[1/6] Chemistry Data (PubChem/NIH)...")
        chem_data = self.data_sources['chemistry'].get_compound_properties([
            'aspirin', 'glucose', 'caffeine', 'morphine', 'penicillin',
            'insulin', 'testosterone', 'cortisol', 'serotonin', 'dopamine'
        ])
        self._ingest_chemistry(chem_data)

        # Geology from USGS
        print("\n[2/6] Geology Data (USGS)...")
        geo_data = self.data_sources['geology'].get_recent_earthquakes(min_magnitude=4.0)
        self._ingest_geology(geo_data)

        # Medicine from NIH
        print("\n[3/6] Medical Research (NIH RePORTER)...")
        med_data = self.data_sources['medicine'].search_projects("immunotherapy", limit=10)
        self._ingest_medicine(med_data)

        # Astronomy from NASA
        print("\n[4/6] Astronomy Data (NASA)...")
        astro_data = self.data_sources['astronomy'].get_near_earth_objects("2024-01-15")
        self._ingest_astronomy(astro_data)

        # Climate from NOAA
        print("\n[5/6] Climate Data (NOAA)...")
        climate_data = self.data_sources['climate'].get_weather_stations_data("CA")
        self._ingest_climate(climate_data)

        # General from Data.gov
        print("\n[6/6] Government Datasets (Data.gov)...")
        gov_data = self.data_sources['general'].search_datasets("health", rows=10)
        self._ingest_government(gov_data)

        print("\n✅ ALL REAL DATA INGESTED INTO UNIVERSAL GRAPH")

    def _ingest_chemistry(self, data: dict):
        """Convert chemistry data to knowledge nodes"""
        if 'compounds' not in data:
            return

        for compound in data['compounds'][:15]:
            # Create features from real chemical properties
            features = np.array([
                compound['molecular_weight'],
                len(compound['formula']),
                hash(compound['formula']) % 1000
            ], dtype=float)

            # Normalize features
            features = features / (np.linalg.norm(features) + 1e-8)

            # Create embedding (in real implementation, use chemical fingerprints)
            embedding = np.random.randn(128)
            embedding = embedding / np.linalg.norm(embedding)

            node = UniversalKnowledgeNode(
                node_id=f"chem_{compound['compound']}",
                domain="chemistry",
                features=features,
                embeddings=embedding,
                connections=[],
                metadata=compound
            )

            self.solver.knowledge_graph.add_node(node)

        print(f"  ✓ Added {len(data['compounds'][:15])} chemistry nodes")

    def _ingest_geology(self, data: dict):
        """Convert earthquake data to knowledge nodes"""
        if 'earthquakes' not in data:
            return

        for eq in data['earthquakes'][:15]:
            features = np.array([
                eq['magnitude'],
                eq['depth_km'],
                abs(eq['latitude'])
            ], dtype=float)

            features = features / (np.linalg.norm(features) + 1e-8)
            embedding = np.random.randn(128)
            embedding = embedding / np.linalg.norm(embedding)

            node = UniversalKnowledgeNode(
                node_id=f"geo_eq_{hash(eq['place']) % 10000}",
                domain="geology",
                features=features,
                embeddings=embedding,
                connections=[],
                metadata=eq
            )

            self.solver.knowledge_graph.add_node(node)

        print(f"  ✓ Added {len(data['earthquakes'][:15])} geology nodes")

    def _ingest_medicine(self, data: dict):
        """Convert medical research to knowledge nodes"""
        if 'projects' not in data:
            return

        for proj in data['projects'][:15]:
            features = np.array([
                proj['award_amount'] / 1e6,
                proj['fiscal_year'] - 2020,
                len(proj['title'])
            ], dtype=float)

            features = features / (np.linalg.norm(features) + 1e-8)
            embedding = np.random.randn(128)
            embedding = embedding / np.linalg.norm(embedding)

            node = UniversalKnowledgeNode(
                node_id=f"med_proj_{hash(proj['title']) % 10000}",
                domain="medicine",
                features=features,
                embeddings=embedding,
                connections=[],
                metadata=proj
            )

            self.solver.knowledge_graph.add_node(node)

        print(f"  ✓ Added {len(data['projects'][:15])} medicine nodes")

    def _ingest_astronomy(self, data: dict):
        """Convert asteroid data to knowledge nodes"""
        if 'asteroids' not in data:
            return

        for asteroid in data['asteroids'][:15]:
            features = np.array([
                asteroid['diameter_km'],
                asteroid['velocity_kmh'] / 1000,
                asteroid['distance_km'] / 1e6
            ], dtype=float)

            features = features / (np.linalg.norm(features) + 1e-8)
            embedding = np.random.randn(128)
            embedding = embedding / np.linalg.norm(embedding)

            node = UniversalKnowledgeNode(
                node_id=f"astro_{asteroid['name'].replace(' ', '_')}",
                domain="astronomy",
                features=features,
                embeddings=embedding,
                connections=[],
                metadata=asteroid
            )

            self.solver.knowledge_graph.add_node(node)

        print(f"  ✓ Added {len(data['asteroids'][:15])} astronomy nodes")

    def _ingest_climate(self, data: dict):
        """Convert weather station data to knowledge nodes"""
        if 'stations' not in data:
            return

        for station in data['stations'][:15]:
            features = np.array([
                station['latitude'],
                station['longitude'],
                station['elevation']
            ], dtype=float)

            features = features / (np.linalg.norm(features) + 1e-8)
            embedding = np.random.randn(128)
            embedding = embedding / np.linalg.norm(embedding)

            node = UniversalKnowledgeNode(
                node_id=f"climate_{station['station_id']}",
                domain="climate",
                features=features,
                embeddings=embedding,
                connections=[],
                metadata=station
            )

            self.solver.knowledge_graph.add_node(node)

        print(f"  ✓ Added {len(data['stations'][:15])} climate nodes")

    def _ingest_government(self, data: dict):
        """Convert government datasets to knowledge nodes"""
        if 'datasets' not in data:
            return

        for dataset in data['datasets'][:15]:
            features = np.array([
                dataset['num_resources'],
                len(dataset['title']),
                hash(dataset['organization']) % 1000
            ], dtype=float)

            features = features / (np.linalg.norm(features) + 1e-8)
            embedding = np.random.randn(128)
            embedding = embedding / np.linalg.norm(embedding)

            node = UniversalKnowledgeNode(
                node_id=f"gov_{hash(dataset['title']) % 10000}",
                domain="government_data",
                features=features,
                embeddings=embedding,
                connections=[],
                metadata=dataset
            )

            self.solver.knowledge_graph.add_node(node)

        print(f"  ✓ Added {len(data['datasets'][:15])} government data nodes")

    def solve_real_world_problems(self):
        """Solve actual grand challenges using real data"""
        print("\n" + "="*70)
        print("🎯 SOLVING REAL-WORLD GRAND CHALLENGES")
        print("="*70)

        # Discover patterns across ALL real data
        patterns = self.solver.discover_universal_patterns()

        # Define grand challenges
        challenges = [
            {
                'name': 'Drug Discovery for Rare Diseases',
                'domain': 'medicine',
                'data': {'target_diseases': 5000, 'current_treatments': 500}
            },
            {
                'name': 'Earthquake Early Warning System',
                'domain': 'geology',
                'data': {'false_positive_rate': 0.15, 'lead_time_seconds': 45}
            },
            {
                'name': 'Asteroid Impact Prevention',
                'domain': 'astronomy',
                'data': {'tracked_objects': 30000, 'potentially_hazardous': 2300}
            },
            {
                'name': 'Climate-Resilient Agriculture',
                'domain': 'climate',
                'data': {'crop_yield_decline': 0.22, 'adaptation_rate': 0.08}
            }
        ]

        solutions = []
        for challenge in challenges:
            solution = self.solver.solve_grand_challenge(challenge)
            solutions.append(solution)

        return solutions

    def generate_comprehensive_report(self, solutions: list):
        """Generate detailed analysis report"""
        print("\n" + "="*70)
        print("📊 COMPREHENSIVE ANALYSIS REPORT")
        print("="*70)

        total_nodes = len(self.solver.knowledge_graph.nodes)
        total_domains = len(self.solver.knowledge_graph.domain_clusters)
        total_patterns = len(self.solver.universal_patterns)

        print(f"\n🌐 Knowledge Graph Statistics:")
        print(f"  • Total Nodes: {total_nodes}")
        print(f"  • Total Domains: {total_domains}")
        print(f"  • Universal Patterns: {total_patterns}")

        print(f"\n📈 Domain Distribution:")
        for domain, nodes in self.solver.knowledge_graph.domain_clusters.items():
            print(f"  • {domain}: {len(nodes)} nodes")

        print(f"\n🎯 Solutions Generated: {len(solutions)}")
        for sol in solutions:
            print(f"\n  📌 {sol['challenge']}")
            print(f"     Confidence: {sol['confidence_score']:.1%}")
            print(f"     Novel Approaches: {len(sol['novel_approaches'])}")

            if sol['novel_approaches']:
                print(f"     Top Approach: {sol['novel_approaches'][0][:70]}...")

        print("\n" + "="*70)
        print("✅ REAL DATA ANALYSIS COMPLETE")
        print("="*70)

        return {
            'total_nodes': total_nodes,
            'total_domains': total_domains,
            'total_patterns': total_patterns,
            'solutions': solutions
        }

def main():
    """Main integration workflow"""
    print("\n" + "="*70)
    print("🚀 LAUNCHING INTEGRATED REAL DATA ANALYSIS")
    print("="*70)

    # Initialize integrator
    integrator = RealDataIntegrator()

    # Step 1: Ingest all real data
    integrator.ingest_all_real_data()

    # Step 2: Solve real-world problems
    solutions = integrator.solve_real_world_problems()

    # Step 3: Generate report
    report = integrator.generate_comprehensive_report(solutions)

    # Save report
    import json
    with open("grand_unified_report.json", "w") as f:
        # Convert solutions to serializable format
        serializable_solutions = []
        for sol in report['solutions']:
            serializable_solutions.append({
                'challenge': sol['challenge'],
                'domain': sol['domain'],
                'confidence_score': float(sol['confidence_score']),
                'novel_approaches': sol['novel_approaches'],
                'num_insights': len(sol['cross_domain_insights']),
                'num_patterns': len(sol['universal_patterns_applied'])
            })

        json.dump({
            'total_nodes': report['total_nodes'],
            'total_domains': report['total_domains'],
            'total_patterns': report['total_patterns'],
            'solutions': serializable_solutions
        }, f, indent=2)

    print("\n💾 Report saved to: grand_unified_report.json")
    print("\n🎉 INTEGRATION COMPLETE!")

if __name__ == "__main__":
    main()
