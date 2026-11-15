"""Adds the Partner Hub texts (and country names) to website/locale/{de,fr,pt,es}.json.

Run once from the repository root: python scripts/i18n_partner_hub.py
Existing translations are never overwritten. Country names come from the
Unicode CLDR data (Babel), which is only needed when running this script.
"""
import json
from pathlib import Path

# English: (German, French, Portuguese, Spanish)
T = {
    "Partner Hub": ("Partner Hub", "Partner Hub", "Partner Hub", "Partner Hub"),
    "Partner Hub: register your company": ("Partner Hub: Unternehmen registrieren", "Partner Hub : inscrire votre entreprise", "Partner Hub: registe a sua empresa", "Partner Hub: registre su empresa"),
    "TradeGate Partner Hub: Find Business Partners in Germany or Abroad | TradeGate Consultants": (
        "TradeGate Partner Hub: Geschäftspartner in Deutschland oder im Ausland finden | TradeGate Consultants",
        "TradeGate Partner Hub : trouver des partenaires commerciaux en Allemagne ou à l’étranger | TradeGate Consultants",
        "TradeGate Partner Hub: encontrar parceiros de negócio na Alemanha ou no estrangeiro | TradeGate Consultants",
        "TradeGate Partner Hub: encontrar socios comerciales en Alemania o en el extranjero | TradeGate Consultants"),
    "Register your company in the TradeGate Partner Hub, our private B2B network. We match companies with business partners in Germany, the EU and abroad and make personal introductions.": (
        "Registrieren Sie Ihr Unternehmen im TradeGate Partner Hub, unserem privaten B2B-Netzwerk. Wir bringen Unternehmen mit Geschäftspartnern in Deutschland, der EU und im Ausland zusammen und stellen persönlich vor.",
        "Inscrivez votre entreprise au TradeGate Partner Hub, notre réseau B2B privé. Nous mettons en relation des entreprises avec des partenaires en Allemagne, dans l’UE et à l’étranger, avec une présentation personnelle.",
        "Registe a sua empresa no TradeGate Partner Hub, a nossa rede B2B privada. Ligamos empresas a parceiros de negócio na Alemanha, na UE e no estrangeiro, com apresentação pessoal.",
        "Registre su empresa en el TradeGate Partner Hub, nuestra red B2B privada. Conectamos empresas con socios comerciales en Alemania, la UE y el extranjero, con presentación personal."),
    "Find business partners in Germany or abroad.": ("Geschäftspartner in Deutschland oder im Ausland finden.", "Trouvez des partenaires commerciaux en Allemagne ou à l’étranger.", "Encontre parceiros de negócio na Alemanha ou no estrangeiro.", "Encuentre socios comerciales en Alemania o en el extranjero."),
    "Register your company in our private B2B network. We compare your profile with other companies, look for the right partner and introduce you personally.": (
        "Registrieren Sie Ihr Unternehmen in unserem privaten B2B-Netzwerk. Wir vergleichen Ihr Profil mit anderen Unternehmen, suchen den passenden Partner und stellen Sie persönlich vor.",
        "Inscrivez votre entreprise dans notre réseau B2B privé. Nous comparons votre profil avec d’autres entreprises, cherchons le bon partenaire et vous présentons personnellement.",
        "Registe a sua empresa na nossa rede B2B privada. Comparamos o seu perfil com outras empresas, procuramos o parceiro certo e apresentamo-lo pessoalmente.",
        "Registre su empresa en nuestra red B2B privada. Comparamos su perfil con otras empresas, buscamos el socio adecuado y le presentamos personalmente."),
    "Register your company": ("Unternehmen registrieren", "Inscrire votre entreprise", "Registe a sua empresa", "Registre su empresa"),
    "Register your company →": ("Unternehmen registrieren →", "Inscrire votre entreprise →", "Registe a sua empresa →", "Registre su empresa →"),
    "Register my company": ("Mein Unternehmen registrieren", "Inscrire mon entreprise", "Registar a minha empresa", "Registrar mi empresa"),
    "How it works": ("So funktioniert es", "Comment ça marche", "Como funciona", "Cómo funciona"),
    "Two directions, one network": ("Zwei Richtungen, ein Netzwerk", "Deux directions, un seul réseau", "Duas direções, uma rede", "Dos direcciones, una red"),
    "International companies": ("Internationale Unternehmen", "Entreprises internationales", "Empresas internacionais", "Empresas internacionales"),
    "looking for distributors, buyers, suppliers or agents in Germany and the EU.": (
        "auf der Suche nach Vertriebspartnern, Abnehmern, Lieferanten oder Handelsvertretern in Deutschland und der EU.",
        "qui cherchent des distributeurs, acheteurs, fournisseurs ou agents en Allemagne et dans l’UE.",
        "que procuram distribuidores, compradores, fornecedores ou agentes na Alemanha e na UE.",
        "que buscan distribuidores, compradores, proveedores o agentes en Alemania y la UE."),
    "German and European companies": ("Deutsche und europäische Unternehmen", "Entreprises allemandes et européennes", "Empresas alemãs e europeias", "Empresas alemanas y europeas"),
    "looking for partners, suppliers and new markets abroad.": (
        "auf der Suche nach Partnern, Lieferanten und neuen Märkten im Ausland.",
        "qui cherchent des partenaires, des fournisseurs et de nouveaux marchés à l’étranger.",
        "que procuram parceiros, fornecedores e novos mercados no estrangeiro.",
        "que buscan socios, proveedores y nuevos mercados en el extranjero."),
    "From profile to introduction": ("Vom Profil zur Vorstellung", "Du profil à la mise en relation", "Do perfil à apresentação", "Del perfil a la presentación"),
    "Register": ("Registrieren", "Inscription", "Registo", "Registro"),
    "Describe your company, what you offer and the partner you are looking for.": (
        "Beschreiben Sie Ihr Unternehmen, Ihr Angebot und den Partner, den Sie suchen.",
        "Décrivez votre entreprise, ce que vous proposez et le partenaire que vous cherchez.",
        "Descreva a sua empresa, o que oferece e o parceiro que procura.",
        "Describa su empresa, lo que ofrece y el socio que busca."),
    "We review": ("Wir prüfen", "Nous vérifions", "Nós verificamos", "Revisamos"),
    "We check every profile before it enters the network, so it stays trustworthy.": (
        "Wir prüfen jedes Profil, bevor es ins Netzwerk aufgenommen wird, damit es vertrauenswürdig bleibt.",
        "Nous vérifions chaque profil avant son entrée dans le réseau, pour qu’il reste fiable.",
        "Verificamos cada perfil antes de entrar na rede, para que ela continue fiável.",
        "Revisamos cada perfil antes de que entre en la red, para que siga siendo fiable."),
    "We match": ("Wir gleichen ab", "Nous rapprochons", "Nós cruzamos", "Buscamos coincidencias"),
    "Our system compares your profile with the network. We check every suggestion ourselves.": (
        "Unser System vergleicht Ihr Profil mit dem Netzwerk. Jeden Vorschlag prüfen wir selbst.",
        "Notre système compare votre profil avec le réseau. Nous vérifions nous-mêmes chaque suggestion.",
        "O nosso sistema compara o seu perfil com a rede. Verificamos pessoalmente cada sugestão.",
        "Nuestro sistema compara su perfil con la red. Revisamos personalmente cada sugerencia."),
    "We introduce": ("Wir stellen vor", "Nous vous présentons", "Nós apresentamos", "Le presentamos"),
    "When both sides agree, we make the introduction and support the first steps.": (
        "Wenn beide Seiten zustimmen, stellen wir den Kontakt her und begleiten die ersten Schritte.",
        "Lorsque les deux parties sont d’accord, nous faisons la mise en relation et accompagnons les premiers pas.",
        "Quando ambas as partes concordam, fazemos a apresentação e apoiamos os primeiros passos.",
        "Cuando ambas partes están de acuerdo, hacemos la presentación y acompañamos los primeros pasos."),
    "Takes about 5 minutes. The clearer your description, the better we can match you.": (
        "Dauert etwa 5 Minuten. Je klarer Ihre Beschreibung, desto besser können wir Sie vermitteln.",
        "Environ 5 minutes. Plus votre description est claire, mieux nous pouvons vous mettre en relation.",
        "Demora cerca de 5 minutos. Quanto mais clara a descrição, melhor o podemos ligar ao parceiro certo.",
        "Lleva unos 5 minutos. Cuanto más clara sea su descripción, mejor podremos encontrarle socio."),
    "1. Your company": ("1. Ihr Unternehmen", "1. Votre entreprise", "1. A sua empresa", "1. Su empresa"),
    "2. Offer and search": ("2. Angebot und Suche", "2. Offre et recherche", "2. Oferta e procura", "2. Oferta y búsqueda"),
    "3. Contact person": ("3. Ansprechperson", "3. Personne de contact", "3. Pessoa de contacto", "3. Persona de contacto"),
    "Company name": ("Name des Unternehmens", "Nom de l’entreprise", "Nome da empresa", "Nombre de la empresa"),
    "Country where you are based": ("Land des Unternehmenssitzes", "Pays où vous êtes établi", "País onde está sediada", "País donde tiene su sede"),
    "City": ("Stadt", "Ville", "Cidade", "Ciudad"),
    "Type of company": ("Art des Unternehmens", "Type d’entreprise", "Tipo de empresa", "Tipo de empresa"),
    "Company size": ("Unternehmensgröße", "Taille de l’entreprise", "Dimensão da empresa", "Tamaño de la empresa"),
    "Sector": ("Branche", "Secteur", "Setor", "Sector"),
    "Main products or services": ("Wichtigste Produkte oder Leistungen", "Principaux produits ou services", "Principais produtos ou serviços", "Principales productos o servicios"),
    "What do you offer a partner?": ("Was bieten Sie einem Partner?", "Qu’offrez-vous à un partenaire ?", "O que oferece a um parceiro?", "¿Qué ofrece a un socio?"),
    "What kind of partner are you looking for?": ("Welchen Partner suchen Sie?", "Quel type de partenaire cherchez-vous ?", "Que tipo de parceiro procura?", "¿Qué tipo de socio busca?"),
    "Partner types you are looking for": ("Gesuchte Partnerarten", "Types de partenaires recherchés", "Tipos de parceiro que procura", "Tipos de socio que busca"),
    "Where are you looking for partners?": ("Wo suchen Sie Partner?", "Où cherchez-vous des partenaires ?", "Onde procura parceiros?", "¿Dónde busca socios?"),
    "Contact person": ("Ansprechperson", "Personne de contact", "Pessoa de contacto", "Persona de contacto"),
    "Role": ("Funktion", "Fonction", "Função", "Cargo"),
    "Full name": ("Vollständiger Name", "Nom complet", "Nome completo", "Nombre completo"),
    "Founder, Export Manager…": ("Gründer, Exportleitung…", "Fondateur, responsable export…", "Fundador, diretor de exportação…", "Fundador, responsable de exportación…"),
    "e.g. roasted coffee, solar inverters, logistics software": ("z. B. Röstkaffee, Solarwechselrichter, Logistiksoftware", "p. ex. café torréfié, onduleurs solaires, logiciel logistique", "p. ex. café torrado, inversores solares, software de logística", "p. ej. café tostado, inversores solares, software logístico"),
    "Capacity, certifications, markets you already serve, what makes you a good partner": (
        "Kapazität, Zertifikate, bereits belieferte Märkte, was Sie zu einem guten Partner macht",
        "Capacité, certifications, marchés déjà servis, ce qui fait de vous un bon partenaire",
        "Capacidade, certificações, mercados que já serve, o que faz de si um bom parceiro",
        "Capacidad, certificaciones, mercados que ya atiende, qué le convierte en un buen socio"),
    "Type of company, products, size, what the partnership should achieve": (
        "Art des Unternehmens, Produkte, Größe, was die Partnerschaft erreichen soll",
        "Type d’entreprise, produits, taille, objectif du partenariat",
        "Tipo de empresa, produtos, dimensão, o que a parceria deve alcançar",
        "Tipo de empresa, productos, tamaño, qué debe lograr la colaboración"),
    "Select country": ("Land auswählen", "Choisir le pays", "Selecione o país", "Seleccione el país"),
    "Select sector": ("Branche auswählen", "Choisir le secteur", "Selecione o setor", "Seleccione el sector"),
    "Select type": ("Art auswählen", "Choisir le type", "Selecione o tipo", "Seleccione el tipo"),
    "Select size": ("Größe auswählen", "Choisir la taille", "Selecione a dimensão", "Seleccione el tamaño"),
    "1–9 employees": ("1–9 Beschäftigte", "1–9 salariés", "1–9 colaboradores", "1–9 empleados"),
    "10–49 employees": ("10–49 Beschäftigte", "10–49 salariés", "10–49 colaboradores", "10–49 empleados"),
    "50–249 employees": ("50–249 Beschäftigte", "50–249 salariés", "50–249 colaboradores", "50–249 empleados"),
    "250+ employees": ("250+ Beschäftigte", "250+ salariés", "250+ colaboradores", "250+ empleados"),
    "Agriculture, food and beverages": ("Landwirtschaft, Lebensmittel und Getränke", "Agriculture, alimentation et boissons", "Agricultura, alimentos e bebidas", "Agricultura, alimentación y bebidas"),
    "Automotive and mobility": ("Automobil und Mobilität", "Automobile et mobilité", "Automóvel e mobilidade", "Automoción y movilidad"),
    "Chemicals and plastics": ("Chemie und Kunststoffe", "Chimie et plastiques", "Química e plásticos", "Química y plásticos"),
    "Construction and building materials": ("Bau und Baustoffe", "Construction et matériaux", "Construção e materiais de construção", "Construcción y materiales"),
    "Consumer goods and retail": ("Konsumgüter und Handel", "Biens de consommation et commerce", "Bens de consumo e retalho", "Bienes de consumo y comercio minorista"),
    "Energy and renewables": ("Energie und Erneuerbare", "Énergie et renouvelables", "Energia e renováveis", "Energía y renovables"),
    "Textiles, fashion and leather": ("Textil, Mode und Leder", "Textile, mode et cuir", "Têxtil, moda e couro", "Textil, moda y cuero"),
    "Healthcare, medical and pharma": ("Gesundheit, Medizin und Pharma", "Santé, médical et pharmacie", "Saúde, medicina e farmacêutica", "Salud, medicina y farmacia"),
    "IT, software and electronics": ("IT, Software und Elektronik", "Informatique, logiciels et électronique", "TI, software e eletrónica", "TI, software y electrónica"),
    "Logistics and transport": ("Logistik und Transport", "Logistique et transport", "Logística e transportes", "Logística y transporte"),
    "Machinery and industrial equipment": ("Maschinen und Industrieausrüstung", "Machines et équipements industriels", "Máquinas e equipamento industrial", "Maquinaria y equipos industriales"),
    "Mining, metals and raw materials": ("Bergbau, Metalle und Rohstoffe", "Mines, métaux et matières premières", "Mineração, metais e matérias-primas", "Minería, metales y materias primas"),
    "Business and professional services": ("Unternehmens- und Fachdienstleistungen", "Services aux entreprises", "Serviços empresariais e profissionais", "Servicios empresariales y profesionales"),
    "Tourism and hospitality": ("Tourismus und Gastgewerbe", "Tourisme et hôtellerie", "Turismo e hotelaria", "Turismo y hostelería"),
    "Wood, furniture and paper": ("Holz, Möbel und Papier", "Bois, meubles et papier", "Madeira, mobiliário e papel", "Madera, muebles y papel"),
    "Other": ("Sonstiges", "Autre", "Outro", "Otro"),
    "Manufacturer / producer": ("Hersteller / Produzent", "Fabricant / producteur", "Fabricante / produtor", "Fabricante / productor"),
    "Exporter / trading company": ("Exporteur / Handelsunternehmen", "Exportateur / société de négoce", "Exportador / empresa comercial", "Exportador / empresa comercializadora"),
    "Importer / distributor / wholesaler": ("Importeur / Vertriebspartner / Großhändler", "Importateur / distributeur / grossiste", "Importador / distribuidor / grossista", "Importador / distribuidor / mayorista"),
    "Retailer / e-commerce": ("Einzelhandel / E-Commerce", "Détaillant / e-commerce", "Retalhista / comércio eletrónico", "Minorista / comercio electrónico"),
    "Service provider": ("Dienstleister", "Prestataire de services", "Prestador de serviços", "Proveedor de servicios"),
    "Investor": ("Investor", "Investisseur", "Investidor", "Inversor"),
    "Importer / distributor": ("Importeur / Vertriebspartner", "Importateur / distributeur", "Importador / distribuidor", "Importador / distribuidor"),
    "Supplier / manufacturer": ("Lieferant / Hersteller", "Fournisseur / fabricant", "Fornecedor / fabricante", "Proveedor / fabricante"),
    "Sales agent / representative": ("Handelsvertreter / Repräsentant", "Agent commercial / représentant", "Agente comercial / representante", "Agente comercial / representante"),
    "Buyer / retailer": ("Abnehmer / Händler", "Acheteur / détaillant", "Comprador / retalhista", "Comprador / minorista"),
    "Joint venture / investor": ("Joint Venture / Investor", "Coentreprise / investisseur", "Joint venture / investidor", "Empresa conjunta / inversor"),
    "Service or technology partner": ("Dienstleistungs- oder Technologiepartner", "Partenaire de services ou technologique", "Parceiro de serviços ou tecnologia", "Socio de servicios o tecnología"),
    "Germany": ("Deutschland", "Allemagne", "Alemanha", "Alemania"),
    "Austria and Switzerland": ("Österreich und Schweiz", "Autriche et Suisse", "Áustria e Suíça", "Austria y Suiza"),
    "Rest of the EU": ("Übrige EU", "Reste de l’UE", "Resto da UE", "Resto de la UE"),
    "Rest of Europe (incl. UK and Türkiye)": ("Übriges Europa (inkl. UK und Türkei)", "Reste de l’Europe (y c. Royaume-Uni et Turquie)", "Resto da Europa (incl. Reino Unido e Turquia)", "Resto de Europa (incl. Reino Unido y Turquía)"),
    "Africa": ("Afrika", "Afrique", "África", "África"),
    "Middle East": ("Naher Osten", "Moyen-Orient", "Médio Oriente", "Oriente Medio"),
    "Asia": ("Asien", "Asie", "Ásia", "Asia"),
    "Americas": ("Amerika", "Amériques", "Américas", "América"),
    "Oceania": ("Ozeanien", "Océanie", "Oceânia", "Oceanía"),
    "Open to any region": ("Offen für alle Regionen", "Ouvert à toutes les régions", "Aberto a qualquer região", "Abierto a cualquier región"),
    "I agree that TradeGate stores this company profile in the TradeGate Partner Hub, compares it with other entries and contacts me about possible partners. Details are never published or passed on without my approval. I can withdraw at any time.": (
        "Ich bin einverstanden, dass TradeGate dieses Unternehmensprofil im TradeGate Partner Hub speichert, mit anderen Einträgen abgleicht und mich zu möglichen Partnern kontaktiert. Angaben werden nie ohne meine Zustimmung veröffentlicht oder weitergegeben. Ich kann jederzeit widerrufen.",
        "J’accepte que TradeGate enregistre ce profil d’entreprise dans le TradeGate Partner Hub, le compare à d’autres profils et me contacte au sujet de partenaires possibles. Les informations ne sont jamais publiées ni transmises sans mon accord. Je peux retirer mon consentement à tout moment.",
        "Concordo que a TradeGate guarde este perfil de empresa no TradeGate Partner Hub, o compare com outros registos e me contacte sobre possíveis parceiros. Os dados nunca são publicados nem partilhados sem a minha autorização. Posso retirar o consentimento a qualquer momento.",
        "Acepto que TradeGate guarde este perfil de empresa en el TradeGate Partner Hub, lo compare con otros registros y me contacte sobre posibles socios. Los datos nunca se publican ni se comparten sin mi aprobación. Puedo retirar mi consentimiento en cualquier momento."),
    "Details in our": ("Details in unserer", "Détails dans notre", "Detalhes na nossa", "Detalles en nuestra"),
    "privacy policy": ("Datenschutzerklärung", "politique de confidentialité", "política de privacidade", "política de privacidad"),
    "We review every profile within 2 working days.": ("Wir prüfen jedes Profil innerhalb von 2 Werktagen.", "Nous examinons chaque profil sous 2 jours ouvrés.", "Analisamos cada perfil no prazo de 2 dias úteis.", "Revisamos cada perfil en un plazo de 2 días laborables."),
    "Our promise": ("Unser Versprechen", "Notre engagement", "O nosso compromisso", "Nuestro compromiso"),
    "Your profile is private: no public listing, no names shared": ("Ihr Profil bleibt privat: keine öffentliche Liste, keine Namen werden weitergegeben", "Votre profil reste privé : aucune publication, aucun nom communiqué", "O seu perfil é privado: sem listagem pública, sem partilha de nomes", "Su perfil es privado: sin listado público ni nombres compartidos"),
    "Every company is checked by us before it joins": ("Jedes Unternehmen wird vor der Aufnahme von uns geprüft", "Chaque entreprise est vérifiée par nous avant son admission", "Cada empresa é verificada por nós antes de entrar", "Revisamos cada empresa antes de que se una"),
    "Introductions only with the agreement of both sides": ("Vorstellungen nur mit Zustimmung beider Seiten", "Mises en relation uniquement avec l’accord des deux parties", "Apresentações apenas com o acordo de ambas as partes", "Presentaciones solo con el acuerdo de ambas partes"),
    "Registering costs nothing": ("Die Registrierung ist kostenlos", "L’inscription est gratuite", "O registo é gratuito", "El registro es gratuito"),
    "Update or delete your profile at any time": ("Profil jederzeit ändern oder löschen", "Modifiez ou supprimez votre profil à tout moment", "Atualize ou elimine o seu perfil a qualquer momento", "Actualice o elimine su perfil en cualquier momento"),
    "Need a partner faster?": ("Brauchen Sie schneller einen Partner?", "Besoin d’un partenaire plus vite ?", "Precisa de um parceiro mais depressa?", "¿Necesita un socio más rápido?"),
    "We also run active partner searches in Germany and the EU, with a shortlist and outreach.": (
        "Wir führen auch aktive Partnersuchen in Deutschland und der EU durch, mit Shortlist und Ansprache.",
        "Nous menons aussi des recherches actives de partenaires en Allemagne et dans l’UE, avec liste restreinte et prise de contact.",
        "Também fazemos pesquisas ativas de parceiros na Alemanha e na UE, com lista curta e contacto direto.",
        "También realizamos búsquedas activas de socios en Alemania y la UE, con lista corta y contacto directo."),
    "Partner search service →": ("Service Partnersuche →", "Service de recherche de partenaires →", "Serviço de pesquisa de parceiros →", "Servicio de búsqueda de socios →"),
    "Questions": ("Fragen", "Questions", "Perguntas", "Preguntas"),
    "Partner Hub FAQ": ("Partner Hub: häufige Fragen", "Partner Hub : questions fréquentes", "Partner Hub: perguntas frequentes", "Partner Hub: preguntas frecuentes"),
    "Who can register?": ("Wer kann sich registrieren?", "Qui peut s’inscrire ?", "Quem se pode registar?", "¿Quién puede registrarse?"),
    "Companies from any country that look for business partners in Germany and the EU, and German or European companies that look for partners abroad.": (
        "Unternehmen aus jedem Land, die Geschäftspartner in Deutschland und der EU suchen, sowie deutsche oder europäische Unternehmen, die Partner im Ausland suchen.",
        "Les entreprises de tout pays qui cherchent des partenaires en Allemagne et dans l’UE, ainsi que les entreprises allemandes ou européennes qui cherchent des partenaires à l’étranger.",
        "Empresas de qualquer país que procuram parceiros na Alemanha e na UE, e empresas alemãs ou europeias que procuram parceiros no estrangeiro.",
        "Empresas de cualquier país que buscan socios en Alemania y la UE, y empresas alemanas o europeas que buscan socios en el extranjero."),
    "Is my company visible to others?": ("Ist mein Unternehmen für andere sichtbar?", "Mon entreprise est-elle visible par d’autres ?", "A minha empresa fica visível para outros?", "¿Mi empresa es visible para otros?"),
    "No. The Partner Hub is private. Only we see the entries. We compare profiles and introduce companies personally, and only with the agreement of both sides.": (
        "Nein. Der Partner Hub ist privat. Nur wir sehen die Einträge. Wir vergleichen Profile und stellen Unternehmen persönlich vor, und nur mit Zustimmung beider Seiten.",
        "Non. Le Partner Hub est privé. Nous seuls voyons les profils. Nous les comparons et présentons les entreprises personnellement, uniquement avec l’accord des deux parties.",
        "Não. O Partner Hub é privado. Só nós vemos os registos. Comparamos perfis e apresentamos as empresas pessoalmente, apenas com o acordo de ambas as partes.",
        "No. El Partner Hub es privado. Solo nosotros vemos los registros. Comparamos perfiles y presentamos a las empresas personalmente, solo con el acuerdo de ambas partes."),
    "What does it cost?": ("Was kostet es?", "Combien cela coûte-t-il ?", "Quanto custa?", "¿Cuánto cuesta?"),
    "Registering costs nothing. If we find a fitting partner, we agree any service fee with you before we make an introduction.": (
        "Die Registrierung ist kostenlos. Finden wir einen passenden Partner, vereinbaren wir ein mögliches Honorar mit Ihnen, bevor wir den Kontakt herstellen.",
        "L’inscription est gratuite. Si nous trouvons un partenaire adapté, nous convenons avec vous d’éventuels honoraires avant toute mise en relation.",
        "O registo é gratuito. Se encontrarmos um parceiro adequado, acordamos consigo qualquer honorário antes de fazer a apresentação.",
        "El registro es gratuito. Si encontramos un socio adecuado, acordamos con usted cualquier honorario antes de hacer la presentación."),
    "What if there is no match in the network yet?": ("Was, wenn es im Netzwerk noch keinen passenden Partner gibt?", "Et s’il n’y a pas encore de partenaire adapté dans le réseau ?", "E se ainda não houver correspondência na rede?", "¿Y si aún no hay coincidencia en la red?"),
    "We look for one. Your profile tells us exactly what to search for, and we can run an active partner search for you.": (
        "Dann suchen wir. Ihr Profil sagt uns genau, wonach wir suchen sollen, und wir können eine aktive Partnersuche für Sie durchführen.",
        "Nous en cherchons un. Votre profil nous indique précisément quoi chercher, et nous pouvons mener une recherche active pour vous.",
        "Procuramos um. O seu perfil diz-nos exatamente o que procurar, e podemos fazer uma pesquisa ativa de parceiros para si.",
        "Lo buscamos. Su perfil nos dice exactamente qué buscar, y podemos realizar una búsqueda activa de socios para usted."),
    "How do I update or delete my profile?": ("Wie ändere oder lösche ich mein Profil?", "Comment modifier ou supprimer mon profil ?", "Como atualizo ou elimino o meu perfil?", "¿Cómo actualizo o elimino mi perfil?"),
    "Write to us at any time and we will update or delete it. We remove profiles that are no longer current.": (
        "Schreiben Sie uns jederzeit, dann ändern oder löschen wir es. Nicht mehr aktuelle Profile entfernen wir.",
        "Écrivez-nous à tout moment et nous le modifierons ou le supprimerons. Nous retirons les profils qui ne sont plus à jour.",
        "Escreva-nos a qualquer momento e atualizamos ou eliminamos o perfil. Removemos perfis que já não estão atuais.",
        "Escríbanos en cualquier momento y lo actualizaremos o eliminaremos. Retiramos los perfiles que ya no están vigentes."),
    "Register your company in our private partner network.": ("Registrieren Sie Ihr Unternehmen in unserem privaten Partnernetzwerk.", "Inscrivez votre entreprise dans notre réseau privé de partenaires.", "Registe a sua empresa na nossa rede privada de parceiros.", "Registre su empresa en nuestra red privada de socios."),
    "For companies looking for partners in Germany, and German companies looking for partners abroad. We compare profiles and introduce you personally.": (
        "Für Unternehmen, die Partner in Deutschland suchen, und deutsche Unternehmen, die Partner im Ausland suchen. Wir vergleichen Profile und stellen Sie persönlich vor.",
        "Pour les entreprises qui cherchent des partenaires en Allemagne, et les entreprises allemandes qui cherchent des partenaires à l’étranger. Nous comparons les profils et vous présentons personnellement.",
        "Para empresas que procuram parceiros na Alemanha e empresas alemãs que procuram parceiros no estrangeiro. Comparamos perfis e apresentamo-lo pessoalmente.",
        "Para empresas que buscan socios en Alemania y empresas alemanas que buscan socios en el extranjero. Comparamos perfiles y le presentamos personalmente."),
    "Thank you. Your company is registered. We review every profile within 2 working days and contact you when we see a fitting partner.": (
        "Vielen Dank. Ihr Unternehmen ist registriert. Wir prüfen jedes Profil innerhalb von 2 Werktagen und melden uns, sobald wir einen passenden Partner sehen.",
        "Merci. Votre entreprise est inscrite. Nous examinons chaque profil sous 2 jours ouvrés et vous contactons dès que nous voyons un partenaire adapté.",
        "Obrigado. A sua empresa está registada. Analisamos cada perfil no prazo de 2 dias úteis e contactamo-lo quando virmos um parceiro adequado.",
        "Gracias. Su empresa está registrada. Revisamos cada perfil en 2 días laborables y le contactamos cuando veamos un socio adecuado."),
    "Thank you. Your company profile has been received.": ("Vielen Dank. Ihr Unternehmensprofil ist eingegangen.", "Merci. Votre profil d’entreprise a bien été reçu.", "Obrigado. O perfil da sua empresa foi recebido.", "Gracias. Hemos recibido el perfil de su empresa."),
    "Please enter your company name.": ("Bitte geben Sie den Namen Ihres Unternehmens ein.", "Veuillez indiquer le nom de votre entreprise.", "Indique o nome da sua empresa.", "Indique el nombre de su empresa."),
    "Please select your country.": ("Bitte wählen Sie Ihr Land aus.", "Veuillez choisir votre pays.", "Selecione o seu país.", "Seleccione su país."),
    "Please select the type of company.": ("Bitte wählen Sie die Art des Unternehmens aus.", "Veuillez choisir le type d’entreprise.", "Selecione o tipo de empresa.", "Seleccione el tipo de empresa."),
    "Please select your sector.": ("Bitte wählen Sie Ihre Branche aus.", "Veuillez choisir votre secteur.", "Selecione o seu setor.", "Seleccione su sector."),
    "Please name your main products or services.": ("Bitte nennen Sie Ihre wichtigsten Produkte oder Leistungen.", "Veuillez indiquer vos principaux produits ou services.", "Indique os seus principais produtos ou serviços.", "Indique sus principales productos o servicios."),
    "Please describe what you offer.": ("Bitte beschreiben Sie Ihr Angebot.", "Veuillez décrire ce que vous proposez.", "Descreva o que oferece.", "Describa lo que ofrece."),
    "Please describe the partner you are looking for.": ("Bitte beschreiben Sie den gesuchten Partner.", "Veuillez décrire le partenaire recherché.", "Descreva o parceiro que procura.", "Describa el socio que busca."),
    "Please choose at least one partner type.": ("Bitte wählen Sie mindestens eine Partnerart.", "Veuillez choisir au moins un type de partenaire.", "Escolha pelo menos um tipo de parceiro.", "Elija al menos un tipo de socio."),
    "Please choose at least one region.": ("Bitte wählen Sie mindestens eine Region.", "Veuillez choisir au moins une région.", "Escolha pelo menos uma região.", "Elija al menos una región."),
    "Please enter a contact person.": ("Bitte geben Sie eine Ansprechperson an.", "Veuillez indiquer une personne de contact.", "Indique uma pessoa de contacto.", "Indique una persona de contacto."),
    "Please add a little more detail (at least 30 characters).": ("Bitte etwas ausführlicher (mindestens 30 Zeichen).", "Merci de donner un peu plus de détails (au moins 30 caractères).", "Acrescente um pouco mais de detalhe (pelo menos 30 caracteres).", "Añada un poco más de detalle (al menos 30 caracteres)."),
    "Please enter a valid website, for example https://www.example.com": ("Bitte geben Sie eine gültige Website an, z. B. https://www.example.com", "Veuillez saisir un site web valide, p. ex. https://www.example.com", "Indique um site válido, por exemplo https://www.example.com", "Indique un sitio web válido, por ejemplo https://www.example.com"),
    "Your consent is needed to add your company to the Partner Hub.": ("Ihre Einwilligung ist nötig, um Ihr Unternehmen in den Partner Hub aufzunehmen.", "Votre consentement est nécessaire pour ajouter votre entreprise au Partner Hub.", "O seu consentimento é necessário para adicionar a empresa ao Partner Hub.", "Necesitamos su consentimiento para añadir su empresa al Partner Hub."),
    "This form session expired. Please refresh and try again.": ("Diese Formularsitzung ist abgelaufen. Bitte laden Sie die Seite neu und versuchen Sie es erneut.", "Cette session de formulaire a expiré. Veuillez actualiser la page et réessayer.", "Esta sessão do formulário expirou. Atualize a página e tente novamente.", "Esta sesión del formulario ha caducado. Actualice la página e inténtelo de nuevo."),
    "Please enter your email address.": ("Bitte geben Sie Ihre E-Mail-Adresse ein.", "Veuillez indiquer votre adresse e-mail.", "Indique o seu endereço de e-mail.", "Indique su dirección de correo electrónico."),
    "Clients worldwide": ("Kunden weltweit", "Clients dans le monde entier", "Clientes em todo o mundo", "Clientes en todo el mundo"),
    "Practical Germany and EU market entry support for international SMEs: strategy, partner search, trade fairs and local presence.": (
        "Praxisnahe Markteintrittsberatung für Deutschland und die EU für internationale KMU: Strategie, Partnersuche, Messen und lokale Präsenz.",
        "Accompagnement concret pour entrer sur le marché allemand et européen, pour les PME internationales : stratégie, recherche de partenaires, salons et présence locale.",
        "Apoio prático à entrada no mercado alemão e europeu para PME internacionais: estratégia, pesquisa de parceiros, feiras e presença local.",
        "Apoyo práctico para entrar en el mercado alemán y europeo para pymes internacionales: estrategia, búsqueda de socios, ferias y presencia local."),
    "We work with companies from any country that want to enter Germany and the EU, and we help German companies find partners abroad.": (
        "Wir arbeiten mit Unternehmen aus allen Ländern, die in Deutschland und der EU Fuß fassen wollen, und helfen deutschen Unternehmen, Partner im Ausland zu finden.",
        "Nous travaillons avec des entreprises de tous pays qui veulent entrer en Allemagne et dans l’UE, et nous aidons les entreprises allemandes à trouver des partenaires à l’étranger.",
        "Trabalhamos com empresas de qualquer país que queiram entrar na Alemanha e na UE, e ajudamos empresas alemãs a encontrar parceiros no estrangeiro.",
        "Trabajamos con empresas de cualquier país que quieran entrar en Alemania y la UE, y ayudamos a empresas alemanas a encontrar socios en el extranjero."),
    "Exporters": ("Exporteure", "Exportateurs", "Exportadores", "Exportadores"),
    "Manufacturers": ("Hersteller", "Fabricants", "Fabricantes", "Fabricantes"),
    "Trade promotion bodies": ("Außenhandelsförderer", "Organismes de promotion du commerce", "Organismos de promoção comercial", "Organismos de promoción comercial"),
    "Tourism boards": ("Tourismusorganisationen", "Offices de tourisme", "Organismos de turismo", "Organismos de turismo"),
    "Start-ups and scale-ups": ("Start-ups und Scale-ups", "Start-ups et scale-ups", "Startups e scale-ups", "Startups y scale-ups"),
    "German companies going abroad": ("Deutsche Unternehmen auf dem Weg ins Ausland", "Entreprises allemandes à l’international", "Empresas alemãs a internacionalizar-se", "Empresas alemanas que salen al exterior"),
    "We support international SMEs, exporters, manufacturers, trade promotion organizations, tourism-related institutions, and growth-oriented businesses looking to test, enter, or strengthen their position in Germany and the wider EU market, from any country.": (
        "Wir unterstützen internationale KMU, Exporteure, Hersteller, Außenhandelsförderer, Tourismusinstitutionen und wachstumsorientierte Unternehmen aus allen Ländern, die ihre Position in Deutschland und der EU testen, aufbauen oder stärken wollen.",
        "Nous accompagnons des PME internationales, exportateurs, fabricants, organismes de promotion du commerce, institutions touristiques et entreprises en croissance de tous pays qui veulent tester, conquérir ou renforcer leur position en Allemagne et dans l’UE.",
        "Apoiamos PME internacionais, exportadores, fabricantes, organismos de promoção comercial, instituições de turismo e empresas em crescimento de qualquer país que queiram testar, entrar ou reforçar a sua posição na Alemanha e na UE.",
        "Apoyamos a pymes internacionales, exportadores, fabricantes, organismos de promoción comercial, instituciones turísticas y empresas en crecimiento de cualquier país que quieran probar, entrar o reforzar su posición en Alemania y la UE."),
    "Looking for business partners for your own company?": ("Sie suchen Geschäftspartner für Ihr eigenes Unternehmen?", "Vous cherchez des partenaires pour votre propre entreprise ?", "Procura parceiros de negócio para a sua própria empresa?", "¿Busca socios comerciales para su propia empresa?"),
    "Register it in the TradeGate Partner Hub →": ("Registrieren Sie es im TradeGate Partner Hub →", "Inscrivez-la au TradeGate Partner Hub →", "Registe-a no TradeGate Partner Hub →", "Regístrela en el TradeGate Partner Hub →"),
    "Consultant or agent?": ("Berater oder Handelsvertreter?", "Consultant ou agent ?", "Consultor ou agente?", "¿Consultor o agente?"),
    "The Partner Hub is for companies looking for business partners. If you want to work with TradeGate on projects, introduce yourself here instead.": (
        "Der Partner Hub ist für Unternehmen, die Geschäftspartner suchen. Wenn Sie mit TradeGate an Projekten arbeiten möchten, stellen Sie sich bitte hier vor.",
        "Le Partner Hub s’adresse aux entreprises qui cherchent des partenaires commerciaux. Si vous souhaitez travailler avec TradeGate sur des projets, présentez-vous plutôt ici.",
        "O Partner Hub destina-se a empresas que procuram parceiros de negócio. Se quer trabalhar com a TradeGate em projetos, apresente-se antes aqui.",
        "El Partner Hub es para empresas que buscan socios comerciales. Si quiere trabajar con TradeGate en proyectos, preséntese mejor aquí."),
    "Partner with us →": ("Partner werden →", "Devenir partenaire →", "Seja nosso parceiro →", "Colabore con nosotros →"),
    "TradeGate Partner Hub:": ("TradeGate Partner Hub:", "TradeGate Partner Hub :", "TradeGate Partner Hub:", "TradeGate Partner Hub:"),
    "register your company in our private B2B network and we introduce you when a fitting partner is there.": (
        "Registrieren Sie Ihr Unternehmen in unserem privaten B2B-Netzwerk, und wir stellen Sie vor, sobald ein passender Partner da ist.",
        "inscrivez votre entreprise dans notre réseau B2B privé et nous vous présentons dès qu’un partenaire adapté s’y trouve.",
        "registe a sua empresa na nossa rede B2B privada e apresentamo-lo quando houver um parceiro adequado.",
        "registre su empresa en nuestra red B2B privada y le presentamos cuando haya un socio adecuado."),
    "Business email": ("Geschäftliche E-Mail", "E-mail professionnel", "E-mail profissional", "Correo electrónico profesional"),
    "Please enter a valid email address.": ("Bitte geben Sie eine gültige E-Mail-Adresse ein.", "Veuillez saisir une adresse e-mail valide.", "Indique um endereço de e-mail válido.", "Indique una dirección de correo electrónico válida."),
}

