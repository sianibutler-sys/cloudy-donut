// Cloudflare Pages Function: GET /api/config
// Public, browser-safe settings read from Cloudflare environment variables.
//   CARTO_API_KEY  CARTO basemaps key (Text variable). It is visible in tile URLs by design;
//                  the key's website (Referer) restriction in CARTO is what protects it.
export async function onRequestGet({ env }) {
  return new Response(JSON.stringify({ cartoKey: env.CARTO_API_KEY || "" }), {
    headers: { "Content-Type": "application/json", "Cache-Control": "public, max-age=300" },
  });
}
