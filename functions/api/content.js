// Cloudflare Pages Function: GET /api/content
// Reads the weekly lineup, locations and tour from Airtable so staff never touch code.
// Falls back to /data/*.json when Airtable isn't configured, which is how the concept runs today.
//
// Airtable tables expected:
//   Flavors   (Slug, Name, Description, Image ID, Tags [multi-select], Contains, This Week [checkbox], Active [checkbox])
//   Locations (Slug, Name, City, Address, Phone, Hours JSON, Hours Label, Note, Lat, Lng, Order)
//   Tour      (City, Date [YYYY-MM-DD], Time, Address, Venue, Status [announced | sold_out], Order)
//   Settings  (Key, Value)  e.g. week_of, lineup_also, order_link, flyer_image, prices

export async function onRequestGet({ env, request }) {
  const origin = new URL(request.url).origin;
  if (!env.AIRTABLE_TOKEN || !env.AIRTABLE_BASE) {
    const [f, s] = await Promise.all([
      fetch(`${origin}/data/flavors.json`).then((r) => r.json()),
      fetch(`${origin}/data/site.json`).then((r) => r.json()),
    ]);
    return json({ ...f, ...s });
  }

  const get = async (table, params = "") => {
    const out = [];
    let offset = "";
    do {
      const r = await fetch(
        `https://api.airtable.com/v0/${env.AIRTABLE_BASE}/${encodeURIComponent(table)}?pageSize=100${params}${offset ? `&offset=${offset}` : ""}`,
        { headers: { Authorization: `Bearer ${env.AIRTABLE_TOKEN}` } }
      );
      if (!r.ok) throw new Error(table);
      const d = await r.json();
      out.push(...d.records.map((x) => x.fields));
      offset = d.offset || "";
    } while (offset);
    return out;
  };

  try {
    const [flavors, locations, tour, settings] = await Promise.all([
      get("Flavors", "&filterByFormula=" + encodeURIComponent("{Active}")),
      get("Locations", "&sort[0][field]=Order"),
      get("Tour", "&sort[0][field]=Order"),
      get("Settings"),
    ]);
    const set = Object.fromEntries(settings.map((s) => [s.Key, s.Value]));
    const data = {
      prices: JSON.parse(set.prices || "[]"),
      flavors: flavors.map((f) => ({
        id: f.Slug, name: f.Name, desc: f.Description || "", img: f["Image ID"],
        tags: f.Tags || [], contains: f.Contains || undefined,
      })),
      lineup: {
        week_of: set.week_of || "",
        also: set.lineup_also || "",
        flavors: flavors.filter((f) => f["This Week"]).map((f) => f.Slug),
      },
      locations: locations.map((l) => ({
        id: l.Slug, name: l.Name, city: l.City, address: l.Address, phone: l.Phone,
        hours: JSON.parse(l["Hours JSON"] || "{}"), hours_label: l["Hours Label"], note: l.Note, lat: l.Lat, lng: l.Lng,
      })),
      tour: { stops: tour.map((t) => ({ city: t.City, date: t.Date || "", time: t.Time || "", address: t.Address || "", venue: t.Venue || "", status: t.Status || "announced" })) },
      links: {
        order: set.order_link || "",
        flyer_image: set.flyer_image || "",
        instagram: "https://www.instagram.com/cloudydonuts/",
        facebook: "https://www.facebook.com/CloudyDonutCo",
        sevenstreams: "https://www.thesevenstreams.com",
      },
    };
    return json(data, 200, "public, max-age=300");
  } catch (e) {
    return json({ error: "Content unavailable" }, 502);
  }
}

const json = (data, status = 200, cache = "no-store") =>
  new Response(JSON.stringify(data), { status, headers: { "Content-Type": "application/json", "Cache-Control": cache } });
