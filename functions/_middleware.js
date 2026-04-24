export async function onRequest({ request, next, env }) {
  const auth = request.headers.get("Authorization");
  if (!env.SITE_PASSWORD) {
    return new Response("Server misconfigured: SITE_PASSWORD not set", { status: 500 });
  }
  const expected = "Basic " + btoa("aacr:" + env.SITE_PASSWORD);
  if (auth === expected) {
    return next();
  }
  return new Response("Authentication required", {
    status: 401,
    headers: {
      "WWW-Authenticate": 'Basic realm="AACR 2026", charset="UTF-8"',
      "Cache-Control": "no-store",
    },
  });
}
