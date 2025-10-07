const el = (id) => document.getElementById(id);

let CURRENT_ID = '';

function showBusy(flag){
  const sp = document.getElementById('spinner');
  if(!sp) return;
  sp.classList.toggle('hidden', !flag);
}

async function api(path, opts) {
  showBusy(true);
  try{
    const res = await fetch(path, opts);
    if (!res.ok) {
      // ทำสำเนา response เพื่อป้องกันการอ่าน body ซ้ำ
      const ct = res.headers.get('content-type') || '';
      let t;
      if (ct.includes('application/json')) {
        t = await res.json();
        throw new Error(t.detail || JSON.stringify(t));
      } else {
        t = await res.text();
        throw new Error(t);
      }
    }
    const ct = res.headers.get('content-type') || '';
    if (ct.includes('application/json')) return res.json();
    return res.text();
  } finally {
    showBusy(false);
  }
}

function posterOrNA(url) {
  if (!url || url === 'N/A') return 'https://via.placeholder.com/400x600?text=No+Poster';
  return url;
}

function toast(msg, type='ok'){
  const wrap = document.getElementById('toastWrap');
  if(!wrap) return alert(msg);
  const t = document.createElement('div');
  t.className = 'toast ' + (type==='err'?'err':'ok');
  t.textContent = msg;
  wrap.appendChild(t);
  setTimeout(()=>{ t.remove(); }, 3600);
}

/* Grid results */
function renderSearchGrid(data) {
  const grid = el('searchGrid');
  grid.innerHTML = '';
  if (!data || !data.Search || !data.Search.length) {
    grid.innerHTML = `<div class="movie-tile" style="padding:16px">ไม่พบผลลัพธ์</div>`;
    return;
  }
  data.Search.forEach(item => {
    const card = document.createElement('div');
    card.className = 'movie-tile';
    card.innerHTML = `
      <img src="${posterOrNA(item.Poster)}" alt="Poster" loading="lazy" />
      <div class="tile-body">
        <h3 class="title">${item.Title || ''}</h3>
        <div class="meta">${item.Year || ''} • ${item.Type || 'movie'}</div>
        <div class="tile-actions">
          <button data-imdb="${item.imdbID}" data-act="select">Select</button>
          <button data-imdb="${item.imdbID}" data-act="details" class="btn-details">Details</button>
        </div>
      </div>
    `;
    card.addEventListener('click', (e) => {
      const btn = e.target.closest('button');
      if (!btn) return;
      const id = btn.getAttribute('data-imdb');
      if (!id) return;
      el('imdbId').value = id;
      
      const action = btn.getAttribute('data-act');
      if (action === 'details') {
        // เพิ่มเอฟเฟกต์พิเศษสำหรับปุ่ม Details
        btn.classList.add('btn-clicked');
        setTimeout(() => {
          btn.classList.remove('btn-clicked');
          onFetch();
        }, 300);
      } else if (action === 'select') {
        // เพิ่มเอฟเฟกต์เหมือนกับปุ่ม Details
        btn.classList.add('btn-clicked');
        setTimeout(() => {
          btn.classList.remove('btn-clicked');
          toast(`เลือกหนัง ID: ${id} แล้ว`, 'ok');
        }, 300);
      }
    });
    grid.appendChild(card);
  });
}

/* Selected movie card */
function renderMovieCard(meta) {
  const card = el('movieCard');
  if (!meta || meta.Response === 'False') {
    card.innerHTML = `<div class="plot">ไม่พบข้อมูลภาพยนตร์จาก OMDb</div>`;
    return;
  }
  const poster = posterOrNA(meta.Poster);
  const title = meta.Title || 'Unknown';
  const year = meta.Year || '';
  const rated = meta.Rated || '';
  const runtime = meta.Runtime || '';
  const genre = meta.Genre || '';
  const director = meta.Director || '';
  const actors = meta.Actors || '';
  const plot = meta.Plot || '';

  card.innerHTML = `
    <img class="poster" src="${poster}" alt="${title} poster" />
    <div class="info">
      <h3>${title} <span class="tag">${year}</span></h3>
      <div class="tags">
        ${rated ? `<span class="tag">${rated}</span>` : ''}
        ${runtime ? `<span class="tag">${runtime}</span>` : ''}
        ${genre ? genre.split(',').slice(0,4).map(g => `<span class="tag">${g.trim()}</span>`).join('') : ''}
      </div>
      <div class="plot">${plot}</div>
      <div class="tags">
        ${director ? `<span class="tag">Director: ${director}</span>` : ''}
        ${actors ? `<span class="tag">Actors: ${actors.split(',').slice(0,3).join(', ').trim()}</span>` : ''}
      </div>
    </div>
  `;
}

