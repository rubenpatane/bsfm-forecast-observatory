(()=>{
function format(value,l,digits=5){return Number(value).toLocaleString(l==='it'?'it-IT':'en-GB',{minimumFractionDigits:digits,maximumFractionDigits:digits})}
function render(data,l=window.BSFM_I18N?.lang?.()||'it'){
 const candidate=Number(data.candidate_mean_log_score),baseline=Number(data.baseline_mean_log_score),max=Math.max(candidate,baseline)||1;
 document.getElementById('candidateScore').textContent=format(candidate,l);document.getElementById('baselineScore').textContent=format(baseline,l);document.getElementById('candidateBar').style.width=`${100*candidate/max}%`;document.getElementById('baselineBar').style.width=`${100*baseline/max}%`;document.getElementById('eventFolds').textContent=data.event_bearing_fold_count;document.getElementById('minimumFolds').textContent=data.minimum_event_bearing_folds;document.getElementById('foldCount').textContent=data.fold_count;
 const difference=Number(data.mean_log_score_improvement)*-1;document.getElementById('scoreDifference').textContent=`+${format(difference,l)} · ${l==='it'?'peggiore':'worse'}`;
}
let DATA=null;fetch('./data/public-data-validation.json',{cache:'no-store'}).then(r=>{if(!r.ok)throw Error(r.status);return r.json()}).then(x=>{DATA=x;render(x)}).catch(()=>{});window.addEventListener('bsfm-language',e=>{if(DATA)render(DATA,e.detail)});
})();
