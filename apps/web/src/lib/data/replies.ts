export interface DraftReply {
	docId: string;
	subject: string;
	body: string;
}

export const DRAFT_REPLIES: DraftReply[] = [
	{
		docId: 'email_client_apartament_bucuresti',
		subject: 'Re: Cerere ofertă amenajare apartament 3 camere',
		body: `Bună ziua, domnule Enache,

Vă mulțumim pentru interesul acordat serviciilor Atelier Nova și pentru detaliile transmise.

Pentru a putea elabora o ofertă personalizată și cât mai precisă pentru apartamentul dumneavoastră din București (aprox. 78 mp, 3 camere), avem nevoie de câteva informații suplimentare:

1. Planul de arhitectură sau un schițat al spațiului (cu dimensiuni orientative)
2. Fotografii ale stării actuale a apartamentului
3. Stilul preferat de design (ex. modern, scandinav, industrial, clasic)
4. Bugetul orientativ disponibil pentru amenajare
5. Nivelul de implicare dorit — consultanță, proiect complet sau coordonare furnizori

Ca referință orientativă, un proiect complet de design interior pentru un apartament de această dimensiune pornește de la 3.500 RON pentru serviciile de proiectare, la care se adaugă costurile de execuție și mobilier.

Suntem disponibili pentru o întâlnire de consultație inițială, online sau la sediul nostru, oricând săptămâna viitoare.

Cu stimă,
Echipa Atelier Nova SRL`
	},
	{
		docId: 'email_client_showroom_pitesti',
		subject: 'Re: Update proiect Showroom Pitești — stadiu lucrări',
		body: `Bună ziua, domnule Popescu,

Vă mulțumim pentru mesaj și înțelegem importanța prezentării planificate.

Referitor la termenele proiectului, dorim să clarificăm un aspect: conform contractului nr. 07 din 10.04.2026, termenul pentru finalizarea Fazei 1 (finisaje pereți și pardoseală) este **30 mai 2026**, nu 15 mai. Bineînțeles, depunem toate eforturile pentru a respecta acest termen și, dacă evoluția lucrărilor o permite, vom comunica orice avans față de planificare.

Stadiul actual al lucrărilor este conform graficului. Putem organiza o vizită la locație săptămâna viitoare pentru un update detaliat, dacă doriți.

Vă vom contacta imediat ce Faza 1 este finalizată, pentru a programa recepția parțială.

Cu stimă,
Echipa Atelier Nova SRL`
	},
	{
		docId: 'email_client_intarziere_livrare',
		subject: 'Re: Întârziere livrare comandă mobilier',
		body: `Bună ziua, doamnă Dumitrescu,

Vă mulțumim că ne-ați contactat și ne cerem scuze sincer pentru întârzierea de 5 zile față de termenul confirmat.

Întârzierea a fost cauzată de o disfuncționalitate la un furnizor terț de transport, situație pe care nu am anticipat-o și pe care ne-o asumăm integral, indiferent de cauza externă.

Apreciem că ne-ați semnalat situația cu calm și în mod direct. Ca gest de bună-voință, vă oferim o **reducere de 5% la valoarea comenzii curente** sau, dacă preferați, un **discount de 8% la o viitoare comandă** plasată în următoarele 6 luni.

Vă rugăm să ne comunicați preferința și vom emite documentele corespunzătoare.

Mulțumim pentru înțelegere și colaborare.

Cu respect,
Echipa Atelier Nova SRL`
	}
];
