(()=>{
let DATA=null;
const COPY={
 it:{label:'Casi recenti comparabili',title:'Somiglianze con F-002 che non furono fatali',intro:'Questi casi vengono selezionati automaticamente dall’ultimo snapshot NTSB acquisito da AGGIORNA. Sono contesto comparativo, non “successi” della previsione: devono essere Boeing commerciali non fatali, coerenti con 737-800/737 NG e con la fase approach/landing oppure con il cluster carrello/strutturale.',warning:'Confronto descrittivo ≠ validazione. Un caso non fatale non soddisfa il target primario di F-002, che richiede il prossimo incidente fatale qualificante, e non modifica il suo punteggio.',empty:'Nessun caso nello snapshot corrente supera la regola automatica di comparabilità.',exact_model:'modello esatto 737-800',family_737_ng:'famiglia 737 NG',approach_landing:'approach / landing',gear_structural_cluster:'cluster carrello / strutturale',source:'Fonte',fatalities:'Vittime'},
 en:{label:'Recent comparable cases',title:'Similarities to F-002 that were non-fatal',intro:'These cases are selected automatically from the latest NTSB snapshot acquired by AGGIORNA. They are comparative context, not forecast “hits”: they must be non-fatal commercial Boeing cases consistent with the 737-800/737 NG hypothesis and either approach/landing phase or the gear/structural cluster.',warning:'Descriptive comparison ≠ validation. A non-fatal case does not satisfy F-002’s primary target, which requires the next qualifying fatal accident, and it does not change its score.',empty:'No case in the current snapshot passes the automatic comparability rule.',exact_model:'exact 737-800 model',family_737_ng:'737 NG family',approach_landing:'approach / landing',gear_structural_cluster:'gear / structural cluster',source:'Source',fatalities:'Fatalities'}
};
function lang(){return window.BSFM_I18N?.lang?.()||document.documentElement.lang||'it'}
function esc(s){return String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}
function render(l=lang()){
 const c=COPY[l]||COPY.it, cases=DATA?.cases||[];
 const cards=cases.length?cases.map(x=>`<article class="card s6"><div class="report-head"><strong>${esc(x.model)} · ${esc(x.carrier)}</strong><span class="report-date">${esc(x.event_date)}</span></div><p class="muted">NTSB ${esc(x.event_id||'—')} · ${esc(x.phase||'—')}</p><div class="report-meta">${(x.similarity_tags||[]).map(t=>`<span class="tag">${esc(c[t]||t)}</span>`).join('')}</div><p class="help">${esc(c.fatalities)}: ${Number(x.fatalities||0)} · ${esc(c.source)}: ${esc(x.source||DATA?.source||'NTSB')}</p></article>`).join(''):`<div class="empty">${esc(c.empty)}</div>`;
 const meta=DATA?`<p class="help">${esc(DATA.source_scope||'')}</p>`:'';
 const html=`<section class="section" id="comparable-cases"><div class="section-title"><div class="label">${esc(c.label)}</div><h2>${esc(c.title)}</h2><p class="muted">${esc(c.intro)}</p>${meta}</div><div class="grid">${cards}</div><div class="notice"><strong>${esc(c.warning)}</strong></div></section>`;
 const host=document.getElementById('comparable-cases'); if(host){host.outerHTML=html;return}
 const anchor=document.getElementById('real-data'); if(anchor)anchor.insertAdjacentHTML('beforebegin',html);
}
function load(){fetch('./data/comparable-cases.json',{cache:'no-store'}).then(r=>r.ok?r.json():Promise.reject()).then(x=>{DATA=x;render()}).catch(()=>{DATA={cases:[]};render()})}
document.addEventListener('DOMContentLoaded',load);
window.addEventListener('bsfm-language',e=>render(e.detail));
})();
