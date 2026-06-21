"""ArdhiMCP — Kenya Land Administration Navigation (5 tools). All data DEMO."""
from __future__ import annotations
from typing import Annotated, Optional
from fastmcp import FastMCP

mcp = FastMCP(name="ardhi-mcp", instructions="Kenya land administration tools. DEMO data only.")

@mcp.tool(name="title_search_guide", description="Guide to searching land titles at Kenya Land Registry. DEMO.", annotations={"readOnlyHint": True, "openWorldHint": False})
def title_search_guide(county: Annotated[Optional[str], "Kenyan county where the land is registered, e.g. 'Kiambu', 'Nairobi'."] = None, parcel_number: Annotated[Optional[str], "Land parcel or title deed number, e.g. 'KIAMBU/TOWNSHIP/1234'."] = None) -> dict:
    return {"source": "DEMO — lands.go.ke for official process", "county": county,
            "parcel": parcel_number,
            "steps": [
                "1. Visit county Land Registry (or use ArdhiSasa portal: ardhisasa.go.ke)",
                "2. Fill Form RL1 (application for official search). Fee: KES 500",
                "3. Provide parcel number (from title deed or survey map)",
                "4. Collect official search result within 5-7 working days",
                "5. Search result confirms: owner, encumbrances, caveats, charges",
            ],
            "documents_needed": ["National ID or Passport", "Parcel number/LR number", "KES 500 fee"],
            "ardhisasa": "ardhisasa.go.ke — online search available for some counties",
            "note": "Always conduct official search before any land transaction. DEMO — verify at lands.go.ke"}

@mcp.tool(name="land_rates_query", description="Land rates and rent for Kenya counties. DEMO.", annotations={"readOnlyHint": True, "openWorldHint": False})
def land_rates_query(county: str, land_use: Optional[str] = "residential") -> dict:
    RATES = {
        "nairobi": {"residential": "KES 0.125–1.00 per m² per year (varies by zone)",
                    "commercial":  "KES 0.50–4.00 per m² per year (CBD higher)"},
        "mombasa": {"residential": "KES 0.10–0.80 per m² per year",
                    "commercial":  "KES 0.40–2.00 per m² per year"},
        "default": {"residential": "KES 0.05–0.50 per m² per year (county-specific)",
                    "commercial":  "KES 0.20–1.50 per m² per year"},
    }
    county_key = county.lower()
    rate_data = RATES.get(county_key, RATES["default"])
    return {"source": "DEMO — county land rates published in annual county budgets", "county": county,
            "land_use": land_use, "rate_estimate": rate_data.get(land_use.lower(), rate_data["residential"]),
            "payment": "Pay at county revenue offices or via county eCitizen portal",
            "note": "Rates set by county government annually. Verify at your county lands office."}

@mcp.tool(name="subdivision_process", description="Land subdivision application process in Kenya. DEMO.", annotations={"readOnlyHint": True, "openWorldHint": False})
def subdivision_process(county: Annotated[Optional[str], "Optional filter for county. Pass None to return all results."] = None, purpose: Annotated[Optional[str], "Optional filter for purpose. Pass None to return all results."] = None) -> dict:
    return {"source": "DEMO — lands.go.ke and county governments",
            "steps": [
                "1. Survey: Engage licensed surveyor. Survey report + mutation form",
                "2. Physical Planning: Apply for subdivision approval at county physical planning dept.",
                "3. Documents: Original title, ID, mutation form, scheme layout plan, fees",
                "4. Technical Committee approval (2–4 weeks typical)",
                "5. New survey plan submitted to Survey of Kenya",
                "6. New title deeds issued for each subdivision",
            ],
            "typical_fees": {"survey": "KES 30,000–100,000+", "physical_planning": "KES 5,000–20,000", "registration": "KES 2,000–5,000"},
            "timeline": "3–12 months depending on county and complexity",
            "note": "Agricultural land subdivision may require Ministry of Agriculture consent."}

@mcp.tool(name="land_dispute_paths", description="Land dispute resolution pathways in Kenya. DEMO.", annotations={"readOnlyHint": True, "openWorldHint": False})
def land_dispute_paths(dispute_type: str, county: Annotated[Optional[str], "Optional filter for county. Pass None to return all results."] = None) -> dict:
    PATHS = {
        "boundary": ["Engage licensed surveyor for re-survey", "County Land Adjudication Officer", "Environment and Land Court (ELC)"],
        "ownership": ["National Land Commission (NLC) — historical injustices", "ELC for formal title disputes", "High Court"],
        "eviction":  ["Legal aid — LSK Pro Bono Clinic", "National Legal Aid Service (NLAS)", "ELC urgent application"],
        "informal":  ["Land Adjudication Committee", "District Land Control Board", "ELC if unresolved"],
    }
    dt = dispute_type.lower()
    path = next((v for k, v in PATHS.items() if k in dt), PATHS["ownership"])
    return {"source": "DEMO — nlc.go.ke, judiciary.go.ke", "dispute_type": dispute_type, "county": county,
            "resolution_pathway": path,
            "nlc": "National Land Commission — nlc.go.ke — historical/public land issues",
            "elc": "Environment and Land Court — judiciary.go.ke — formal title disputes",
            "legal_aid": "NLAS free legal aid: nlas.go.ke",
            "disclaimer": "Not legal advice. Consult an advocate."}

@mcp.tool(name="land_rights_query", description="Land rights under Kenya Constitution 2010 and Land Act 2012. DEMO.", annotations={"readOnlyHint": True, "openWorldHint": False})
def land_rights_query(topic: str) -> dict:
    RIGHTS = {
        "ownership": "Every Kenyan citizen has right to own land anywhere in Kenya (Art 40, Constitution 2010).",
        "community_land": "Community land vested in and managed by communities per Community Land Act 2016.",
        "government_land": "Public land vested in the national and county governments managed by NLC.",
        "adverse_possession": "12 years continuous possession may give right to title under Limitation of Actions Act.",
        "inheritance": "Law of Succession Act governs inheritance. Spouses and children protected regardless of gender.",
        "foreign_ownership": "Non-citizens may hold leasehold land (up to 99 years), not freehold.",
        "eviction": "Forced evictions without court order unconstitutional. Art 40(3) protects against arbitrary deprivation.",
    }
    t = topic.lower()
    matched = {k: v for k, v in RIGHTS.items() if k in t or any(w in t for w in k.split("_"))}
    return {"source": "DEMO — Kenya Land Act 2012, Constitution 2010 (kenyalaw.org)", "topic": topic,
            "rights": matched or {"general": "Review Land Act 2012 at kenyalaw.org"},
            "disclaimer": "Not legal advice. Consult an advocate or NLC."}
