(()=>{
let DATA=null;
const $=id=>document.getElementById(id);
function lang(){return window.BSFM_I18N?.lang?.()||document.documentElement.lang||'it'}
function date(value,l){if(!value)return '—';const d=new Date(`${value}T12:00:00Z`);return new Intl.DateTimeFormat(l==='it'?'it-IT':'en-GB',{day:'numeric',month:'short',year:'numeric',timeZone:'UTC'}).format(d)}
function render(l=lang()){
 if(!DATA)return;const p=DATA.prediction||{};
 $('forecastModel').textContent=DATA.model_version||'—';$('forecastCutoff').textContent=date(DATA.cutoff,l);$('forecastWindow').textContent=`${date(p.modal_week?.start,l)} – ${date(p.modal_week?.end,l)}`;$('forecastDay').textContent=date(p.modal_day,l);$('forecastPrimary').textContent=p.primary_family_variant||'—';$('forecastSecondary').textContent=p.secondary_family_variant||'—';$('forecastPhase').textContent=p.phase||'—';$('forecastCluster').textContent=p.primary_event_class||'—';$('forecastAlternative').textContent=p.alternative_event_class||'—';$('forecastGeography').textContent=(p.geography||[]).join(' / ')||'—';$('forecastOperator').textContent=p.operator||'—';$('forecastMsn').textContent=p.msn||'—';$('forecastIntegrity').textContent=DATA.integrity||'—';
}
fetch('./data/forecast.json',{cache:'no-store'}).then(r=>{if(!r.ok)throw Error(r.status);return r.json()}).then(x=>{DATA=x;render()}).catch(()=>{});
window.addEventListener('bsfm-language',e=>render(e.detail));
})();
