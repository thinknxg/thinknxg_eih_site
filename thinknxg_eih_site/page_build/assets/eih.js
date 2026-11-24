(function(){
function ready(f){document.readyState!=="loading"?f():document.addEventListener("DOMContentLoaded",f)}
ready(function(){
var b=document.querySelector(".eih-burger"),m=document.querySelector(".eih-navlinks");
if(b&&m){b.addEventListener("click",function(){var o=m.style.display==="flex";m.style.display=o?"none":"flex";b.setAttribute("aria-expanded",String(!o))});
m.addEventListener("click",function(e){if(e.target.closest("a")&&window.innerWidth<=640){m.style.display="none";b.setAttribute("aria-expanded","false")}})}
var L=document.querySelectorAll(".eih-layer"),P=document.querySelectorAll(".eih-panel");
L.forEach(function(l){l.addEventListener("click",function(){var i=l.getAttribute("data-eih-layer");L.forEach(function(x){x.classList.toggle("on",x===l)});P.forEach(function(p){p.classList.toggle("on",p.getAttribute("data-eih-panel")===i)})})});
if("IntersectionObserver" in window){var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add("in");io.unobserve(e.target)}})},{threshold:.08});
document.querySelectorAll(".eih-card").forEach(function(el){el.classList.add("eih-reveal");io.observe(el)});setTimeout(function(){document.querySelectorAll(".eih-reveal").forEach(function(e){e.classList.add("in")})},3000)}
var f=document.getElementById("eih-enquiry");if(!f)return;
var st=document.getElementById("eih-status");
function say(t,c){st.textContent=t;st.className="eih-status "+c}
f.addEventListener("submit",function(ev){ev.preventDefault();
var bad=false;f.querySelectorAll("[required]").forEach(function(el){var v=el.type==="checkbox"?el.checked:el.value.trim();el.classList.toggle("bad",!v);if(!v)bad=true});
var em=f.elements.business_email;if(em.value&&!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(em.value)){em.classList.add("bad");bad=true}
if(bad){say("Please complete the highlighted fields.","err");return}
var d={doctype:"E-Invoice Hub Enquiry"};["full_name","business_email","company","country","erp_system","required_compliance","existing_asp","invoice_volume","message","website_url"].forEach(function(k){d[k]=f.elements[k].value.trim()});
d.consent=1;d.source_page=location.pathname;
var btn=f.querySelector(".eih-submit");btn.disabled=true;say("Sending...","");
fetch("/api/method/thinknxg_eih_site.api.enquiry.submit_enquiry",{method:"POST",headers:{"Content-Type":"application/json","Accept":"application/json","X-Frappe-CSRF-Token":(window.csrf_token&&window.csrf_token!=="{{ csrf_token }}")?window.csrf_token:""},body:JSON.stringify(d)})
.then(function(r){return r.json().then(function(j){return{ok:r.ok,j:j}})}).then(function(x){btn.disabled=false;
if(x.ok){f.reset();say("Thank you. Your enquiry has been received and our team will respond.","ok")}
else{var msg="Could not send your enquiry. Please check the details and try again.";try{var s=JSON.parse(x.j._server_messages||"[]");if(s.length)msg=JSON.parse(s[0]).message.replace(/<[^>]+>/g,"")}catch(e){}say(msg,"err")}})
.catch(function(){btn.disabled=false;say("Network error. Please try again.","err")})})
})})();
