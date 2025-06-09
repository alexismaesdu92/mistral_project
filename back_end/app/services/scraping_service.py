"""
Récupération intégrale de https://docs.mistral.ai/ -> markdown structurés

"""

import argparse, asyncio, hashlib, csv, re, sys, os, urllib.parse as ulib
from datetime import datetime
from pathlib import Path
# Importer python-slugify correctement
from slugify import slugify as python_slugify

import httpx
from bs4 import BeautifulSoup
from markdownify import markdownify as md
from tqdm import tqdm
import tldextract

BASE_URL = "https://docs.mistral.ai/"

HEADERS = {
    "User-Agent": "mistral-doc-scraper/0.1 (+https://github.com/you)",
    "Accept": "text/html,application/xhtml+xml"
}


def norm_url(url: str) -> str:
    """Nettoie l’URL (supprime le fragment et normalise les '../')."""
    u = ulib.urlsplit(url)
    clean = ulib.urlunsplit((u.scheme, u.netloc, ulib.urljoin(u.path, "."), u.query, ""))
    return clean.rstrip("/")

def is_in_scope(url: str) -> bool:
    """Filtre : domaine docs.mistral.ai uniquement."""
    u = ulib.urlsplit(url)
    return u.scheme in {"http", "https"} and u.netloc.endswith("docs.mistral.ai")

def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def html_to_markdown(html: str) -> str:
    md_text = md(
        html,
        heading_style="ATX",
        bullets="*",
        strip=["script", "style", "header", "footer", "nav", "aside"],
        escape_asterisks=False,
    )
    # Nettoyages mineurs
    md_text = re.sub(r"\n{3,}", "\n\n", md_text).strip() + "\n"
    return md_text

def custom_slugify(text, separator="/", lowercase=False):
    result = python_slugify(text)
    if separator != "-":
        result = result.replace("-", separator)
    if not lowercase:
        parts = result.split(separator)
        original_parts = text.split("/")
        for i, part in enumerate(parts):
            if i < len(original_parts) and original_parts[i].lower() == part:
                parts[i] = original_parts[i]
        result = separator.join(parts)
    return result

def build_path(url: str, outdir: Path) -> Path:
    """Ex. https://docs.mistral.ai/sdk/python → out/sdk/python/index.md"""
    u = ulib.urlsplit(url)
    path = u.path.lstrip("/") or "index"
    if path.endswith("/"):
        path += "index"
    fname = custom_slugify(path, separator="/", lowercase=False) + ".md"
    return outdir / u.netloc / fname

# -------------------- scrapper --------------------

class DocScraper:
    def __init__(self, out: Path, concurrency: int = 10):
        self.out = out
        self.client = httpx.AsyncClient(headers=HEADERS, http2=False, follow_redirects=True, timeout=15)
        self.seen = set()
        self.sem = asyncio.Semaphore(concurrency)
        self.manifest_rows = []

    async def close(self):
        await self.client.aclose()

    async def fetch(self, url: str) -> str | None:
        async with self.sem:
            try:
                r = await self.client.get(url)
                if r.status_code == 200 and "text/html" in r.headers.get("content-type", ""):
                    return r.text
            except httpx.RequestError as e:
                tqdm.write(f"[WARN] {url} → {e}")
        return None

    async def parse(self, url: str):
        if url in self.seen:
            return
        self.seen.add(url)

        html = await self.fetch(url)
        if html is None:
            return

        try:
            # Essayer d'abord avec lxml, puis avec html.parser si lxml n'est pas disponible
            soup = BeautifulSoup(html, "lxml")
        except Exception:
            soup = BeautifulSoup(html, "html.parser")

        main = soup.find("main") or soup  # fallback : entier
        md_text = html_to_markdown(str(main))
        file_path = build_path(url, self.out)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(md_text, encoding="utf-8")

        self.manifest_rows.append({
            "url": url,
            "file": str(file_path.relative_to(self.out)),
            "sha256": sha256(md_text),
            "fetched_at": datetime.utcnow().isoformat()
        })

        # -------- 2) détecter les liens internes --------
        for a in soup.find_all("a", href=True):
            href = ulib.urljoin(url, a["href"])
            href = norm_url(href)
            if is_in_scope(href):
                asyncio.create_task(self.parse(href))

    async def run(self, start_url: str):
        await self.parse(start_url)
        await asyncio.gather(*asyncio.all_tasks(asyncio.get_event_loop()) - {asyncio.current_task()})

    def save_manifest(self):
        csv_path = self.out / "manifest.csv"
        with csv_path.open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=["url", "file", "sha256", "fetched_at"])
            w.writeheader()
            for row in self.manifest_rows:
                w.writerow(row)

# -------------------- exécution CLI --------------------

def main():
    out_dir = Path("data/scraping_test")
    
    out_dir.mkdir(parents=True, exist_ok=True)
    
    scraper = DocScraper(out=out_dir)

    try:
        asyncio.run(scraper.run(BASE_URL))
    except Exception as e:
        print(f"Erreur pendant le scraping: {e}")
    finally:
        try:
            scraper.save_manifest()
            asyncio.run(scraper.close())
        except Exception as e:
            print(f"Erreur pendant la finalisation: {e}")

    print(f"\n✅ Scraping terminé. Fichiers dans : {out_dir}")

if __name__ == "__main__":
    main()
