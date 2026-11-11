// Cloudflare Pages Function: GET /api/instagram
// Returns the latest @cloudydonuts posts so the Pop-ups page row stays current on its own.
//
// Setup (once Cloudy connects their Instagram professional account):
//   IG_ACCESS_TOKEN  long-lived token from the Instagram API with Instagram Login (Secret)
//   IG_KV            optional KV namespace binding. When present, the function refreshes the
//                    token about once a week and keeps the new one there, so it never lapses.
// Without a token it returns 204 and the page falls back to the post list in data/site.json.

const FIELDS = "id,media_type,media_url,thumbnail_url,permalink,caption,timestamp";
const WEEK = 7 * 24 * 60 * 60 * 1000;

export async function onRequestGet({ env }) {
  let token = (env.IG_KV && (await env.IG_KV.get("token"))) || env.IG_ACCESS_TOKEN;
  if (!token) return new Response(null, { status: 204 });

  if (env.IG_KV) {
    const last = Number((await env.IG_KV.get("refreshed")) || 0);
    if (Date.now() - last > WEEK) {
      const r = await fetch(`https://graph.instagram.com/refresh_access_token?grant_type=ig_refresh_token&access_token=${token}`);
      if (r.ok) {
        const d = await r.json();
        token = d.access_token || token;
        await env.IG_KV.put("token", token);
        await env.IG_KV.put("refreshed", String(Date.now()));
      }
    }
  }

  const r = await fetch(`https://graph.instagram.com/me/media?fields=${FIELDS}&limit=12&access_token=${token}`);
  if (!r.ok) return new Response(null, { status: 204 });
  const d = await r.json();
  const posts = (d.data || []).map((p) => ({
    url: p.permalink,
    img: p.media_type === "VIDEO" ? p.thumbnail_url : p.media_url,
    kind: p.media_type === "VIDEO" ? "reel" : p.media_type === "CAROUSEL_ALBUM" ? "carousel" : "post",
    caption: (p.caption || "").split("\n")[0].slice(0, 140),
    date: p.timestamp,
  }));
  return new Response(JSON.stringify({ posts }), {
    headers: { "content-type": "application/json", "cache-control": "public, max-age=900" },
  });
}
