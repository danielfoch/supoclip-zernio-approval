#!/usr/bin/env python3
import argparse, html, re, subprocess
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont


def parse_sec(s):
    if ':' not in s:
        return float(s)
    parts=[float(x) for x in s.split(':')]
    out=0
    for p in parts: out=out*60+p
    return out


def parse_vtt(path):
    if not path or not Path(path).exists(): return []
    items=[]
    text=Path(path).read_text(errors='ignore')
    for block in text.split('\n\n'):
        lines=block.splitlines()
        if not lines or '-->' not in lines[0]: continue
        st,en=lines[0].split('-->')[0].strip(), lines[0].split('-->')[1].split()[0].strip()
        body=' '.join(lines[1:])
        body=re.sub(r'<\d\d:\d\d:\d\d\.\d{3}>',' ',body)
        body=re.sub(r'</?c[^>]*>',' ',body)
        body=re.sub(r'<[^>]+>',' ',body)
        body=html.unescape(' '.join(body.split()))
        if body: items.append((parse_sec(st),parse_sec(en),body))
    return items


def caption_groups(items,start,duration):
    end=start+duration; groups=[]; buf=[]; gs=None; ge=None; wc=0
    for st,en,txt in items:
        if en<start or st>end: continue
        rst=max(0,st-start); ren=min(duration,en-start)
        if gs is None: gs=rst
        buf.append(txt); ge=ren; wc+=len(txt.split())
        if ge-gs>=2.3 or wc>=8:
            groups.append((gs,max(ge,gs+0.7),' '.join(' '.join(buf).split())))
            buf=[]; gs=None; ge=None; wc=0
    if buf and gs is not None: groups.append((gs,max(ge,gs+0.8),' '.join(' '.join(buf).split())))
    return groups


def get_font(size):
    for p in ['/System/Library/Fonts/Supplemental/Arial Bold.ttf','/Library/Fonts/Arial Bold.ttf','/System/Library/Fonts/Supplemental/Arial.ttf']:
        if Path(p).exists(): return ImageFont.truetype(p,size)
    return ImageFont.load_default()


def wrap(draw,text,font,maxw):
    words=text.split(); lines=[]; cur=''
    for w in words:
        test=(cur+' '+w).strip()
        if draw.textbbox((0,0),test,font=font)[2]>maxw and cur:
            lines.append(cur); cur=w
        else: cur=test
    if cur: lines.append(cur)
    return lines[:3]


def draw_box(img,text,font,y,maxw,W,box=(0,0,0,185),stroke=3):
    draw=ImageDraw.Draw(img,'RGBA')
    lines=wrap(draw,text,font,maxw)
    lineh=int(font.size*1.12); total=lineh*len(lines)+24
    draw.rounded_rectangle((38,y-12,W-38,y+total-12), radius=22, fill=box)
    yy=y
    for line in lines:
        bbox=draw.textbbox((0,0),line,font=font,stroke_width=stroke)
        x=(W-(bbox[2]-bbox[0]))//2
        draw.text((x,yy),line,font=font,fill=(255,255,255),stroke_width=stroke,stroke_fill=(0,0,0))
        yy+=lineh


def crop_scale(frame,crop,size):
    x,y,w,h=[int(v) for v in crop]
    return cv2.resize(frame[y:y+h,x:x+w],size,interpolation=cv2.INTER_AREA)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--input',required=True)
    ap.add_argument('--captions')
    ap.add_argument('--output',required=True)
    ap.add_argument('--hook',required=True)
    ap.add_argument('--start',type=float,default=0)
    ap.add_argument('--duration',type=float,default=165)
    ap.add_argument('--split-at',type=float,default=8.0)
    ap.add_argument('--width',type=int,default=720)
    ap.add_argument('--height',type=int,default=1280)
    args=ap.parse_args()

    W,H=args.width,args.height
    out=Path(args.output); out.parent.mkdir(parents=True,exist_ok=True)
    silent=out.with_suffix('.silent.mp4'); audio=out.with_suffix('.audio.m4a')

    cap=cv2.VideoCapture(args.input)
    fps=cap.get(cv2.CAP_PROP_FPS) or 30
    sw=int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)); sh=int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    full_w=round(sh*9/16); full_h=sh
    half_w=sw//2
    half_h=round(half_w*8/9)
    half_y=max(0,(sh-half_h)//2)
    face_half=(0,half_y,half_w,half_h)
    screen_half=(half_w,half_y,half_w,half_h)
    face_detector=cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')
    last_x=None

    events=caption_groups(parse_vtt(args.captions),args.start,args.duration)
    hook_font=get_font(52); cap_font=get_font(44)
    def active(t):
        for s,e,txt in events:
            if s<=t<=e: return txt
        return ''
    def face_crop(frame):
        nonlocal last_x
        gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        faces=face_detector.detectMultiScale(gray,1.05,4,minSize=(80,80))
        if len(faces):
            x,y,w,h=max(faces,key=lambda r:r[2]*r[3])
            x0=max(0,min(sw-full_w,int(x+w/2-full_w/2)))
            if last_x is not None: x0=int(last_x*0.72+x0*0.28)
            last_x=x0
        elif last_x is not None:
            x0=last_x
        else:
            x0=max(0,min(sw-full_w,0))
        return (x0,0,full_w,full_h)

    writer=cv2.VideoWriter(str(silent),cv2.VideoWriter_fourcc(*'mp4v'),fps,(W,H))
    cap.set(cv2.CAP_PROP_POS_MSEC,args.start*1000)
    total=int(args.duration*fps)
    for i in range(total):
        ok,frame=cap.read()
        if not ok: break
        t=i/fps
        if t<args.split_at:
            rendered=crop_scale(frame,face_crop(frame),(W,H))
        else:
            top=crop_scale(frame,face_half,(W,H//2))
            bottom=crop_scale(frame,screen_half,(W,H//2))
            rendered=np.vstack([top,bottom])
        pil=Image.fromarray(cv2.cvtColor(rendered,cv2.COLOR_BGR2RGB)).convert('RGBA')
        if t<6: draw_box(pil,args.hook.upper(),hook_font,70,W-100,W,box=(0,0,0,190))
        txt=active(t)
        if txt: draw_box(pil,txt,cap_font,H-290,W-90,W,box=(0,0,0,185))
        writer.write(cv2.cvtColor(np.array(pil.convert('RGB')),cv2.COLOR_RGB2BGR))
    writer.release(); cap.release()

    subprocess.run(['ffmpeg','-y','-ss',str(args.start),'-t',str(args.duration),'-i',args.input,'-vn','-c:a','aac','-b:a','128k',str(audio)],check=True)
    subprocess.run(['ffmpeg','-y','-i',str(silent),'-i',str(audio),'-c:v','libx264','-preset','veryfast','-crf','22','-c:a','copy','-movflags','+faststart',str(out)],check=True)
    silent.unlink(missing_ok=True); audio.unlink(missing_ok=True)
    print(out)

if __name__=='__main__': main()
