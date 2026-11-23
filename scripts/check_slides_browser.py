"""Browser checks for docs/index.html (needs: pip install playwright; playwright install chromium).

Usage: python3 scripts/check_slides_browser.py [--chrome PATH] [--shots DIR]
"""
import sys, re, pathlib, argparse, tempfile
from playwright.sync_api import sync_playwright
ap=argparse.ArgumentParser(); ap.add_argument('--chrome'); ap.add_argument('--shots', default=tempfile.mkdtemp()); a=ap.parse_args()
U=(pathlib.Path(__file__).resolve().parents[1]/'docs'/'index.html').as_uri()
out=a.shots
res=[]
def chk(name,cond): res.append((name,bool(cond))); print(('PASS' if cond else 'FAIL'),name)
with sync_playwright() as p:
    b=p.chromium.launch(**({'executable_path':a.chrome} if a.chrome else {}))
    # desktop
    pg=b.new_page(viewport={'width':1366,'height':800})
    errs=[]; pg.on('pageerror',lambda e:errs.append(str(e))); pg.on('console',lambda m: m.type=='error' and errs.append(m.text))
    pg.goto(U)
    active=lambda: pg.evaluate("[...document.querySelectorAll('.slide')].findIndex(s=>s.classList.contains('active'))")
    chk('14 slides', pg.locator('.slide').count()==14)
    chk('starts at 1', active()==0)
    pg.keyboard.press('ArrowRight'); chk('ArrowRight -> 2', active()==1)
    pg.keyboard.press('ArrowLeft'); chk('ArrowLeft -> 1', active()==0)
    pg.keyboard.press('End'); chk('End -> 14', active()==13)
    pg.keyboard.press('Home'); chk('Home -> 1', active()==0)
    pg.click('#next'); chk('next button', active()==1)
    pg.click('#prev'); chk('prev button', active()==0)
    chk('prev disabled at 1', pg.is_disabled('#prev'))
    pg.goto(U+'#5'); pg.reload(); chk('hash #5 deep link', active()==4)
    # stepper
    vis=lambda sel: pg.evaluate(f"[...document.querySelectorAll('{sel}')].filter(e=>getComputedStyle(e).display!='none').length")
    chk('stepper shows 1 panel initially', vis('#s5 .step')==1)
    pg.click('#s5 [data-step="3"]'); chk('stepper step 4 shows all 4', vis('#s5 .step')==4)
    pg.screenshot(path=f'{out}/d5.png')
    pg.keyboard.press('ArrowRight'); pg.keyboard.press('ArrowRight'); pg.keyboard.press('ArrowRight')
    chk('reached slide 8', active()==7)
    pg.click('#s8 [data-sc="2"]'); chk('scenario 3 highlighted', pg.evaluate("document.querySelector('#s8 [data-row=\"2\"]').classList.contains('on') && !document.querySelector('#s8 [data-row=\"0\"]').classList.contains('on')"))
    pg.screenshot(path=f'{out}/d8.png')
    pg.goto(U+'#13'); pg.reload()
    pg.click('#s13 .qitem:nth-of-type(1) [data-opt="b"]'); chk('quiz wrong feedback', '再想想' in pg.inner_text('#s13 .qitem:nth-of-type(1) .feedback'))
    pg.click('#s13 .qitem:nth-of-type(1) [data-opt="a"]'); chk('quiz correct feedback + explain open', '答對' in pg.inner_text('#s13 .qitem:nth-of-type(1) .feedback') and pg.evaluate("document.querySelector('#s13 .qitem .explain').open"))
    pg.screenshot(path=f'{out}/d13.png')
    # sources expansion
    pg.goto(U+'#4'); pg.reload()
    pg.click('#s4 .sources summary'); chk('sources expand', pg.evaluate("document.querySelector('#s4 .sources').open"))
    pg.screenshot(path=f'{out}/d4.png')
    # space on button does not change slide
    pg.goto(U+'#5'); pg.reload(); pg.focus('#s5 [data-step="1"]'); pg.keyboard.press('Space'); chk('Space on button stays on slide', active()==4)
    # overflow check per slide on desktop
    over=[]
    for i in range(14):
        pg.goto(U+f'#{i+1}'); pg.reload()
        o=pg.evaluate("(()=>{const s=document.querySelector('.slide.active');return s.scrollHeight-s.clientHeight})()")
        if o>0: over.append((i+1,o))
        pg.wait_for_timeout(400); pg.screenshot(path=f'{out}/desk{i+1:02d}.png')
    print('desktop overflow (px):',over)
    chk('no JS errors', not errs); print(errs)
    # mobile with touch
    ctx=b.new_context(viewport={'width':390,'height':844},has_touch=True,is_mobile=True,device_scale_factor=2)
    m=ctx.new_page(); m.goto(U)
    act=lambda: m.evaluate("[...document.querySelectorAll('.slide')].findIndex(s=>s.classList.contains('active'))")
    def swipe(dx):
        m.evaluate(f"""(()=>{{const t=(x)=>new Touch({{identifier:1,target:document.body,clientX:x,clientY:400}});
        document.dispatchEvent(new TouchEvent('touchstart',{{touches:[t(300)],changedTouches:[t(300)]}}));
        document.dispatchEvent(new TouchEvent('touchend',{{touches:[],changedTouches:[t(300+{dx})]}}));}})()""")
    swipe(-150); chk('swipe left -> 2', act()==1)
    swipe(150); chk('swipe right -> 1', act()==0)
    hov=[]
    for i in range(14):
        m.goto(U+f'#{i+1}'); m.reload()
        w=m.evaluate("document.querySelector('.slide.active').scrollWidth - document.querySelector('.slide.active').clientWidth")
        if w>0: hov.append((i+1,w))
        m.wait_for_timeout(400); m.screenshot(path=f'{out}/mob{i+1:02d}.png')
    chk('mobile no horizontal overflow', not hov); print(hov)
    # no-JS
    nj=b.new_context(java_script_enabled=False,viewport={'width':1366,'height':800}); n=nj.new_page(); n.goto(U)
    chk('no-JS: html.no-js', n.evaluate is not None and 'no-js' in (n.get_attribute('html','class') or ''))
    txt=n.inner_text('body')
    chk('no-JS: all slides visible text', all(s in txt for s in ['讓 LLM 先查資料再回答','4 Generate：有來源的答案','無中生有','看答案','Sources（五篇論文與 Wiki）']) )
    chk('no-JS: all 4 steps displayed', n.evaluate("[...document.querySelectorAll('#s5 .step')].every(e=>getComputedStyle(e).display!='none')"))
    chk('no-JS: quiz option buttons hidden', n.evaluate("getComputedStyle(document.querySelector('.opts')).display=='none'"))
    n.screenshot(path=f'{out}/nojs.png',full_page=True)
    # reduced motion
    rm=b.new_context(reduced_motion='reduce',viewport={'width':1366,'height':800}); r=rm.new_page(); r.goto(U)
    chk('reduced motion: no transition', r.evaluate("getComputedStyle(document.querySelector('.slide')).transitionDuration")in('0s','0s, 0s, 0s, 0s'))
    b.close()
print('SUMMARY', sum(c for _,c in res), '/', len(res), '| screenshots:', out)
sys.exit(0 if all(c for _,c in res) else 1)
