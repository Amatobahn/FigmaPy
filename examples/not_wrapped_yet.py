"""Call an endpoint this version of figmapy has no generated method for.

    python examples/not_wrapped_yet.py

Figma ships API changes whenever it likes, and your installed version will sometimes be
a release behind. That should cost you a slightly uglier call, not a blocked afternoon.
"""

import figmapy

figma = figmapy.Figma()

print("generated from Figma spec", figmapy.FIGMA_SPEC_VERSION)

# 1. Any endpoint, generated or not. Returns the raw JSON.
me = figma.request("GET", "/v1/me")
print(me["handle"])

# 2. Parameters the generated signature does not know about go through too.
figma.request("GET", "/v1/files/aBc123XyZ", params={"depth": 1, "some_new_flag": True})

# 3. A field Figma shipped after this release is still readable on the model,
#    because the models accept unknown fields instead of dropping them.
#    file = figma.get_file(key)
#    file.someFieldFromNextMonth

# 4. And if even the client is in the way, the httpx client is right there.
response = figma.http.get("https://api.figma.com/v1/me", headers=figma.headers)
print(response.status_code)
