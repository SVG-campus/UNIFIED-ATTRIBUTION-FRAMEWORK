"""
Cross-Domain Relationship Finder
Discovers patterns and analogies across different academic fields
"""

import numpy as np
from typing import Dict, List, Tuple, Any
import json
from dataclasses import dataclass, asdict
from collections import defaultdict

@dataclass
class DomainPattern:
    domain: str
    pattern_type: str
    features: Dict[str, float]
    attribution_vector: List[float]
    metadata: Dict[str, Any]

@dataclass
class CrossDomainRelationship:
    domain_a: str
    domain_b: str
    similarity_score: float
    shared_patterns: List[str]
    analogies: List[Dict[str, str]]

class RelationshipFinder:
    """Finds relationships and analogies across academic domains"""

    def __init__(self):
        self.domain_patterns = defaultdict(list)
        self.relationships = []

    def add_domain_pattern(self, pattern: DomainPattern):
        """Register a pattern from a specific domain"""
        self.domain_patterns[pattern.domain].append(pattern)

    def cosine_similarity(self, vec_a: List[float], vec_b: List[float]) -> float:
        """Calculate cosine similarity between two vectors"""
        vec_a = np.array(vec_a)
        vec_b = np.array(vec_b)

        if len(vec_a) == 0 or len(vec_b) == 0:
            return 0.0

        dot_product = np.dot(vec_a, vec_b)
        norm_a = np.linalg.norm(vec_a)
        norm_b = np.linalg.norm(vec_b)

        if norm_a == 0 or norm_b == 0:
            return 0.0

        return float(dot_product / (norm_a * norm_b))

    def find_domain_similarities(self, threshold: float = 0.5) -> List[CrossDomainRelationship]:
        """Find similarities between all domain pairs"""
        domains = list(self.domain_patterns.keys())
        relationships = []

        for i, domain_a in enumerate(domains):
            for domain_b in domains[i+1:]:
                patterns_a = self.domain_patterns[domain_a]
                patterns_b = self.domain_patterns[domain_b]

                similarities = []
                shared_patterns = []
                analogies = []

                for pattern_a in patterns_a:
                    for pattern_b in patterns_b:
                        sim = self.cosine_similarity(
                            pattern_a.attribution_vector,
                            pattern_b.attribution_vector
                        )

                        if sim >= threshold:
                            similarities.append(sim)
                            shared_patterns.append(f"{pattern_a.pattern_type}↔{pattern_b.pattern_type}")
                            analogies.append({
                                "from": f"{domain_a}.{pattern_a.pattern_type}",
                                "to": f"{domain_b}.{pattern_b.pattern_type}",
                                "similarity": round(sim, 3)
                            })

                if similarities:
                    avg_similarity = np.mean(similarities)
                    relationship = CrossDomainRelationship(
                        domain_a=domain_a,
                        domain_b=domain_b,
                        similarity_score=round(avg_similarity, 3),
                        shared_patterns=list(set(shared_patterns)),
                        analogies=analogies
                    )
                    relationships.append(relationship)

        self.relationships = sorted(relationships, key=lambda x: x.similarity_score, reverse=True)
        return self.relationships

    def generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive relationship report"""
        if not self.relationships:
            self.find_domain_similarities()

        report = {
            "total_domains": len(self.domain_patterns),
            "total_patterns": sum(len(patterns) for patterns in self.domain_patterns.values()),
            "total_relationships": len(self.relationships),
            "strongest_relationships": [
                asdict(rel) for rel in self.relationships[:10]
            ],
            "domain_connectivity": self._calculate_connectivity(),
            "universal_patterns": self._find_universal_patterns()
        }

        return report

    def _calculate_connectivity(self) -> Dict[str, int]:
        """Calculate how many connections each domain has"""
        connectivity = defaultdict(int)
        for rel in self.relationships:
            connectivity[rel.domain_a] += 1
            connectivity[rel.domain_b] += 1
        return dict(connectivity)

    def _find_universal_patterns(self) -> List[Dict[str, Any]]:
        """Find patterns that appear across multiple domains"""
        pattern_counts = defaultdict(list)

        for rel in self.relationships:
            for pattern in rel.shared_patterns:
                pattern_counts[pattern].append((rel.domain_a, rel.domain_b))

        universal = [
            {
                "pattern": pattern,
                "frequency": len(domains),
                "domains": [f"{d[0]}-{d[1]}" for d in domains]
            }
            for pattern, domains in pattern_counts.items()
            if len(domains) >= 3
        ]

        return sorted(universal, key=lambda x: x["frequency"], reverse=True)

if __name__ == "__main__":
    print("Cross-Domain Relationship Finder loaded successfully")
