(()=>{
const COPY={
 it:{
  title:'Nuova previsione automatica da sole fonti pubbliche online',
  intro:'È un record prospettico separato da F-002. Il modello usa T-100 e soli esiti autoritativi disponibili al cutoff, riaffina i parametri sotto regole congelate e non rivendica ancora capacità predittiva.',
  waiting:'Contratto preregistrato: nessuna previsione ancora emessa',
  waitingBody:'La prima previsione può essere creata soltanto da un AGGIORNA successivo al commit del contratto. Questo impedisce di adattare le regole al risultato.',
  status:'Stato',version:'Versione',cutoff:'Cutoff dati',horizon:'Orizzonte',modal:'Giorno più probabile',interval:'Intervallo temporale 80%',family:'Famiglia più probabile',training:'Esiti PIT in addestramento',exposure:'Ultima esposizione ammissibile',
  conditional:'Condizionato al verificarsi del target entro i 90 giorni',
  sources:'Fonti online',sourcesBody:'BTS T-100 Segment · NTSB AVALL per discovery · autorità investigative/aviazione civile per l’adjudication.',
  limit:'Sperimentale e non validata',limitBody:'Il backtest BSFM-PD 1.3 resta negativo e con 3 finestre-evento su 10 richieste. Qui non viene pubblicata una probabilità assoluta di incidente e il risultato non valuta voli, operatori o aeromobili specifici.',
  extra:'Ipotesi sui dati aggiuntivi',extraBody:'Esposizione globale e precursori PIT potrebbero aggiungere informazione, ma il miglioramento non è assunto. Potrà essere affermato solo dopo un confronto appaiato su cutoff futuri identici.',
  record:'Apri il record immutabile',unavailable:'Stato della previsione pubblica non disponibile.'
 },
 en:{
  title:'New automated forecast from public online sources only',
  intro:'This is a prospective record separate from F-002. The model uses T-100 and only authoritative outcomes available at the cutoff, refits parameters under frozen rules, and does not yet claim predictive skill.',
  waiting:'Preregistered contract: no forecast issued yet',
  waitingBody:'The first forecast may be created only by an AGGIORNA run after the contract commit. This prevents fitting the rules to the result.',
  status:'Status',version:'Version',cutoff:'Data cutoff',horizon:'Horizon',modal:'Most likely day',interval:'80% time interval',family:'Most likely family',training:'PIT outcomes in training',exposure:'Latest admissible exposure',
  conditional:'Conditional on the target occurring within the 90-day horizon',
  sources:'Online sources',sourcesBody:'BTS T-100 Segment · NTSB AVALL for discovery · accident-investigation/civil-aviation authorities for adjudication.',
  limit:'Experimental and unvalidated',limitBody:'The BSFM-PD 1.3 backtest remains negative with 3 event-bearing windows against 10 required. No absolute accident probability is published here, and this output does not assess a specific flight, operator or aircraft.',
  extra:'Additional-data hypothesis',extraBody:'Global exposure and PIT precursors may add information, but improvement is not assumed. It may be claimed only after a paired comparison on identical future cutoffs.',
  record:'Open immutable record',unavailable:'Public forecast state unavailable.'
 }};
let DATA=null;
function esc(value){return String(value??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}
function dateText(value,l){if(!value)return '—';const date=new Date(`${value}T12:00:00Z`);return new Intl.DateTimeFormat(l==='it'?'it-IT':'en-GB',{dateStyle:'medium',timeZone:'UTC'}).format(date)}
function render(data,l=window.BSFM_I18N?.lang?.()||'it'){
 const c=COPY[l]||COPY.it,host=document.getElementById('publicDataForecast');if(!host)return;
 if(!data?.prediction){host.innerHTML=`<h2>${c.title}</h2><p class="muted">${c.intro}</p><div class="notice info"><strong>${c.waiting}</strong><div class="muted">${c.waitingBody}</div></div><div class="gates"><div class="gate"><span>${c.status}</span><b class="no">${esc(data?.status||'PREREGISTERED')}</b></div><div class="gate"><span>${c.version}</span><b>BSFM-PD ${esc(data?.model_version||'1.4')}</b></div></div>`;return;
 }
 const p=data.prediction,interval=p.conditional_interval_80||{},families=Object.entries(p.family_distribution_conditional||{}).sort((a,b)=>Number(b[1])-Number(a[1])),top=families[0]||['—',0];
 const record=data.record_path?`<a class="button" target="_blank" rel="noopener noreferrer" href="https://github.com/rubenpatane/bsfm-forecast-observatory/blob/main/${encodeURI(data.record_path)}">${c.record}</a>`:'';
 host.innerHTML=`<h2>${c.title}</h2><p class="muted">${c.intro}</p><div class="gates"><div class="gate"><span>${c.status}</span><b class="no">${esc(data.status)}</b></div><div class="gate"><span>${c.version}</span><b>BSFM-PD ${esc(data.model_version)}</b></div><div class="gate"><span>${c.cutoff}</span><b>${dateText(data.cutoff,l)}</b></div><div class="gate"><span>${c.horizon}</span><b>${dateText(p.start_date,l)} → ${dateText(p.horizon_end,l)}</b></div></div><div class="facts"><div class="fact"><span class="muted">${c.modal}</span><strong>${dateText(p.modal_date,l)}</strong><small>${c.conditional}</small></div><div class="fact"><span class="muted">${c.interval}</span><strong>${dateText(interval.lower,l)} → ${dateText(interval.upper,l)}</strong><small>${c.conditional}</small></div><div class="fact"><span class="muted">${c.family}</span><strong>${esc(top[0])}</strong><small>${c.conditional}</small></div><div class="fact"><span class="muted">${c.training}</span><strong>${esc(data.training?.outcome_count??'—')}</strong></div><div class="fact"><span class="muted">${c.exposure}</span><strong>${esc(data.training?.latest_exposure_period??'—')}</strong></div></div><div class="grid"><div class="notice info s6"><strong>${c.sources}</strong><div class="muted">${c.sourcesBody}</div></div><div class="notice warning s6"><strong>${c.limit}</strong><div class="muted">${c.limitBody}</div></div><div class="notice info full"><strong>${c.extra}</strong><div class="muted">${c.extraBody}</div></div></div><div class="button-row">${record}</div>`;
}
fetch('./data/public-data-forecast.json',{cache:'no-store'}).then(r=>{if(!r.ok)throw Error(r.status);return r.json()}).then(data=>{DATA=data;render(data)}).catch(()=>{const host=document.getElementById('publicDataForecast');if(host)host.textContent=COPY[window.BSFM_I18N?.lang?.()||'it'].unavailable});
window.addEventListener('bsfm-language',event=>{if(DATA)render(DATA,event.detail)});
})();