/* Charts */
function donutSVG({pos, neg, neu}) {
  const total = Math.max(1, pos + neg + neu);
  const parts = [
    {label:'Positive', value:pos, color:'var(--pos)'},
    {label:'Negative', value:neg, color:'var(--neg)'},
    {label:'Neutral',  value:neu, color:'var(--neu)'}
  ];
  const r = 60, R=80, cx=100, cy=100;
  let start = 0;
  let svg = `<svg viewBox="0 0 200 200" width="100%" height="100%" aria-label="Sentiment Donut">`;
  for (const p of parts) {
    const angle = (p.value/total) * Math.PI*2;
    const end = start + angle;
    const large = angle > Math.PI ? 1 : 0;
    const x1 = cx + R*Math.cos(start), y1 = cy + R*Math.sin(start);
    const x2 = cx + R*Math.cos(end),   y2 = cy + R*Math.sin(end);
    const x3 = cx + r*Math.cos(end),   y3 = cy + r*Math.sin(end);
    const x4 = cx + r*Math.cos(start), y4 = cy + r*Math.sin(start);
    svg += `
      <path d="M ${x1} ${y1} A ${R} ${R} 0 ${large} 1 ${x2} ${y2}
               L ${x3} ${y3} A ${r} ${r} 0 ${large} 0 ${x4} ${y4} Z"
            fill="${p.color}" opacity="0.9"></path>`;
    start = end;
  }
  svg += `<circle cx="${cx}" cy="${cy}" r="${r-1}" fill="var(--glass)" stroke="var(--border)"></circle>`;
  svg += `</svg>`;
  return svg;
}

function barsSVG({pos, neg, neu}) {
  const maxV = Math.max(1, pos, neg, neu);
  const scale = (v) => Math.round((v/maxV) * 160) + 2;
  const row = (y, label, v, color) => `
    <g transform="translate(0, ${y})">
      <text x="0" y="12" font-size="12" fill="var(--muted)">${label}</text>
      <rect x="70" y="2" width="${scale(v)}" height="12" rx="6" fill="${color}" opacity="0.9"></rect>
      <text x="${70+scale(v)+8}" y="12" font-size="12" fill="var(--text)">${v}</text>
    </g>`;
  return `<svg viewBox="0 0 260 80" width="100%" height="100%" aria-label="Counts Bar">
    ${row(4,'Positive', pos, 'var(--pos)')}
    ${row(28,'Negative', neg, 'var(--neg)')}
    ${row(52,'Neutral',  neu, 'var(--neu)')}
  </svg>`;
}

function renderStatsCards(sum) {
  const box = el('statsCards');
  const stats = [
    ['Total', sum.total],
    ['Positives', sum.positives],
    ['Negatives', sum.negatives],
    ['Neutral', sum.neutral],
    ['Positivity Ratio', sum.positivity_ratio],
    ['Avg Confidence', sum.avg_confidence],
  ];
  box.innerHTML = stats.map(([k,v]) => `
    <div class="stat"><div class="k">${k}</div><div class="v">${v}</div></div>
  `).join('');
}

function labelClass(label) {
  const L = (label||'').toUpperCase();
  if (L.startsWith('POS')) return 'pos';
  if (L.startsWith('NEG')) return 'neg';
  return 'neu';
}
function renderReviewsList(rows) {
  const wrap = el('reviewsList');
  if (!rows || !rows.length) { wrap.innerHTML = '<div class="rev">ยังไม่มีรีวิว</div>'; return; }
  const latest = rows.slice(-12).reverse();
  wrap.innerHTML = latest.map(r => `
    <div class="rev">
      <div class="line">
        <span class="badge ${labelClass(r.label)}">${r.label || '-'}${r.score!=null ? ' • ' + Number(r.score).toFixed(2) : ''}</span>
        ${r.timestamp ? `<span class="k">${r.timestamp}</span>` : ''}
      </div>
      <div class="text">${r.text || ''}</div>
      <div class="scorebar"><span style="width:${Math.round((r.score||0)*100)}%"></span></div>
    </div>
  `).join('');
}

async function onSearch() {
  const q = el('searchQuery').value.trim();
  if (!q) return;
  try {
    const data = await api(`/api/movies/search?query=${encodeURIComponent(q)}`);
    renderSearchGrid(data);
    const first = (data.Search && data.Search[0] && data.Search[0].imdbID) || '';
    if (first) el('imdbId').value = first;
  } catch (e) {
    renderSearchGrid({Search:[]});
    toast(e.message || e, 'err');
  }
}

async function onFetch() {
  const id = el('imdbId').value.trim();
  if (!id) return;
  try {
    const data = await api(`/api/movies/${id}`);
    renderMovieCard(data);
    CURRENT_ID = id;
    toast('Loaded movie details', 'ok');
  } catch (e) {
    renderMovieCard(null);
    toast(e.message || e, 'err');
  }
}

