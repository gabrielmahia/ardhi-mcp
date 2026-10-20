"""ArdhiMCP — Kenya Land Administration Navigation (5 tools). All data DEMO."""
from __future__ import annotations

from typing import Annotated, Optional

from fastmcp import FastMCP
from pydantic import Field

mcp = FastMCP(name="ardhi-mcp", instructions="Kenya land administration tools. DEMO data only.")

@mcp.tool(name="title_search_guide", description="Steps to run an official land title search in Kenya: the county land registry or ArdhiSasa, Form RL1, the fee, documents and what the result confirms. Use when someone is about to buy, sell or otherwise transact in land and needs to check the title first. county and parcel_number are only echoed back; the steps are the same everywhere. Returns the source label, county, parcel, numbered steps, documents needed, the ArdhiSasa portal and a reminder to search before any transaction. Static guide labelled DEMO: verify at lands.go.ke. Read-only; no side effects.", annotations={"readOnlyHint": True, "openWorldHint": False})
def title_search_guide(county: str | None = Field(None, description="Kenyan county where the land is registered, e.g. 'Kiambu', 'Nairobi'."), parcel_number: str | None = Field(None, description="Land parcel or title deed number, e.g. 'KIAMBU/TOWNSHIP/1234'.")) -> dict:
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

@mcp.tool(name="land_rates_query", description="Indicative annual land rates in KES per square metre for a county and land use. Use when someone asks roughly what land rates they will pay. Only some counties are in the sample table; any other county gets a generic default and rate_basis says so. land_use of residential or commercial selects the rate; any other land use returns the residential rate. Returns the source label, county, land_use, rate_basis, rate_estimate, how to pay and a note that counties set rates annually. Indicative figures labelled DEMO: verify with the county lands office. Read-only; no side effects.", annotations={"readOnlyHint": True, "openWorldHint": False})
def land_rates_query(county: Annotated[str, Field(description="County name such as Nairobi or Mombasa; counties not in the sample table get a generic default.")], land_use: Annotated[str | None, Field(description="residential (default) or commercial; anything else returns the residential rate.")] = "residential") -> dict:
    """Return land rates, valuation, and annual charge data for Kenya counties."""
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
            "land_use": land_use, "rate_basis": "county table" if county_key in RATES else "generic default", "rate_estimate": rate_data.get(land_use.lower(), rate_data["residential"]),
            "payment": "Pay at county revenue offices or via county eCitizen portal",
            "note": "Rates set by county government annually. Verify at your county lands office."}

@mcp.tool(name="subdivision_process", description="Steps, typical fees and timeline to subdivide land in Kenya: survey, physical planning approval, documents, technical committee approval and new titles. Use when someone plans to subdivide a parcel. county and purpose are accepted but do not change the result. Returns the source label, numbered steps, typical fees (survey, physical planning, registration), a timeline of 3 to 12 months and a note on agricultural land consent. Indicative figures labelled DEMO: confirm with the county. Read-only; no side effects.", annotations={"readOnlyHint": True, "openWorldHint": False})
def subdivision_process(county: str | None = Field(None, description="Optional filter for county. Pass None to return all results."), purpose: str | None = Field(None, description="Optional filter for purpose. Pass None to return all results.")) -> dict:
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

@mcp.tool(name="land_dispute_paths", description="Routes to resolve a land dispute in Kenya for boundary, ownership, eviction or informal-tenure disputes, with the offices to approach in order (surveyor, land adjudication, National Land Commission, the Environment and Land Court, legal aid). Use when someone describes a land dispute and asks where to go. dispute_type selects the pathway; county is an optional filter label. Returns the resolution_pathway plus NLC, ELC and legal-aid details and a not-legal-advice disclaimer. Static guide labelled DEMO: consult an advocate. Read-only; no side effects.", annotations={"readOnlyHint": True, "openWorldHint": False})
def land_dispute_paths(dispute_type: Annotated[str, Field(description="boundary, ownership, eviction or informal.")], county: str | None = Field(None, description="Optional filter for county. Pass None to return all results.")) -> dict:
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

@mcp.tool(name="land_rights_query", description="Explain land rights in Kenya: ownership, community land, government land and adverse possession, with the legal basis. Use when someone asks what rights they have over land. Keywords in topic select entries; if none match it returns a pointer to the Land Act at kenyalaw.org. Returns the source label, topic, the rights and a not-legal-advice disclaimer. Static summary labelled DEMO: consult an advocate or the NLC. Read-only; no side effects.", annotations={"readOnlyHint": True, "openWorldHint": False})
def land_rights_query(topic: Annotated[str, Field(description="Rights topic such as ownership, community_land, government_land or adverse_possession.")]) -> dict:
    """Return land ownership rights, women's land rights, and community land information."""
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

def main() -> None:
    """Console entry point."""
    mcp.run()
