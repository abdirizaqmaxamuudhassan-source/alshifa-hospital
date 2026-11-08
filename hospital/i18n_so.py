"""Lightweight English -> Somali translation of rendered pages (text between tags, placeholders)."""
import re
PAIRS = """Home|Bogga Hore
About|Nagu Saabsan
Departments|Waaxaha
Doctors|Dhakhaatiirta
Services|Adeegyada
Contact|Nala Xiriir
My Portal|Boggayga
Dashboard|Gudiga Maamulka
Logout|Ka bax
Login|Gal
Book Appointment|Ballan Qabso
Modern Hospital|Isbitaalka Casriga ah
&copy; Al-Shifa Modern Hospital|&copy; Isbitaalka Casriga ah ee Al-Shifa
Emergency: +252 61 0000000 (24/7)|Degdeg: +252 61 0000000 (24/7)
Trusted care since 1998|Daryeel la aamino tan iyo 1998
Your health, in safe hands.|Caafimaadkaaga, gacmo aamin ah.
Al-Shifa Modern Hospital brings specialist doctors, advanced diagnostics and 24/7 emergency care under one roof.|Isbitaalka Casriga ah ee Al-Shifa wuxuu hal saqaf hoostiis ku keenay dhakhaatiir takhasus leh, baaritaano casri ah iyo daryeel degdeg ah 24/7.
Find a Doctor|Raadi Dhakhtar
Emergency 24/7|Degdeg 24/7
Ambulance: +252 61 1111111|Ambalaas: +252 61 1111111
Opening Hours|Saacadaha Shaqada
Mon - Fri|Isniin - Jimce
Saturday|Sabti
Sunday|Axad
Emergency & OPD 10:00 - 14:00|Degdeg & OPD 10:00 - 14:00
Our Medical Services|Adeegyadayada Caafimaadka
Featured Doctors|Dhakhaatiirta Gaarka ah
Patient Testimonials|Qiimeynta Bukaanleyda
Book|Ballan
sano|sano
yrs|sano
doctor|dhakhtar
doctors|dhakhtar
About Al-Shifa|Ku Saabsan Al-Shifa
Our History|Taariikhdeenna
Founded in 1998 as a 30-bed clinic, Al-Shifa has grown into a multi-specialty hospital serving thousands of families every year.|Waxaa la aasaasay 1998 isagoo rug caafimaad oo 30 sariirood ah, Al-Shifa wuxuu noqday isbitaal takhasusyo badan leh oo sannad kasta u adeega kumanaan qoys.
Mission|Hadafka
Deliver safe, affordable, compassionate care.|In la bixiyo daryeel ammaan ah, qiimo jaban oo naxariis leh.
Vision|Aragtida
To be the region's most trusted healthcare partner.|In aan noqonno lammaanaha caafimaadka ee ugu la aaminsan gobolka.
Facilities|Xarumaha
24/7 emergency & trauma unit|Waaxda degdegga iyo dhaawaca 24/7
Modern operating theatres|Qolalka qalliinka casriga ah
ICU & NICU|ICU & NICU
In-house pharmacy & laboratory|Farmasi iyo shaybaar isbitaalka ku jira
Medical Equipment|Qalabka Caafimaadka
MRI & CT scanners|Mashiinnada MRI & CT
Digital X-ray & ultrasound|X-ray dhijitaal ah & ultrasound
ECG / Echo cardiography|ECG / Echo wadnaha
Automated lab analyzers|Mashiinno shaybaar oo is-shaqeeya
Our Medical Team|Kooxdayada Caafimaadka
Our Doctors|Dhakhaatiirtayada
Search by name or specialization|Ku raadi magac ama takhasus
All departments|Waaxaha oo dhan
Search|Raadi
No doctors found.|Dhakhtar lama helin.
Book an Appointment|Ballan Qabso
Request Appointment|Codso Ballan
Your request is Pending until approved by hospital staff.|Codsigaagu wuu sugayaa ilaa shaqaalaha isbitaalku ansixiyo.
Patient Registration|Diiwaangelinta Bukaanka
Create Account|Samee Akoon
Already registered?|Horey ma isku diiwaangelisay?
New patient?|Bukaan cusub?
Register|Is diiwaangeli
Contact Us|Nala Soo Xiriir
Buunda Weyn, Baydhabo (Baidoa), Somalia|Buunda Weyn, Baydhabo, Soomaaliya
Get Directions|Hel Jihada
Send Message|Dir Farriin
Name|Magaca
Phone|Telefoon
Department|Waaxda
Doctor|Dhakhtarka
Date|Taariikhda
Time|Waqtiga
Reason|Sababta
Email|Iimaylka
Message|Farriinta
Username|Magaca isticmaalaha
First name|Magaca koowaad
Last name|Magaca dambe
Password|Furaha sirta ah
Password confirmation|Xaqiiji furaha sirta ah
Date cannot be in the past.|Taariikhdu ma noqon karto mid hore.
Doctor is not in that department.|Dhakhtarkaasi kuma jiro waaxdaas.
That slot is already booked.|Waqtigaas horay ayaa loo qabsaday.
Thank you! Your message has been received.|Mahadsanid! Farriintaada waa la helay.
Appointment requested. Status: Pending admin approval.|Ballanta waa la codsaday. Xaalad: Waxay sugaysaa ansixinta maamulka.
Welcome to Al-Shifa!|Ku soo dhawoow Al-Shifa!
Appointment approved.|Ballanta waa la ansixiyay.
Appointment rejected.|Ballanta waa la diiday.
Appointment completed.|Ballanta waa la dhammeeyay.
This account is a staff account.|Akoonkani waa akoon shaqaale.
Open dashboard|Fur gudiga maamulka
Profile|Astaanta
Medical history|Taariikhda caafimaad
No records yet.|Weli diiwaan ma jiro.
Appointment History|Taariikhda Ballamaha
Dept|Waaxda
Status|Xaalad
Pending|Sugaya
Approved|La ansixiyay
Rejected|La diiday
Completed|La dhammeeyay
None yet.|Weli ma jiro.
Book one|Ballan qabso
Prescriptions|Warqadaha Daawada
No prescriptions.|Warqad daawo ma jirto.
Lab Results|Natiijooyinka Shaybaarka
No lab results.|Natiijo shaybaar ma jirto.
Manage|Maamul
Patients|Bukaanleyda
Appointments|Ballamaha
Staff & Users|Shaqaalaha & Isticmaalayaasha
Payments|Lacag-bixinta
Pharmacy|Farmasiga
Laboratory|Shaybaarka
Website Content|Nuxurka Website-ka
Report (CSV)|Warbixin (CSV)
Today|Maanta
Revenue (paid)|Dakhliga (la bixiyay)
Monthly Appointments|Ballamaha Bishiiba
Patient Growth|Kobaca Bukaanleyda
Revenue Analytics|Falanqaynta Dakhliga
Appointments by Status|Ballamaha Iyadoo la eegayo Xaalad
Search name or phone|Raadi magac ama telefoon
All statuses|Dhammaan xaaladaha
Filter|Shaandhee
Patient|Bukaanka
When|Goorma
Action|Tallaabo
Approve|Ansixi
Reject|Diid
Done|La dhammeeyay
No appointments.|Ballan ma jiro.
Cardiology|Wadnaha
Pediatrics|Carruurta
Neurology|Neerfaha
Dentistry|Ilkaha
Gynecology|Haweenka
Orthopedics|Lafaha iyo Kala-goysyada
Emergency Department|Waaxda Xaaladaha Degdegga
General Medicine|Daawada Guud
Heart and vascular care.|Daryeelka wadnaha iyo xididdada.
Care for infants and children.|Daryeelka dhallaanka iyo carruurta.
Brain, spine and nerve care.|Daryeelka maskaxda, laf-dhabarta iyo neerfaha.
Oral and dental health.|Caafimaadka afka iyo ilkaha.
Women's health and maternity.|Caafimaadka haweenka iyo dhalmada.
Bones, joints and sports injuries.|Lafaha, kala-goysyada iyo dhaawacyada ciyaaraha.
24/7 emergency and trauma care.|Daryeel degdeg ah iyo dhaawac 24/7.
Primary and family care.|Daryeelka aasaasiga ah iyo qoyska.
Emergency Care|Daryeel Degdeg ah
24/7 trauma and emergency response.|Jawaab degdeg ah iyo dhaawac 24/7.
Accurate diagnostic testing.|Baaritaano sax ah oo cudurada lagu ogaado.
In-house pharmacy open daily.|Farmasi isbitaalka ku jirta oo furan maalin kasta.
Surgery|Qalliin
Modern operating theatres.|Qolalka qalliinka casriga ah.
Medical Checkups|Baaritaan Caafimaad
Preventive health packages.|Xidhmooyin ka hortag caafimaad.
Ambulance Services|Adeegga Ambalaasta
Fully equipped ambulances.|Ambalaasyo qalab buuxa leh."""
D = dict(l.split("|", 1) for l in PAIRS.splitlines())
RULES = [(r"^Welcome, (.*)$", r"Soo dhawoow, \1"), (r"^Phone: (.*)$", r"Telefoon: \1"),
         (r"^Email: (.*)$", r"Iimayl: \1"), (r"^Blood group: (.*)$", r"Nooca dhiigga: \1")]
_seg = re.compile(r">([^<>]+)<")
_attr = re.compile(r'(placeholder|title)="([^"]+)"')

def _t(s):
    if s in D: return D[s]
    for p, r in RULES:
        if re.search(p, s): return re.sub(p, r, s)
    return None

def translate_html(html):
    def seg(m):
        raw = m.group(1); s = raw.strip(); out = _t(s) if s else None
        if out is None: return m.group(0)
        return ">" + raw[:len(raw)-len(raw.lstrip())] + out + raw[len(raw.rstrip()):] + "<"
    html = _seg.sub(seg, html)
    html = _attr.sub(lambda m: f'{m.group(1)}="{_t(m.group(2)) or m.group(2)}"', html)
    return html.replace('<html lang="en">', '<html lang="so">', 1)

D.update({"Ambulance & Emergency 24/7": "Ambalaas & Degdeg 24/7", "Emergency Call": "Wicitaan Degdeg ah"})