async function autoAnalyzeAndRefresh(id){
  try{
    await api(`/api/analyze/${id}`, { method: 'POST' });
    const sum = await api(`/api/summary/${id}`);
    const dataset = { pos: sum.positives, neg: sum.negatives, neu: sum.neutral };
    el('donutChart').innerHTML = donutSVG(dataset);
    el('barChart').innerHTML = barsSVG(dataset);
    renderStatsCards(sum);
    try {
      const detail = await api(`/api/analysis/${id}`);
      renderReviewsList(detail.rows);
    } catch { renderReviewsList([]); }
    toast('Analyzed successfully', 'ok');
  }catch(e){
    toast(e.message || e, 'err');
  }
}

async function onUpload(useSample=false) {
  const id = el('imdbId').value.trim();
  if (!id) return;
  try {
    let data;
    if (useSample) {
      data = await api(`/api/reviews/${id}/use-sample`, { method: 'POST' });
    } else {
      const f = el('reviewsFile').files[0];
      if (!f) { toast('กรุณาเลือกไฟล์ CSV หรือ JSON','err'); return; }
      const fd = new FormData();
      fd.append('file', f);
      data = await api(`/api/reviews/${id}/upload`, { method: 'POST', body: fd });
    }
    CURRENT_ID = id;
    await autoAnalyzeAndRefresh(id);
  } catch (e) {
    toast(e.message || e, 'err');
  }
}

async function onGenMock() {
  const id = (CURRENT_ID || el('imdbId').value.trim());
  if (!id) return;
  try {
    await api(`/api/reviews/${id}/generate?count=40`, { method: 'POST' });
    await autoAnalyzeAndRefresh(id);
  } catch (e) { toast(e.message || e, 'err'); }
}

async function onFetchTMDb() {
  const id = (CURRENT_ID || el('imdbId').value.trim());
  if (!id) return;
  try {
    await api(`/api/reviews/${id}/import/tmdb?max_pages=1`, { method: 'POST' });
    await autoAnalyzeAndRefresh(id);
  } catch (e) { toast(e.message || e, 'err'); }
}

async function onExport() {
  const id = CURRENT_ID || el('imdbId').value.trim();
  if (!id) return;
  try {
    const res = await fetch(`/api/export/${id}.csv`);
    if (!res.ok) throw new Error(await res.text());
    const blob = await res.blob();
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${id}_analysis.csv`;
    a.click();
    URL.revokeObjectURL(url);
    toast('Exported CSV', 'ok');
  } catch (e) { toast(e.message || e, 'err'); }
}

async function onAnalyzeText() {
  const t = el('oneText').value.trim();
  if (!t) return;
  try {
    const data = await api('/api/analyze-text', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({text: t})
    });
    toast(`Label: ${data.label} • Score: ${Number(data.score).toFixed(2)}`, 'ok');
  } catch (e) {
    toast(e.message || e, 'err');
  }
}

async function onAddComment(){
  const id = CURRENT_ID || el('imdbId').value.trim();
  if (!id) { toast('กรุณาเลือก/ดึงข้อมูลหนังก่อน','err'); return; }
  const tEl = el('newComment');
  const t = tEl.value.trim();
  if (!t) { toast('กรุณาพิมพ์คอมเมนต์','err'); return; }
  try{
    await api(`/api/reviews/${id}/add`, {
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify({ text: t, source: 'user' })
    });
    tEl.value = '';
    updateCommentCounter();
    await autoAnalyzeAndRefresh(id);
  }catch(e){ toast(e.message || e, 'err'); }
}

function updateCommentCounter(){
  const tEl = el('newComment');
  const cEl = el('commentCounter');
  if (!tEl || !cEl) return;
  const max = 280;
  const len = (tEl.value || '').length;
  cEl.textContent = `${len} / ${max}`;
  cEl.style.color = len > max ? '#ff9aa2' : 'var(--muted)';
}

// Wire events
el('btnSearch').onclick = onSearch;
el('btnFetch').onclick = onFetch;
el('btnUseSample').onclick = () => onUpload(true);
el('btnGenMock').onclick = onGenMock;
el('btnFetchTMDb').onclick = onFetchTMDb;
el('btnExport').onclick = onExport;
el('btnOneText').onclick = onAnalyzeText;
const addBtn = document.getElementById('btnAddComment');
if (addBtn) addBtn.onclick = onAddComment;
const newComment = document.getElementById('newComment');
if (newComment){
  newComment.addEventListener('input', updateCommentCounter);
  newComment.addEventListener('keydown', (e)=>{
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
      e.preventDefault();
      onAddComment();
    }
  });
  updateCommentCounter();
}

// Support direct file click
const fileInputLabel = document.querySelector('label.file');
if (fileInputLabel) {
  fileInputLabel.addEventListener('change', () => onUpload(false));
}
