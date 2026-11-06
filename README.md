# podcast-site-tools

One-off Python scripts I wrote for a freelance client in 2019–2020: a podcast whose website was a
set of hand-maintained static HTML pages, one per episode, with no shared data layer behind them.
The scripts crawl and read those pages, bulk-edit them with BeautifulSoup, and consolidate the
episode metadata into XML and JSON so the catalog could be searched, filtered and re-generated.

This is preserved as it was, not a polished project. It was written before I used AI coding tools.

## Provenance

- **Client:** anonymized. The client's name, URLs and payment identifiers have been replaced with
  placeholders (`podcast.example`, `payments.example`, `BUTTON_ID`, `site_copy/`).
- **When it was written:** the file modification times on the original scripts run from
  **2019-08-06 to 2020-02-03**.
- **When this repository was created:** November 2026, from a backup of my old work directory.
  The commit dates reflect that. They are not the original dates.
- **What changed from the originals:** only placeholder substitutions of client names, URLs,
  payment-link identifiers, my Windows username and a contact line in a docstring (29 lines in 11
  files). Logic, formatting and line endings are untouched.
- **What is not included:** the client's site content (HTML pages, images, the episode data files)
  and the browser driver. The scripts expect those next to them, so they **cannot run as-is**.

## What's in `scripts/`

| Script | What it does |
|---|---|
| `scraper.py` | The main tool. A `PathList` class selects files; a `Scraper` class finds elements across many HTML files and bulk-updates their text or attributes with BeautifulSoup. Also includes a recursive Selenium crawler that collects every internal page of a JavaScript-rendered site. |
| `get_ep_sources.py` | Reads every `ep_*.html` page, pulls the embedded player's `src` out of the `<iframe>`, writes episode number → source, and reports missing episode numbers. |
| `make_xml.py` | Builds `episodes.xml` from a tab-separated, ordered episode list. |
| `insert_into_xml.py`, `fix_ets.py` | Merge the player sources into the XML and strip a redundant URL prefix. |
| `insert_ep_links.py` | Adds a link to each episode's page in the JSON data. |
| `escape_fslashes.py` | Escapes forward slashes in the player-source field of the JSON. |
| `find_missing_pix.py` | Reports episodes whose image file is missing. |
| `scan.py` | Checks pages for an expected "more episodes" link. |
| `insertTag.py`, `insertTag2.py`, `autoCopyPaste.py` | Inject an animated donate button and link into every page. |
| `fixDonationLinks.py`, `fixDonoLink.py` | Rewrite broken donation links across the site (a test run found most of them were wrong). |
| `proof.py` | Selenium check that every page's donate button points at the correct URL. |

## Known limitations

This is 2019-era code and it shows:

- Uses Selenium 3 APIs (`find_element_by_xpath`, `FirefoxProfile`) that Selenium 4 removed.
- Hard-coded paths and directory names, with debug `print` calls left in.
- `PathList.__init__` has a mutable default argument (`files=[]`).
- The crawler uses recursion instead of a loop, which would hit Python's recursion limit on a large site.
- No tests, no packaging, no error handling beyond a helper that prints exceptions.

It is not maintained.
