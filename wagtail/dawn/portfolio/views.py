import hashlib
import hmac
import time
import urllib.parse

from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

PORTAL_TOKEN_COOKIE = "portal_token"
PORTAL_TOKEN_LIFETIME = 8 * 3600  # 8 hours


def _make_portal_token(user_id):
    timestamp = int(time.time())
    msg = f"{user_id}:{timestamp}".encode()
    sig = hmac.new(settings.SECRET_KEY.encode(), msg, hashlib.sha256).hexdigest()
    return f"{user_id}:{timestamp}:{sig}"


def _validate_portal_token(token_str):
    try:
        user_id, timestamp, sig = token_str.split(":", 2)
        if time.time() - int(timestamp) > PORTAL_TOKEN_LIFETIME:
            return False
        msg = f"{user_id}:{timestamp}".encode()
        expected = hmac.new(settings.SECRET_KEY.encode(), msg, hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected, sig)
    except Exception:
        return False


def _is_safe_next(url):
    try:
        parsed = urllib.parse.urlparse(url)
        if parsed.scheme not in ("http", "https"):
            return False
        host = parsed.netloc.split(":")[0]  # strip port
        return (
            host == "localhost"
            or host.endswith(".localhost")
            or host.endswith(".nip.io")
        )
    except Exception:
        return False


def _gate_html(gate_url):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Demo Access Required</title>
<style>
  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: system-ui, -apple-system, sans-serif;
    background: #0f1117;
    color: #e2e6f0;
  }}
  .card {{
    background: #1a1d27;
    border: 1px solid #2a2e3f;
    border-radius: 12px;
    padding: 2.5rem 2rem;
    max-width: 400px;
    width: 100%;
    text-align: center;
  }}
  .lock {{ font-size: 2.5rem; margin-bottom: 1.25rem; }}
  h1 {{ font-size: 1.25rem; font-weight: 600; margin-bottom: 0.5rem; }}
  p {{ font-size: 14px; color: #7a82a0; line-height: 1.6; margin-bottom: 1.75rem; }}
  a {{
    display: inline-block;
    background: #f5a623;
    color: #1a1d27;
    font-weight: 600;
    font-size: 14px;
    padding: 0.6rem 1.5rem;
    border-radius: 6px;
    text-decoration: none;
  }}
  a:hover {{ background: #e0941a; }}
  .sub {{ display: block; margin-top: 1rem; font-size: 13px; color: #7a82a0; }}
</style>
</head>
<body>
<div class="card">
  <div class="lock">&#128274;</div>
  <h1>Demo access required</h1>
  <p>This showroom is restricted to authorized users.<br>
  Sign in to the Portal to continue.</p>
  <a href="{gate_url}">Sign in to Portal</a>
  <span class="sub">After signing in, you will be redirected back here.</span>
</div>
</body>
</html>"""


@csrf_exempt
def forward_auth_showrooms(request):
    """
    Caddy forward_auth endpoint. Returns 200 to allow, 401 + gate page to deny.
    Checks: (1) portal_token cookie signed with SECRET_KEY, (2) Dawn admin session.
    """
    # Dawn session present (admin is browsing catalystdev.localhost — same session forwarded)
    if request.user.is_authenticated:
        return HttpResponse(status=200)

    # Portal token cookie set by the redirect-based auth flow
    token_str = request.COOKIES.get(PORTAL_TOKEN_COOKIE, "")
    if token_str and _validate_portal_token(token_str):
        return HttpResponse(status=200)

    # Build gate URL so the button sends users through the portal flow with
    # the original showroom URL as the post-auth redirect target.
    forwarded_host = request.META.get("HTTP_X_FORWARDED_HOST", "")
    forwarded_uri = request.META.get("HTTP_X_FORWARDED_URI", "/")
    gate_base = getattr(settings, "PORTAL_GATE_BASE_URL", "http://catalystdev.localhost")
    if forwarded_host:
        next_url = urllib.parse.quote(f"http://{forwarded_host}{forwarded_uri}")
        gate_url = f"{gate_base}/portal/gate/?next={next_url}"
    else:
        gate_url = f"{gate_base}/portal/gate/"

    return HttpResponse(_gate_html(gate_url), status=401, content_type="text/html")


@csrf_exempt
def portal_gate(request):
    """
    If the user is authenticated to Dawn, issue a signed portal token and
    redirect to the showroom's /_portal/ callback to set the cookie.
    Otherwise redirect to the Dawn login page.
    """
    next_url = request.GET.get("next", "http://catalystdev.localhost/")
    if not _is_safe_next(next_url):
        next_url = "http://catalystdev.localhost/"

    if not request.user.is_authenticated:
        encoded_gate = urllib.parse.quote(f"/portal/gate/?next={urllib.parse.quote(next_url)}")
        return HttpResponseRedirect(f"/admin/login/?next={encoded_gate}")

    token = _make_portal_token(request.user.pk)
    parsed = urllib.parse.urlparse(next_url)
    callback = (
        f"{parsed.scheme}://{parsed.netloc}/_portal/"
        f"?token={urllib.parse.quote(token)}"
        f"&next={urllib.parse.quote(next_url)}"
    )
    return HttpResponseRedirect(callback)


@csrf_exempt
def portal_set(request):
    """
    Caddy proxies /_portal/* on every showroom to this endpoint.
    Validates the token, sets a portal_token cookie for the showroom domain
    (the browser sees the response as coming from the showroom), then redirects.
    """
    token_str = request.GET.get("token", "")
    next_url = request.GET.get("next", "/")
    if not _is_safe_next(next_url):
        next_url = "/"

    if not token_str or not _validate_portal_token(token_str):
        encoded_next = urllib.parse.quote(next_url)
        gate_base = getattr(settings, "PORTAL_GATE_BASE_URL", "http://catalystdev.localhost")
        return HttpResponseRedirect(
            f"{gate_base}/portal/gate/?next={encoded_next}"
        )

    response = HttpResponseRedirect(next_url)
    response.set_cookie(
        PORTAL_TOKEN_COOKIE,
        token_str,
        max_age=PORTAL_TOKEN_LIFETIME,
        httponly=True,
        samesite="Lax",
        secure=False,
    )
    return response
