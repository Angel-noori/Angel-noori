#!/usr/bin/env python3
import os, json, html, urllib.request
from pathlib import Path
from datetime import datetime, timezone
USER='Angel-noori'
ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/'assets'
TOKEN=os.environ.get('GITHUB_TOKEN','')
HEADERS={'Accept':'application/vnd.github+json','User-Agent':'Angel-noori-profile-metrics','X-GitHub-Api-Version':'2022-11-28'}
if TOKEN: HEADERS['Authorization']=f'Bearer {TOKEN}'
def api(path):
    req=urllib.request.Request('https://api.github.com'+path,headers=HEADERS)
    with urllib.request.urlopen(req,timeout=30) as r: return json.load(r)
def esc(x): return html.escape(str(x),quote=True)
def rank(value,cuts):
    if value>=cuts[3]: return 'DIAMOND'
    if value>=cuts[2]: return 'PLATINUM'
    if value>=cuts[1]: return 'GOLD'
    if value>=cuts[0]: return 'SILVER'
    return 'BRONZE'
def main():
    user=api(f'/users/{USER}')
    repos=[]
    for page in range(1,5):
        batch=api(f'/users/{USER}/repos?per_page=100&page={page}&sort=updated&type=owner')
        if not batch: break
        repos+=batch
        if len(batch)<100: break
    total_stars=sum(int(r.get('stargazers_count',0)) for r in repos)
    total_forks=sum(int(r.get('forks_count',0)) for r in repos)
    lang_counts={}
    for r in repos:
        lang=r.get('language')
        if lang: lang_counts[lang]=lang_counts.get(lang,0)+1
    lang_names=[x[0] for x in sorted(lang_counts.items(), key=lambda x:(-x[1],x[0]))]
    created=datetime.fromisoformat(user['created_at'].replace('Z','+00:00'))
    years=max(0,(datetime.now(timezone.utc)-created).days//365)
    updated=datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    stats=[('PUBLIC REPOS',user.get('public_repos',0),'#00ff9c'),('FOLLOWERS',user.get('followers',0),'#00d9ff'),('TOTAL STARS',total_stars,'#a25cff'),('TOTAL FORKS',total_forks,'#ff2d95'),('LANGUAGES',len(lang_names),'#ffd54a'),('ACCOUNT AGE',f'{years}y','#ff8a35')]
    cards=[]
    for i,(label,val,color) in enumerate(stats):
        x=45+(i%3)*345; y=120+(i//3)*92
        cards.append(f'<rect x="{x}" y="{y}" width="320" height="70" rx="18" fill="#0c1821" stroke="{color}" stroke-width="2"/><text x="{x+22}" y="{y+28}" fill="{color}" font-family="Arial" font-size="15" font-weight="700">{esc(label)}</text><text x="{x+22}" y="{y+57}" fill="#f0f7fb" font-family="Arial" font-size="27" font-weight="800">{esc(val)}</text>')
    lang_line=' • '.join(lang_names[:7]) if lang_names else 'No primary languages detected yet'
    metrics=f'''<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="355" viewBox="0 0 1100 355"><defs><linearGradient id="g" x1="0" x2="1"><stop stop-color="#00ff9c"/><stop offset=".35" stop-color="#00d9ff"/><stop offset=".7" stop-color="#a25cff"/><stop offset="1" stop-color="#ff2d95"/></linearGradient></defs><rect width="1100" height="355" rx="28" fill="#061019" stroke="url(#g)" stroke-width="3"/><text x="45" y="55" fill="url(#g)" font-family="Arial" font-size="32" font-weight="800">ANGEL-NOORI • GITHUB COMMAND CENTER</text><text x="45" y="88" fill="#9eb6c6" font-family="Arial" font-size="15">Generated inside this repository from GitHub API • Updated {esc(updated)}</text>{''.join(cards)}<text x="45" y="325" fill="#00ff9c" font-family="Arial" font-size="15" font-weight="700">TOP REPOSITORY LANGUAGES</text><text x="285" y="325" fill="#c9d6df" font-family="Arial" font-size="15">{esc(lang_line)}</text></svg>'''
    (ASSETS/'github-metrics.svg').write_text(metrics,encoding='utf-8')
    trophies=[('REPO BUILDER',user.get('public_repos',0),rank(user.get('public_repos',0),[3,8,20,50]),'#ffd54a'),('STAR COLLECTOR',total_stars,rank(total_stars,[1,5,20,100]),'#00ff9c'),('CODE EXPLORER',len(lang_names),rank(len(lang_names),[2,4,7,12]),'#00d9ff'),('COMMUNITY',user.get('followers',0),rank(user.get('followers',0),[3,10,30,100]),'#a25cff'),('FORKED IDEAS',total_forks,rank(total_forks,[1,3,10,40]),'#ff2d95'),('GITHUB AGE',years,rank(years,[1,2,4,7]),'#ff8a35')]
    tc=[]
    for i,(label,val,rk,color) in enumerate(trophies):
        x=32+i*176
        tc.append(f'<rect x="{x}" y="126" width="160" height="130" rx="20" fill="#0c1821" stroke="{color}" stroke-width="2"/><circle cx="{x+80}" cy="162" r="20" fill="#081219" stroke="{color}" stroke-width="3"/><text x="{x+80}" y="169" text-anchor="middle" fill="{color}" font-family="Arial" font-size="22" font-weight="800">★</text><text x="{x+80}" y="202" text-anchor="middle" fill="#f2f7fa" font-family="Arial" font-size="13" font-weight="800">{esc(label)}</text><text x="{x+80}" y="226" text-anchor="middle" fill="{color}" font-family="Arial" font-size="15" font-weight="800">{esc(rk)}</text><text x="{x+80}" y="247" text-anchor="middle" fill="#9fb4c1" font-family="Arial" font-size="12">VALUE: {esc(val)}</text>')
    tsvg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="300" viewBox="0 0 1100 300"><defs><linearGradient id="g" x1="0" x2="1"><stop stop-color="#ffd54a"/><stop offset=".25" stop-color="#00ff9c"/><stop offset=".5" stop-color="#00d9ff"/><stop offset=".75" stop-color="#a25cff"/><stop offset="1" stop-color="#ff2d95"/></linearGradient></defs><rect width="1100" height="300" rx="28" fill="#061019" stroke="url(#g)" stroke-width="3"/><text x="42" y="54" fill="url(#g)" font-family="Arial" font-size="32" font-weight="800">ANGEL-NOORI • GITHUB TROPHY MATRIX</text><text x="42" y="86" fill="#9eb6c6" font-family="Arial" font-size="15">Dynamic custom ranks generated from current public GitHub profile data</text>{''.join(tc)}<text x="42" y="282" fill="#718b9b" font-family="Arial" font-size="12">Local asset • no github-readme-stats.vercel.app or github-profile-trophy.vercel.app dependency</text></svg>'''
    (ASSETS/'github-trophies.svg').write_text(tsvg,encoding='utf-8')
if __name__=='__main__': main()
