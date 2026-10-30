# A1 vs competitors: thesis website

A free website (GitHub Pages) that shows A1 vs competitors: OpCo view per country, global peers, volatility, beta, GARCH(1,1) and a regression.
A free GitHub job fetches Yahoo prices and recomputes GARCH every weekday evening. No server, no cost.

## One-time setup (about 10 minutes)

1. **Create a GitHub account** (github.com) if you do not have one.
2. **New repository**: click + > New repository. Name: `a1-thesis`. Choose **Public** (free GitHub Pages needs public). Click Create.
   *Public means anyone with the link can see the site and the files. Only put public-report figures in the Excel, nothing internal.*
3. **Upload the files**: in the new repo click "uploading an existing file". Unzip this package, open the `thesis-site` folder, select EVERYTHING inside it (including the `.github` folder, `docs`, `scripts`) and drag it in. Click Commit changes.
4. **Check the workflow file arrived**: in the repo you should see `.github/workflows/update.yml`. If the `.github` folder is missing (some browsers skip it):
   Add file > Create new file > type the name `.github/workflows/update.yml` > paste the text from `workflow_copy.txt` > Commit.
5. **Turn on the website**: Settings > Pages > Source: "Deploy from a branch" > Branch `main`, folder `/docs` > Save.
6. **Allow the job to save data**: Settings > Actions > General > Workflow permissions > "Read and write permissions" > Save.
7. **Run the job once**: Actions tab > "Update data" > Run workflow (green button). Wait about 2 minutes. If GitHub asks to enable workflows, click enable.
8. **Open your site**: `https://YOUR-USERNAME.github.io/a1-thesis/` (Settings > Pages shows the exact link). Reload after step 7 finished.

## Everyday use
- **Prices and GARCH** update by themselves every weekday evening. Data date is shown at the top of the site.
- **Fix or add a ticker**: open `scripts/tickers.py` on GitHub > pencil icon > edit > Commit. The job runs automatically after a change. The site shows which tickers have problems.
- **Fill OpCo data**: download `docs/data/opco_data.xlsx`, fill it in Excel (always fill the Source column), then in the repo open the `docs/data` folder > Add file > Upload files > the same file name > Commit. The site updates in a minute.
- **If the data date gets old**: GitHub can pause scheduled jobs on quiet repos. Run it by hand (step 7).

## What the site cannot do
- Yahoo is the only price source: some smaller exchanges (e.g. Skopje) may have no data.
- Returns are in local currency (SEK, NOK, CHF, EUR mixed): say so in the thesis limitations.
- Unlisted competitors (Telemach, Yettel, Vivacom, Telekom Srbija) appear only in the OpCo view.