ROOT = Path(__file__).resolve().parent.parent
LOCALES = ["de", "fr", "pt", "es"]


def country_names():
    """English country name -> {lang: localised name}, from CLDR via Babel."""
    from babel import Locale
    import sys
    sys.path.insert(0, str(ROOT))
    from website.partner_pool import REGION_OF_COUNTRY

    en = Locale("en").territories
    by_name = {v: k for k, v in en.items() if len(k) == 2}
    alias = {"Czechia": "CZ", "Türkiye": "TR", "Congo (Brazzaville)": "CG", "Congo (DRC)": "CD", "Côte d'Ivoire": "CI",
             "Hong Kong": "HK", "Palestine": "PS", "Myanmar": "MM", "North Macedonia": "MK", "Eswatini": "SZ",
             "Cabo Verde": "CV", "Kosovo": "XK", "São Tomé and Príncipe": "ST", "Timor-Leste": "TL", "United States": "US",
             "United Kingdom": "GB", "South Korea": "KR", "Laos": "LA", "Vietnam": "VN", "Bosnia and Herzegovina": "BA",
             "Trinidad and Tobago": "TT", "Saudi Arabia": "SA", "Taiwan": "TW", "Macau": "MO"}
    out, missing = {}, []
    for name in REGION_OF_COUNTRY:
        code = alias.get(name) or by_name.get(name)
        if not code:
            missing.append(name)
            continue
        out[name] = {lang: Locale(lang).territories.get(code, name) for lang in LOCALES}
    if missing:
        print("No CLDR code for:", missing)
    return out


FAQ_OLD = ("International SMEs, exporters, manufacturers, tourism boards, and startups testing EU demand — especially teams that want EU access without EU overhead (office, staff, travel). "
           "Clients from Nigeria, South Africa, UAE, Saudi Arabia, India, Morocco, and Turkey are a particularly strong fit.")
FAQ_NEW = "International SMEs, exporters, manufacturers, tourism boards, and startups testing EU demand — especially teams that want EU access without EU overhead (office, staff, travel)."


def main():
    countries = country_names()
    for i, lang in enumerate(LOCALES):
        path = ROOT / "website" / "locale" / f"{lang}.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        added = 0
        for en, tr in T.items():
            key = " ".join(en.split())
            if key not in data:
                data[key] = tr[i]
                added += 1
        if FAQ_NEW not in data and FAQ_OLD in data:
            old = data[FAQ_OLD]
            data[FAQ_NEW] = old[: old.rfind(".", 0, len(old) - 1) + 1]
            added += 1
        for en, names in countries.items():
            if en not in data:
                data[en] = names[lang]
                added += 1
        path.write_text(json.dumps(data, ensure_ascii=False, indent=0) + "\n", encoding="utf-8")
        print(lang, "added", added)


if __name__ == "__main__":
    main()
