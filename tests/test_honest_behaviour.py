from ardhi_mcp import server

_fn = lambda name: (getattr(server, name).fn if hasattr(getattr(server, name), "fn") else getattr(server, name))


def test_a_county_outside_the_table_is_flagged_as_a_generic_default():
    assert _fn("land_rates_query")("Nairobi")["rate_basis"] == "county table"
    assert _fn("land_rates_query")("Wajir")["rate_basis"] == "generic default"
