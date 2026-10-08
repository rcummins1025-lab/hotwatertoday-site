# Hot Water Today website

Static site for Hot Water Today (Kyle Cadotte). Home, Services and a thank-you page. No framework and no server; it runs on GitHub Pages, Netlify, Vercel or anything that serves files.

```
index.html          Home
services.html       Services
thanks.html         Shown after the lead form is sent
favicon.ico, favicon-32.png, apple-touch-icon.png   Flame "O" from the logo
logo.png            Original logo file, as supplied
assets/site.css     All styles
assets/site.js      Tap-through lead form
assets/logo.png     Logo with a transparent background (header and footer)
assets/mark-512.png Flame "O" on transparent, 512px
assets/fonts/       League Gothic + Libre Franklin (self-hosted, OFL)
assets/img/         Photos, each in several widths, WebP + JPEG
assets/og.jpg       Social preview image
build.py            Generates the three HTML pages
tools/images.py     Turns source photos into the files in assets/img
```

## Editing

Phone, email, towns, license number, form settings and all page copy live in `build.py`. Edit it and run:

```
python3 build.py
```

Commit the regenerated `*.html`. Don't hand-edit the HTML; the next build overwrites it.

## Lead form (FormSubmit)

The form posts to [FormSubmit](https://formsubmit.co). No account or API key.

**Current setting: TEST MODE.** Leads go only to `rcummins1025@gmail.com` with the subject `TEST Hot Water Today lead`. Nothing goes to info@ yet.

First use of any destination address needs a one-time activation:

1. Submit the form once on the live site.
2. FormSubmit emails an activation link to the destination address. Click it.
3. Submit again. That lead (and every one after) is delivered.

To switch to Kyle's inbox when Ryan approves:

1. In `build.py` set `FORM_TO = "info@hotwatertodaycorp.com"` and `FORM_SUBJECT = "New Hot Water Today lead"`.
2. `python3 build.py`, commit, push.
3. Submit once, and have Kyle click the activation email at info@.
4. Optional: FormSubmit's activation email gives a random alias. Use it in place of the address in `FORM_TO` to keep the email out of the page source.

Each lead email lists: Issue, Heater type, Water heater venting, Water heater location, Equipment size, How soon, Town, Name, Phone, Note. Venting and location are only asked (and only sent) for water heater requests; they are skipped when someone picks "Boiler or other plumbing". The form sends with JavaScript and then opens `thanks.html`. Without JavaScript it shows every question at once and FormSubmit redirects to `_next` (built from `SITE_URL`).

## Logo

`logo.png` is the logo as supplied (white background). `assets/logo.png` is the same logo trimmed, with the white removed so it sits on any light background, 800px wide. The footer is light gray because the logo's red and gray don't read on a dark background. The favicons are the flame "O" cut out of the logo.

Site colors come from the logo: red `#C30405` (sampled from "HOT") for buttons, the call bar and accents, charcoal `#4A4A4A` for text and headings, `#2A2A2A` for the dark photo panels, white backgrounds. They are set once at the top of `assets/site.css`.

## Photos

The three photos (heater close-up, utility room, work van) are AI-generated renders, approved by Kyle. They contain no people and no real branding. To replace one with a real photo:

```
python3 -m pip install pillow
python3 tools/images.py heater=~/Downloads/new-heater.jpg
```

Names: `heater` (home hero, 16:10), `utility` (services, 3:2), `van` (towns band, 3:2). Images are center-cropped to those ratios. Update the alt text in `IMAGES` in `build.py` to describe the new photo, then rebuild.

## Claims to confirm before launch

The proof strip says **Same-day service** and **Licensed in MA**. Confirm both with Kyle. Add his license number to `LICENSE_NO` in `build.py` to show it.

## Hosting

### GitHub Pages
Repo Settings → Pages → Deploy from a branch → `main` / `(root)`. The site appears at `https://rcummins1025-lab.github.io/hotwatertoday-site/`.

### Custom domain (later): www.hotwatertodaycorp.com

| Type  | Host | Value |
|-------|------|-------|
| CNAME | `www` | `rcummins1025-lab.github.io` |
| A     | `@`   | `185.199.108.153` |
| A     | `@`   | `185.199.109.153` |
| A     | `@`   | `185.199.110.153` |
| A     | `@`   | `185.199.111.153` |

Then set Custom domain to `www.hotwatertodaycorp.com` in Settings → Pages and tick Enforce HTTPS once the certificate is issued.
