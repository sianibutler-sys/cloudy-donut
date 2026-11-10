# Cloudy Donut Co. concept

A concept rebuild of cloudydonut.com by Siani Creates, made for a cold pitch. It's private by design: noindex meta tag, `X-Robots-Tag` header, `robots.txt` disallow, and a "Concept by Siani Creates" label on every page.

## Deploy

1. Create a new repo `cloudy-donut` on GitHub (sianibutler-sys) and push this folder as-is.
2. In Cloudflare: Workers & Pages > Create > Pages > Connect to Git > pick the repo.
   - Framework preset: None
   - Build command: leave empty
   - Output directory: `/`
3. Deploy. The site runs right away on the JSON files in `/data`. No Airtable is needed for the demo.

To preview locally, double-click `index.html`, or run `python3 -m http.server` in this folder and open http://localhost:8000.

## How the pieces fit

| File | What it does |
| --- | --- |
| `index.html`, `styles.css`, `app.js` | The site. Palette lives in `:root` at the top of `styles.css`. |
| `data/flavors.json` | All 44 flavors, copied from cloudydonut.com/our-flavors, with filter tags. |
| `data/site.json` | Weekly lineup, locations and hours, tour stops, links. |
| `data/fallback.js` | Copy of both JSON files so the page previews from a double-click. Regenerate it if you edit the JSON. |
| `functions/api/content.js` | Reads lineup, hours and tour live from Airtable once it's connected. Falls back to `/data` until then. |
| `functions/api/submit.js` | Saves all four forms (newsletter, tour alert, cake waitlist, catering) to one Airtable table. |

Photos load straight from Cloudy's own Wix media CDN, so nothing of theirs is copied into the repo.

## Connecting Airtable (only if they sign)

Set these in Cloudflare Pages > Settings > Variables, in Cloudy's own account: `AIRTABLE_TOKEN`, `AIRTABLE_BASE`, optional `AIRTABLE_TABLE` (default `Submissions`), optional `NOTIFY_WEBHOOK` for catering emails. The expected table and field names are in the comment at the top of each function.

## Before you send it

- Open it in a browser and confirm the photos load. They couldn't be checked from the build environment.
- Design direction: their real brand colors from cloudydonut.com (cream #FFFBED, mint #ABDBC6, sage #80A495, charcoal) and their Caudex serif, pushed toward the founders' Instagram energy: film grain, cinematic photography, 7Streams-style condensed headlines (Anton), and pop-ups styled like their "Cloudy Donut Presents" flyers.
- The splash uses SVG fractal-noise filters to render real volumetric clouds, then reveals the logo and their tagline. It plays once per visit and is skipped for reduced-motion users.
- Founder section is typographic on purpose. Ask Derrick and Zewiditu for portraits they'd like used before adding any photos of them.
- The Newark pop-up (Sat Nov 14) comes from their Instagram flyer. After that date passes, the flyer falls back to "On Tour" until a new dated stop is added.
- The weekly lineup is a sample of 8 real flavors pictured on their homepage. Swap in the current week from their Instagram if you can, since that's the strongest live proof.
- Find the "Order ahead" link. Their FAQ mentions DoorDash, Grubhub and ordering direct, but the live provider isn't identifiable from the site. Put it in `links.order` in `site.json`. Until then the button shows a placeholder note.
- Tour dates for Delaware, Detroit, Chicago, New Orleans and Los Angeles are blank on purpose. Press reported the cities but no dates.
- Their site has a few contradictions the new build fixes by having one source of truth. Catering notice is listed as both 14 and 7 days (this demo uses 14). The FAQ lists two NYC shops and a Federal Hill merch shop that the Locations page doesn't show. Raise these gently in the pitch as cleanup the build handles.
