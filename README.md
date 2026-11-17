# Alya Syifa photography site: setup guide

A fast static site in **English (main) and Italian**. It has a homepage plus one page each for your three main services.
There's no database and no monthly fee, and it's built to be hosted free on GitHub Pages.

```
index.html                    English homepage: intro, gallery, services, about, contact
graduation.html               English: graduation photos in Padova
couples-pre-wedding.html      English: couples & pre-wedding, Padova and Venice
brands.html                   English: brands, fashion, food, cafés, products
it/index.html                 Italian homepage
it/laurea.html                Italian versions of the three service pages
it/coppie-pre-wedding.html
it/brand.html
css/style.css                 design (colours at the top)
js/lightbox.js                full-screen photo viewer
images/                       web-sized photos from your three shoots, plus a placeholder for your About portrait
sitemap.xml, robots.txt       help Google find every page and photo
404.html                      "page not found" (both languages)
tools/prepare_photos.py       resizes your photos and writes the HTML for you
```

Every English page has an Italian twin. The two are linked so Google shows each visitor the right language. **When you change one, change its twin too.**

---

## Step 1: Fill in the placeholders

Open the folder in a text editor (VS Code is free). Your GitHub username, Instagram handle, email (syifaalya157@gmail.com) and WhatsApp number are already filled in. The "How it works" steps describe your process: unedited photos within 24 hours, edited photos 5–7 working days after the client's choice.


Then search for `[` and rewrite every bracketed placeholder by hand. These are your About text. **Don't publish until no `[` placeholders are left.**

**The Italian text:** I wrote it, and it hasn't been checked by a native speaker. Ask an Italian friend to read it once before you publish. I avoided gendered words that refer to you, such as *fotografo/fotografa*, so the text is correct either way. The Italian pages say you speak English and Indonesian, so Italian clients know what to expect.

## Step 2: Add your photos

**Already done:**
- **Homepage:** a collage of four photos at the top (flowers, ring close-up, portrait, chrysanthemum), plus 9 photos mixing all three shoots below. To swap a collage photo, change its file name in `index.html` and `it/index.html` (search for `collage`).
- **Brands page:** one gallery per project. *Flowers by Maison Kusuma* has 8 photos, *Jewellery* 3, and *Drinks* 2.
- **Descriptions:** every photo has a description and caption in both languages. Dates come from the camera.
- **Prices:** starting prices on both homepages: Padova from €60 and Venice from €100 (1 hour, 40 edited photos, preview within 48 hours, one free revision), with a button to send an enquiry. To change a price, search all files for `€60` / `60 €` or `€100` / `100 €`, and for `"minPrice"` (the copy stored for Google).

Still missing: **a portrait of you** for the About section (search for `placeholder-portrait`), and photos for the **graduation** and **couples** pages. Those two pages have no gallery until you add one; there's a ready-made spot marked in each file.

**About RAW files (.ARW):** websites can't show RAW files. Export a JPG from your editing app (Lightroom or similar) first, then run the script on the JPGs. The two flower close-ups on the brands page (`chrysanthemum-macro`, `asparagus-fern-macro`) were converted from your RAW files with a plain, neutral conversion, not your own edit. If you'd like them to match the warm look of your other photos, export your own edited JPGs with those file names and run the script again.

To add more photos later:

**Only use photos of clients if they agreed to it.** Photos of identifiable people are personal data under the GDPR. The usual practice is a short written consent (*liberatoria*) that covers using the photos on your website and social media. A professional can confirm the details for your situation.

1. Keep the homepage to your best 6–12 photos overall, and 3–6 per service page.
2. Put the originals in a folder **outside** this site folder and rename them descriptively, e.g. `laurea-prato-della-valle.jpg` or `pre-wedding-venezia-alba.jpg`. File names are a small signal Google reads.
3. Install Python (python.org), then run once: `pip install Pillow`
4. From inside this site folder, run:
   ```
   python tools/prepare_photos.py ~/Desktop/web-photos --site https://syifaalya157-ops.github.io > snippets.txt
   ```
5. `snippets.txt` contains:
   - `<figure>` blocks for **English** pages and a second set for **Italian** pages (the Italian ones start with `../images/`, because those pages are in the `it/` folder). Paste them into the `<div class="gallery" ...>` of each page.
   - sitemap lines. Add them inside the `<url>` of each page that shows the photo, in both languages.
6. Replace each `DESCRIBE THIS PHOTO` with a plain description (the **alt text**), in the page's language. For example, `alt="Graduate with a laurel wreath in Prato della Valle, Padova"` on an English page, and `alt="Laureata con la corona d'alloro in Prato della Valle, Padova"` on its Italian twin.
7. Delete `snippets.txt` when you're done. Once your About portrait is in, delete the `placeholder-portrait` files from `images/`.

The script also **removes hidden metadata, including GPS location**, so you don't publish where you live.

