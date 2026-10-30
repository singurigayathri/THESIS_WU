"""Edit this file to change which companies the website tracks.
After editing, the data refreshes automatically (or run the workflow by hand).
Format: "Name shown on the website": "Yahoo Finance ticker"
"""
START_DATE = "2020-01-01"

LISTED = {
    "A1 Telekom Austria": "TKA.VI",
    "Deutsche Telekom": "DTE.DE",
    "Swisscom": "SCMN.SW",
    "Proximus": "PROX.BR",
    "Telia": "TELIA.ST",
    "Telenor": "TEL.OL",
    "Orange": "ORA.PA",
    "KPN": "KPN.AS",
    "Telefonica": "TEF.MC",
    "Hrvatski Telekom": "HT.ZA",
    "Telekom Slovenije": "TLSG.LJ",
    "Makedonski Telekom": "MPT.MK",   # often missing on Yahoo
}

# Market benchmark used for beta. Keep the word "STOXX" or "Index" in the name.
BENCHMARK = {"STOXX Europe 600": "^STOXX"}
