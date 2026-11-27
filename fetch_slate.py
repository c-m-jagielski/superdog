#!/usr/bin/env python3
"""Build slate.json for the Superdog app from CollegeFootballData.com (CFBD).

Setup:   export CFBD_API_KEY='your-key'      (free key: https://collegefootballdata.com/key)
Usage:   python fetch_slate.py --week 12
         python fetch_slate.py --week 12,13 --provider Caesars --out slate.json
Then in the app: Commissioner tab > Import slate > choose slate.json.
Re-run after games finish and re-import to fill in final scores. Spreads of games
already in the app are never changed by a re-import (lines are frozen at first load).
Uses ~2 API calls per week requested; stdlib only.
"""
import argparse, collections, datetime as dt, json, os, re, sys
import urllib.error, urllib.parse, urllib.request

BASE = 'https://api.collegefootballdata.com'
FMT = re.compile(r'^(?P<team>.+?)\s+(?P<sp>[+-]?\d+(?:\.\d+)?)$')   # "Alabama -26.5"


def get(path, key, **params):
    url = f"{BASE}{path}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={
        'Authorization': f'Bearer {key}', 'Accept': 'application/json',
        'User-Agent': 'superdog-slate/1.0'})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        hint = {401: 'API key rejected; check CFBD_API_KEY.',
                429: 'Monthly call quota exceeded.'}.get(e.code, '')
        sys.exit(f'HTTP {e.code} from {path}. {hint}')
    except urllib.error.URLError as e:
        sys.exit(f'Network error: {e.reason}')


def first(*vals):
    return next((v for v in vals if v is not None), None)


def parse_line(game, provider):
    """-> ((fav, dog, spread), None) or (None, reason). Uses formattedSpread so the
    favorite comes from the text, not from a sign convention."""
    line = next((l for l in game.get('lines') or []
                 if (l.get('provider') or '').lower() == provider.lower()
                 and l.get('formattedSpread')), None)
    if not line:
        return None, 'no line from provider'
    m = FMT.match(str(line['formattedSpread']).strip())
    if not m:
        return None, 'unparsable spread'
    mag = abs(float(m['sp']))
    if mag == 0:
        return None, "pick'em"
    team, home, away = m['team'].strip().lower(), game['homeTeam'], game['awayTeam']
    if team == home.lower():
        return (home, away, mag), None
    if team == away.lower():
        return (away, home, mag), None
    return None, 'favorite name mismatch'


def build_week(lines, games, week, provider):
    by_id = {g.get('id'): g for g in games}
    out, skipped, provs = [], collections.defaultdict(list), collections.Counter()
    for g in lines:
        for l in g.get('lines') or []:
            provs[l.get('provider')] += 1
        parsed, why = parse_line(g, provider)
        label = f"{g.get('awayTeam')} @ {g.get('homeTeam')}"
        if not parsed:
            skipped[why].append(label)
            continue
        fav, dog, spread = parsed
        gm = by_id.get(g['id'], {})
        hp = first(gm.get('homePoints'), g.get('homeScore'))
        ap = first(gm.get('awayPoints'), g.get('awayScore'))
        final = gm.get('completed') is True and hp is not None and ap is not None
        fav_home = fav == g['homeTeam']
        rec = {'id': g['id'], 'week': week, 'fav': fav, 'dog': dog, 'spread': spread,
               'kick': '' if gm.get('startTimeTBD') else (gm.get('startDate') or g.get('startDate') or ''),
               'final': final}
        if final:
            rec['favScore'], rec['dogScore'] = (hp, ap) if fav_home else (ap, hp)
        out.append(rec)
    return out, skipped, provs


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--week', required=True, help='CFBD week number, or comma list: 12 or 12,13')
    ap.add_argument('--year', type=int, default=dt.date.today().year if dt.date.today().month >= 8 else dt.date.today().year - 1)
    ap.add_argument('--provider', default='consensus', help='line provider (default: consensus)')
    ap.add_argument('--season-type', default='regular', choices=['regular', 'postseason'])
    ap.add_argument('--out', default='slate.json')
    a = ap.parse_args(argv)
    key = os.environ.get('CFBD_API_KEY')
    if not key:
        sys.exit('Set CFBD_API_KEY first (free key: https://collegefootballdata.com/key).')
    weeks = [int(w) for w in a.week.split(',')]
    allg = []
    for w in weeks:
        q = dict(year=a.year, week=w, seasonType=a.season_type)
        lines, games = get('/lines', key, **q), get('/games', key, **q)
        recs, skipped, provs = build_week(lines, games, w, a.provider)
        allg += recs
        print(f'Week {w}: {len(lines)} games in feed -> {len(recs)} included '
              f'({sum(r["final"] for r in recs)} final)', file=sys.stderr)
        print(f'  providers seen (line records): {dict(provs)}', file=sys.stderr)
        for why, names in skipped.items():
            print(f'  skipped {len(names)} ({why}): {", ".join(names[:4])}{" ..." if len(names) > 4 else ""}', file=sys.stderr)
    if not allg:
        sys.exit('No usable games. Try another --provider (see providers seen above) or check --week/--year.')
    json.dump({'source': 'cfbd', 'provider': a.provider, 'year': a.year,
               'generated': dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds'),
               'games': allg}, open(a.out, 'w'), indent=1)
    print(f'Wrote {len(allg)} games to {a.out}', file=sys.stderr)


if __name__ == '__main__':
    main()
