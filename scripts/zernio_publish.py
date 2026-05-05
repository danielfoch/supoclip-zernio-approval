#!/usr/bin/env python3
import argparse, json, subprocess, sys
from pathlib import Path


def run(cmd):
    p=subprocess.run(cmd,text=True,capture_output=True)
    if p.returncode:
        print(p.stdout); print(p.stderr,file=sys.stderr); raise SystemExit(p.returncode)
    return p.stdout


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--video',required=True)
    ap.add_argument('--caption-file',required=True)
    ap.add_argument('--accounts',required=True)
    ap.add_argument('--title',default='')
    ap.add_argument('--hashtags',default='TorontoRealEstate,CanadianRealEstate,HousingMarket,RealEstate,Economics')
    args=ap.parse_args()
    media=json.loads(run(['zernio','media:upload',args.video,'--pretty']))
    url=media.get('url')
    if not url: raise SystemExit('No media URL returned by zernio')
    text=Path(args.caption_file).read_text()
    out=run(['zernio','posts:create','--text',text,'--title',args.title,'--accounts',args.accounts,'--media',url,'--hashtags',args.hashtags,'--pretty'])
    print(out)

if __name__=='__main__': main()
