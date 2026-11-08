const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}}),{threshold:.1});
document.querySelectorAll('.reveal').forEach(el=>io.observe(el));
// Booking form: only show doctors of the chosen department
const dep=document.getElementById('id_department'),doc=document.getElementById('id_doctor');
if(dep&&doc&&window.DOCTOR_DEPTS){const filter=()=>{[...doc.options].forEach(o=>{o.hidden=o.value&&String(DOCTOR_DEPTS[o.value])!==dep.value&&dep.value!=='';});
 const s=doc.selectedOptions[0];if(s&&s.hidden)doc.value=''};dep.addEventListener('change',filter);filter()}
