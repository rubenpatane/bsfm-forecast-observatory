(()=>{
const UI={
 it:{label:'Bacheca in evidenza · aggiornamento manuale',pending:'IN ATTESA DI FONTI UFFICIALI',updated:'Aggiornata manualmente',event:'Evento segnalato',close:'Dove PD14 si avvicina',limits:'Dove non coincide',verdict:'Verdetto editoriale provvisorio',sources:'Fonti disponibili',sourceNote:'Queste fonti documentano la segnalazione iniziale. Non sostituiscono il futuro record ufficiale necessario per la valutazione e il punteggio.',manual:'Questa bacheca non viene modificata da AGGIORNA e non produce effetti sul modello, sul forecast congelato o sul punteggio.'},
 en:{label:'Featured board · manual update',pending:'AWAITING OFFICIAL SOURCES',updated:'Manually updated',event:'Reported event',close:'Where PD14 is close',limits:'Where it does not match',verdict:'Provisional editorial verdict',sources:'Available sources',sourceNote:'These sources document the initial report. They do not replace the future official record required for adjudication and scoring.',manual:'This board is not modified by AGGIORNA and has no effect on the model, frozen forecast or score.'}
};
let DATA=null;
const esc=value=>String(value??'').replace(/[&<>"']/g,char=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
const local=(value,lang)=>typeof value==='object'&&value!==null?(value[lang]??value.it??value.en??''):value;
function safeLink(value){try{const url=new URL(value);return url.protocol==='https:'?url.href:null}catch{return null}}
function renderList(items,lang){return `<ul>${(items||[]).map(item=>`<li>${esc(local(item,lang))}</li>`).join('')}</ul>`}
function render(data,lang=window.BSFM_I18N?.lang?.()||'it'){
 const copy=UI[lang]||UI.it,entry=data.entry||{};
 const timeline=(entry.timeline||[]).map(item=>`<div class="editorial-time editorial-time-${esc(item.kind)}"><span>${esc(item.display)}</span><strong>${esc(local(item.label,lang))}</strong></div>`).join('');
 const signals=(entry.signals||[]).map(item=>`<div class="editorial-signal"><strong>${esc(lang==='en'?(item.value_en||item.value):item.value)}</strong><span>${esc(local(item.label,lang))}</span></div>`).join('');
 const sources=(entry.sources||[]).map(source=>{const url=safeLink(source.url);return url?`<a href="${esc(url)}" target="_blank" rel="noopener noreferrer">${esc(source.publisher)}</a>`:esc(source.publisher)}).join('<span aria-hidden="true">·</span>');
 const html=`<article class="editorial-shell"><div class="editorial-head"><div><div class="label">${copy.label}</div><div class="editorial-date">${copy.updated}: ${esc(data.updated_on)}</div></div><span class="status-chip pending">${copy.pending}</span></div><h2>${esc(local(entry.title,lang))}</h2><p class="editorial-intro">${esc(local(entry.intro,lang))}</p><div class="editorial-event"><strong>${copy.event}</strong><span>${esc(entry.event?.flight)} · ${esc(entry.event?.aircraft)} · ${esc(local(entry.event?.route,lang))}</span><p>${esc(local(entry.event?.provisional_summary,lang))}</p></div><div class="editorial-timeline" aria-label="Timeline">${timeline}</div><div class="editorial-signals">${signals}</div><div class="editorial-compare"><div class="editorial-column editorial-close"><h3>${copy.close}</h3>${renderList(entry.similarities,lang)}</div><div class="editorial-column editorial-limits"><h3>${copy.limits}</h3>${renderList(entry.limits,lang)}</div></div><div class="editorial-verdict"><div><span>${copy.verdict}</span><strong>${esc(entry.verdict?.code)}</strong></div><p>${esc(local(entry.verdict,lang))}</p></div><div class="editorial-sources"><strong>${copy.sources}</strong><div>${sources}</div><p>${copy.sourceNote}</p></div><p class="editorial-manual">${copy.manual}</p></article>`;
 document.querySelectorAll('[data-editorial-board]').forEach(host=>{host.innerHTML=html});
}
fetch('./data/editorial-board.json',{cache:'no-store'}).then(response=>{if(!response.ok)throw Error(response.status);return response.json()}).then(data=>{DATA=data;render(data)}).catch(()=>{});
window.addEventListener('bsfm-language',event=>{if(DATA)render(DATA,event.detail)});
})();
