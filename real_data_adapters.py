"""
Real Scientific Data Adapters
Connects to freely available government and academic databases
NO API KEYS REQUIRED for these sources
"""

import requests
import numpy as np
import json
from typing import Dict, List, Any, Optional
import time

class RealDataAdapter:
    """Base adapter for real scientific data sources"""

    def __init__(self, domain_name: str):
        self.domain_name = domain_name
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'UnifiedAttributionFramework/1.0 (Educational/Research)'
        })

    def fetch_with_retry(self, url: str, max_retries: int = 3) -> Optional[Dict]:
        """Fetch data with retry logic"""
        for attempt in range(max_retries):
            try:
                response = self.session.get(url, timeout=10)
                response.raise_for_status()
                return response.json()
            except Exception as e:
                print(f"  Attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    time.sleep(2)
                else:
                    return None
        return None

class PubChemAdapter(RealDataAdapter):
    """
    PubChem - NIH chemical compound database
    Source: https://pubchem.ncbi.nlm.nih.gov/docs/pug-rest
    No API key required
    """

    def __init__(self):
        super().__init__("pubchem_chemistry")
        self.base_url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"

    def get_compound_properties(self, compound_names: List[str]) -> Dict[str, Any]:
        """Get chemical properties for compounds"""
        properties_data = []

        print(f"\n🧪 Fetching real chemistry data from PubChem (NIH)...")

        for name in compound_names[:10]:  # Limit to 10 for demo
            url = f"{self.base_url}/compound/name/{name}/property/MolecularWeight,MolecularFormula,IUPACName/JSON"
            data = self.fetch_with_retry(url)

            if data and 'PropertyTable' in data:
                props = data['PropertyTable']['Properties'][0]
                properties_data.append({
                    'compound': name,
                    'molecular_weight': props.get('MolecularWeight', 0),
                    'formula': props.get('MolecularFormula', ''),
                    'cid': props.get('CID', 0)
                })
                print(f"  ✓ {name}: {props.get('MolecularFormula', 'N/A')}")

        return {'compounds': properties_data, 'source': 'PubChem/NIH'}

class NOAAWeatherAdapter(RealDataAdapter):
    """
    NOAA Weather API - US National Weather Service
    Source: https://www.weather.gov/documentation/services-web-api
    No API key required
    """

    def __init__(self):
        super().__init__("noaa_climate")
        self.base_url = "https://api.weather.gov"

    def get_weather_stations_data(self, state: str = "CA") -> Dict[str, Any]:
        """Get real weather station data"""
        print(f"\n🌦️  Fetching real climate data from NOAA...")

        # Get stations
        url = f"{self.base_url}/stations?state={state}&limit=10"
        data = self.fetch_with_retry(url)

        stations_data = []
        if data and 'features' in data:
            for station in data['features'][:5]:
                props = station['properties']
                coords = station['geometry']['coordinates']

                stations_data.append({
                    'station_id': props.get('stationIdentifier', 'N/A'),
                    'name': props.get('name', 'N/A'),
                    'latitude': coords[1],
                    'longitude': coords[0],
                    'elevation': props.get('elevation', {}).get('value', 0)
                })
                print(f"  ✓ {props.get('name', 'N/A')[:40]}")

        return {'stations': stations_data, 'source': 'NOAA/NWS'}

class NASAAdapter(RealDataAdapter):
    """
    NASA Open Data - No key needed for basic endpoints
    Source: https://api.nasa.gov
    """

    def __init__(self):
        super().__init__("nasa_space")
        self.base_url = "https://api.nasa.gov"
        # Use DEMO_KEY which is rate-limited but requires no signup
        self.api_key = "DEMO_KEY"

    def get_near_earth_objects(self, date: str = "2024-01-01") -> Dict[str, Any]:
        """Get Near Earth Object data"""
        print(f"\n🚀 Fetching real space data from NASA...")

        url = f"{self.base_url}/neo/rest/v1/feed?start_date={date}&end_date={date}&api_key={self.api_key}"
        data = self.fetch_with_retry(url)

        neo_data = []
        if data and 'near_earth_objects' in data:
            for date_key, objects in data['near_earth_objects'].items():
                for obj in objects[:5]:
                    neo_data.append({
                        'name': obj.get('name', 'N/A'),
                        'diameter_km': obj.get('estimated_diameter', {}).get('kilometers', {}).get('estimated_diameter_max', 0),
                        'velocity_kmh': float(obj.get('close_approach_data', [{}])[0].get('relative_velocity', {}).get('kilometers_per_hour', 0)),
                        'distance_km': float(obj.get('close_approach_data', [{}])[0].get('miss_distance', {}).get('kilometers', 0)),
                        'hazardous': obj.get('is_potentially_hazardous_asteroid', False)
                    })
                    hazard = "⚠️" if obj.get('is_potentially_hazardous_asteroid') else "✓"
                    print(f"  {hazard} {obj.get('name', 'N/A')[:40]}")

        return {'asteroids': neo_data, 'source': 'NASA/JPL'}

class USGSEarthquakeAdapter(RealDataAdapter):
    """
    USGS Earthquake Data
    Source: https://earthquake.usgs.gov/fdsnws/event/1/
    No API key required
    """

    def __init__(self):
        super().__init__("usgs_earthquakes")
        self.base_url = "https://earthquake.usgs.gov/fdsnws/event/1"

    def get_recent_earthquakes(self, min_magnitude: float = 5.0, days: int = 7) -> Dict[str, Any]:
        """Get recent significant earthquakes"""
        print(f"\n🌍 Fetching real earthquake data from USGS...")

        url = f"{self.base_url}/query?format=geojson&minmagnitude={min_magnitude}&limit=20"
        data = self.fetch_with_retry(url)

        earthquake_data = []
        if data and 'features' in data:
            for quake in data['features'][:10]:
                props = quake['properties']
                coords = quake['geometry']['coordinates']

                earthquake_data.append({
                    'magnitude': props.get('mag', 0),
                    'place': props.get('place', 'N/A'),
                    'latitude': coords[1],
                    'longitude': coords[0],
                    'depth_km': coords[2],
                    'time': props.get('time', 0)
                })
                print(f"  ✓ M{props.get('mag', 0):.1f} - {props.get('place', 'N/A')[:50]}")

        return {'earthquakes': earthquake_data, 'source': 'USGS'}

class DataGovAdapter(RealDataAdapter):
    """
    Data.gov - US Government Open Data
    Source: https://catalog.data.gov/api/3/
    No API key required
    """

    def __init__(self):
        super().__init__("datagov_general")
        self.base_url = "https://catalog.data.gov/api/3/action"

    def search_datasets(self, query: str, rows: int = 10) -> Dict[str, Any]:
        """Search for datasets"""
        print(f"\n📊 Searching Data.gov for: {query}...")

        url = f"{self.base_url}/package_search?q={query}&rows={rows}"
        data = self.fetch_with_retry(url)

        datasets = []
        if data and data.get('success') and 'result' in data:
            for pkg in data['result'].get('results', [])[:5]:
                datasets.append({
                    'title': pkg.get('title', 'N/A'),
                    'organization': pkg.get('organization', {}).get('title', 'N/A'),
                    'num_resources': len(pkg.get('resources', [])),
                    'metadata_created': pkg.get('metadata_created', 'N/A')
                })
                print(f"  ✓ {pkg.get('title', 'N/A')[:60]}")

        return {'datasets': datasets, 'source': 'Data.gov'}

class NIHReporterAdapter(RealDataAdapter):
    """
    NIH RePORTER - Research funding and publications
    Source: https://api.reporter.nih.gov
    No API key required
    """

    def __init__(self):
        super().__init__("nih_research")
        self.base_url = "https://api.reporter.nih.gov/v2"

    def search_projects(self, query: str, limit: int = 10) -> Dict[str, Any]:
        """Search NIH funded research projects"""
        print(f"\n🔬 Fetching NIH research data...")

        url = f"{self.base_url}/projects/search"
        payload = {
            "criteria": {
                "project_title": query,
                "fiscal_years": [2024, 2023]
            },
            "offset": 0,
            "limit": limit
        }

        try:
            response = self.session.post(url, json=payload, timeout=10)
            data = response.json()

            projects = []
            if 'results' in data:
                for proj in data['results'][:5]:
                    projects.append({
                        'title': proj.get('project_title', 'N/A'),
                        'pi_name': proj.get('principal_investigators', [{}])[0].get('full_name', 'N/A') if proj.get('principal_investigators') else 'N/A',
                        'organization': proj.get('organization', {}).get('org_name', 'N/A'),
                        'award_amount': proj.get('award_amount', 0),
                        'fiscal_year': proj.get('fiscal_year', 0)
                    })
                    print(f"  ✓ {proj.get('project_title', 'N/A')[:60]}")

            return {'projects': projects, 'source': 'NIH RePORTER'}
        except Exception as e:
            print(f"  Error: {e}")
            return {'projects': [], 'source': 'NIH RePORTER', 'error': str(e)}


def test_all_adapters():
    """Test all real data adapters"""
    print("="*70)
    print("TESTING REAL SCIENTIFIC DATA SOURCES")
    print("="*70)

    results = {}

    # Test PubChem
    try:
        pubchem = PubChemAdapter()
        results['pubchem'] = pubchem.get_compound_properties([
            'aspirin', 'caffeine', 'glucose', 'water', 'ethanol'
        ])
    except Exception as e:
        print(f"PubChem error: {e}")
        results['pubchem'] = {'error': str(e)}

    # Test NOAA
    try:
        noaa = NOAAWeatherAdapter()
        results['noaa'] = noaa.get_weather_stations_data("CA")
    except Exception as e:
        print(f"NOAA error: {e}")
        results['noaa'] = {'error': str(e)}

    # Test NASA
    try:
        nasa = NASAAdapter()
        results['nasa'] = nasa.get_near_earth_objects("2024-01-01")
    except Exception as e:
        print(f"NASA error: {e}")
        results['nasa'] = {'error': str(e)}

    # Test USGS
    try:
        usgs = USGSEarthquakeAdapter()
        results['usgs'] = usgs.get_recent_earthquakes(min_magnitude=5.0)
    except Exception as e:
        print(f"USGS error: {e}")
        results['usgs'] = {'error': str(e)}

    # Test Data.gov
    try:
        datagov = DataGovAdapter()
        results['datagov'] = datagov.search_datasets("climate")
    except Exception as e:
        print(f"Data.gov error: {e}")
        results['datagov'] = {'error': str(e)}

    # Test NIH
    try:
        nih = NIHReporterAdapter()
        results['nih'] = nih.search_projects("cancer")
    except Exception as e:
        print(f"NIH error: {e}")
        results['nih'] = {'error': str(e)}

    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    for source, data in results.items():
        status = "✓" if 'error' not in data else "✗"
        print(f"{status} {source.upper()}: {data.get('source', 'Error')}")

    return results

if __name__ == "__main__":
    results = test_all_adapters()
