// Cloudflare Pages Function: POST /api/submit
// Writes every site form to one Airtable table and (optionally) emails a notification.
// Env vars (Cloudflare Pages > Settings > Variables):
//   AIRTABLE_TOKEN   personal access token with data.records:write on the base
//   AIRTABLE_BASE    base ID (app...)
//   AIRTABLE_TABLE   table name, default "Submissions"
//   NOTIFY_WEBHOOK   optional URL (e.g. an Airtable automation or email service) to ping on catering requests

const FORMS = new Set(["newsletter", "tour_alert", "ship_waitlist", "catering"]);

export async function onRequestPost({ request, env }) {
  let body;
  try { body = await request.json(); } catch { return json({ error: "Bad request" }, 400); }
  const { form, fields } = body || {};
  if (!FORMS.has(form) || typeof fields !== "object") return json({ error: "Unknown form" }, 400);
  if (!fields.email || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(fields.email)) return json({ error: "Email required" }, 400);

  if (!env.AIRTABLE_TOKEN || !env.AIRTABLE_BASE) return json({ error: "Not configured" }, 503);

  const clean = {};
  for (const [k, v] of Object.entries(fields)) clean[k] = String(v).slice(0, 2000);

  const record = {
    Form: form,
    Email: clean.email,
    Name: [clean.first_name, clean.last_name].filter(Boolean).join(" "),
    Details: JSON.stringify(clean, null, 2),
    Status: "New",
  };

  const table = encodeURIComponent(env.AIRTABLE_TABLE || "Submissions");
  const r = await fetch(`https://api.airtable.com/v0/${env.AIRTABLE_BASE}/${table}`, {
    method: "POST",
    headers: { Authorization: `Bearer ${env.AIRTABLE_TOKEN}`, "Content-Type": "application/json" },
    body: JSON.stringify({ records: [{ fields: record }], typecast: true }),
  });
  if (!r.ok) return json({ error: "Save failed" }, 502);

  if (form === "catering" && env.NOTIFY_WEBHOOK) {
    await fetch(env.NOTIFY_WEBHOOK, {
      method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ form, ...clean }),
    }).catch(() => {});
  }
  return json({ ok: true });
}

const json = (data, status = 200) =>
  new Response(JSON.stringify(data), { status, headers: { "Content-Type": "application/json" } });