## Step 3: Publish on GitHub Pages (free)

1. Create a free account at github.com.
2. Create a **public** repository named exactly `syifaalya157-ops.github.io`.
3. Upload all files and folders (Add file → Upload files).
4. Go to **Settings → Pages** and set it to deploy from the `main` branch, `/ (root)`.
5. A few minutes later the site is live at `https://syifaalya157-ops.github.io`.

Things to know: the repository is public, so anyone can download its files. **Never upload full-resolution originals.** The limits are 1 GB per site and a soft limit of 100 GB of traffic per month, which is plenty for web-sized photos. If GitHub's menus look different from these steps, follow GitHub's "Creating a GitHub Pages site" guide.

## Step 4: Get found by clients in Padova and Venice

This matters more than anything technical on the site.

1. **Google Business Profile (free).** This is what puts you on Google Maps and in the local results for searches like "fotografo laurea Padova".
   - Register as a **service-area business**: you travel to clients and don't have a studio. Google's guidelines say a service-area business should hide its home address and list the areas it serves (Padova, Venezia).
   - Use your real name as the business name, the same as on the website. **Don't add keywords** like "Fotografo Padova" to the name; Google's rules forbid it and it can get the profile suspended.
   - Add your website, your services, and photos.
2. **Reviews.** After each session, send clients a link to leave a Google review. Google says the number of reviews and positive ratings counts towards how "prominent" a business is in local results. Never write reviews yourself or ask friends to post fake ones.
3. **Google Search Console (free):** add the site and submit `https://syifaalya157-ops.github.io/sitemap.xml`.
4. **Links:** put the site link in your Instagram bio, your Google profile, and anywhere you post your work. Links from other websites also count towards prominence.
5. **Text:** the service pages already have real text. Make it yours, and add specific places and details from sessions you've actually done.

## Before you start charging: please check

I'm not a lawyer or accountant, and these points need checking with a *commercialista* or CAF:

- **Tax status.** Whether you need a partita IVA, or whether occasional work (*prestazione occasionale*) is possible for you, depends on your situation. If you do have a partita IVA, Italian rules require it on your website's home page. There's a ready-made line for it in the footer of `index.html`: remove the comment marks and fill it in.
- **Your study permit's hour limit.** Italy's labour inspectorate (INL, note of 24 May 2022) says students with a study permit can work up to 20 hours a week and 1,040 a year, and unused hours from one week can't be moved to another. The official pages I could read don't say how this applies to self-employed work. Keep a simple log of your hours per session, including editing, so you can show you stayed within the limit when you renew your permit.
- **Shooting in Venice.** I couldn't find reliable information on whether professional photo shoots in Venice's public spaces need a permit. Check with the Comune di Venezia before booking paid sessions there.

## Optional: your own domain and email

A domain like `alyasyifa.com` (check availability) looks more professional than `syifaalya157-ops.github.io`, and it lets you have an email address like `hello@alyasyifa.com`.

1. **Buy the domain** from any registrar. Compare yearly renewal prices, not just the first-year price.
2. **Connect it to GitHub Pages.** In the repository, go to Settings → Pages → Custom domain and enter it. **Do this before changing DNS**, because GitHub warns that doing it the other way round can let someone take over your domain. Then at your registrar, add four A records pointing to `185.199.108.153`, `185.199.109.153`, `185.199.110.153` and `185.199.111.153`, plus a CNAME record for `www` pointing to `syifaalya157-ops.github.io`. Turn on "Enforce HTTPS" once it appears, which can take up to 24 hours. Never add wildcard (`*`) records.
3. **Update the site:** Find and Replace `https://syifaalya157-ops.github.io` with `https://yourdomain.com` in every file, then resubmit the sitemap in Search Console.
4. **Email:** your email provider gives you MX records to add at the registrar. These don't affect the website records above.

## Keeping it updated

- **New photo:** run the script and paste the blocks into the English page and its Italian twin. Add the sitemap line and update `<lastmod>`.
- **New service page:** copy an existing page in both languages and update the `canonical` and `hreflang` lines at the top of **both** files so they point to each other. Then add both to `sitemap.xml` and link them from the services list.
- **Colours:** change them at the top of `css/style.css`. Dark mode follows the visitor's phone or computer setting.

## Trade-offs

- **Two languages means double maintenance.** Google judges a page's language from its visible text, so a half-translated page works against you. If keeping both versions in sync becomes too much, it's better to drop Italian than to leave it out of date. Bear in mind that dropping it means fewer local clients from Padova and Venice finding you.
- **A visible email address attracts some spam.** WhatsApp is listed too, because many clients in Italy prefer it.
- **Google Fonts:** the typeface loads from Google. To avoid that, delete the three `fonts.googleapis`/`fonts.gstatic` lines in each page, and the site will use the device's own font.
