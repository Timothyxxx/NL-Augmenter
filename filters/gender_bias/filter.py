from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType

class GenderBiasFilter(SentenceOperation):
    tasks = [TaskType.TEXT_TO_TEXT_GENERATION]
    languages = ["en", "fr", "pl"]

    def __init__(self, language, feminine_input=[], masculine_input=[]):
        super().__init__()
        self.language = language
        self.feminine_input = feminine_input
        self.masculine_input = masculine_input  

    @staticmethod
    def flag_sentences(sentences, language, feminine_input=[], masculine_input=[]):
        """
        flag sentences as belonging to the feminine, masculine or neutral groups
        :param sentences: sentences array
        :param language: the string key representing the supported langage
        :return: array of objects, each containing the analyzed sentence along with three flags
        """
        flagged_sentences = []
                
        # Define the words, that represent feminine and masculine groups in both languages
        if language == "en":
            feminine_relation = ["woman", "auntie", "niece", "girl", "daughter", "girlfriend", 
                                 "mistress", "sister", "bride", "wife", "mother", "mum", "mom", "mommy", 
                                 "grandmother", "granny"]
            feminine_relation_plural = ["women", "aunties", "nieces", "girls", "daughters", "girlfriends",
                                 "mistresses", "sisters", "brides", "wives", "mothers", "mums", "moms", "mommies", 
                                 "grandmothers", "grannies"]
            feminine_jobs = ["actress", "heroine", "superwoman",
                             "hostess", "waitress", "stewardess",
                             "landlady", "proprietress", "businesswoman",
                             "firewoman", "policewoman"]
            feminine_jobs_plural = ["actresses", "heroines", "superwomen",
                             "hostesses", "waitresses", "stewardesses",
                             "landladies", "proprietresses", "businesswomen",
                             "firewomen", "policewomen"]
            masculine_jobs = ["actor", "hero", "superman",
                              "waiter", "businesswoman",
                              "landlord", "proprietor", "businessman", 
                              "fireman", "policeman"]
            masculine_jobs_plural = ["actors", "heros", "supermen",
                              "waiters", "businesswomen",
                              "landlords", "proprietors", "businessmen", 
                              "firemen", "policemen"]
            masculine_relation = ["man", "uncle", "nephew","boy", "boyfriend", "master", "brother",
                                  "groom", "bridegroom", "husband", "father", "dad", "daddy", "grandfather"]
            masculine_relation_plural = ["men", "uncles", "nephews", "boys", "boyfriends", "masters", "brothers",
                                  "grooms", "bridegrooms", "husbands", "fathers", "dads", "daddies", "grandfathers"]
            feminine_titles = ["mrs", "ms", "miss", "mademoiselle", "fräulein", "madam", "lady", "gentlewoman", 
                               "baronesse", "countess", "viscountess", "marquise", "duchess", "princess", "emperess", "queen", 
                               "dame", "primadonna", "diva", "goodwife", "guidwife"]
            masculine_titles = ["mr", "mister", "sir", "lord", "gentleman", 
                                "baron", "count", "viscount", "marquess", "duke", "prince", "emperor", "king", "goodman"]

            feminine = ["she", "her", "hers"] + feminine_relation + feminine_relation_plural + feminine_titles + feminine_jobs + feminine_jobs_plural
            masculine = ["he", "him", "his"] + masculine_relation + masculine_relation_plural + masculine_titles + masculine_jobs + masculine_jobs_plural

        elif language == "fr":
            feminine_relation = ["femme", "meuf", "nana", "tante", "fille", "fillette", "gamine", "gonzesse", 
                                 "amie", "pote", "compagne", "maîtresse", "amante", "soeur ", "épouse", "mariée", 
                                 "mère", "maman", "daronne", "nièce", "tante", "grand-mère", "mamie"]
            feminine_relation_plural = ["femmes", "meufs", "nanas", "tantes", "filles", "fillettes", "gamines", "gonzesses", 
                                 "amies", "potes", "compagnes", "maîtresses", "amantes", "soeurs", "épouses", "mariées", 
                                 "mères", "mamans", "daronnes", "nièces", "tantes", "grand-mères", "mamies"]
            feminine_jobs = ["actrice", "comédienne", "héroïne", "amatrice", 
                             "réalisatrice", "productrice", "opératrice",
                             "danseuse", "chanteuse", "musicienne", "animatrice",
                             "étudiante", "enseignante", "chercheuse", "innovatrice",
                             "proprietrice", "directrice", "dirigeante", "conductrice",
                             "programmeuse", "informaticienne",  "ingénieure",
                             "technicienne", "aiguilleuse", "moniale", "nonne",
                             "hôtesse", "serveuse", "servante", "cuisinière", "boulangère",
                             "policière", "gardienne", "infermière", "pharmacienne",                             
                             "acheteuse", "vendeuse", "éleveuse", "agricultrice"]
            feminine_jobs_plural = ["actrices", "comédiennes", "héroïnes", "amatrices", 
                             "réalisatrices", "productrices", "opératrices",
                             "danseuses", "chanteuses", "musiciennes", "animatrices",
                             "étudiantes", "enseignantes", "chercheuses", "innovatrices",
                             "proprietrices", "directrices", "dirigeantes", "conductrices",
                             "programmeuses", "informaticiennes",  "ingénieures",
                             "techniciennes", "aiguilleuses", "moniales", "nonnes",
                             "hôtesses", "serveuses", "servantes", "cuisinières", "boulangères",
                             "policières", "gardiennes", "infermières", "pharmaciennes",                             
                             "acheteuses", "vendeuses", "éleveuses", "agricultrices"]
            masculine_jobs = ["acteur", "comédien", "héros", "amateur", 
                              "réalisateur", "producteur", "opérateur",
                              "danseur", "chanteur", "musicien", "animateur",
                              "étudiant", "enseignant", "chercheur", "innovateur",                            
                              "propriétaire", "directeur", "dirigeant", "conducteur",
                              "programmeur", "informaticien", " ingénieur",
                              "techicien", "aiguilleur", "moine", "prêtre",
                              "steward", "serveur", "servant", "cuisinier", "boulanger",
                              "policier", "gardien", "infermier", "pharmacien",                              
                              "acheteur", "vendeur", "éleveur", "agriculteur"]
            masculine_jobs_plural = ["acteurs", "comédiens", "héros", "amateurs", 
                              "réalisateurs", "producteurs", "opérateurs",
                              "danseurs", "chanteurs", "musiciens", "animateurs",
                              "étudiants", "enseignants", "chercheurs", "innovateurs",                            
                              "propriétaires", "directeurs", "dirigeants", "conducteurs",
                              "programmeurs", "informaticiens", " ingénieurs",
                              "techiciens", "aiguilleurs", "moines", "prêtres",
                              "stewards", "serveurs", "servants", "cuisiniers", "boulangers",
                              "policiers", "gardiens", "infermiers", "pharmaciens",                              
                              "acheteurs", "vendeurs", "éleveurs", "agriculteurs"]
            masculine_relation = ["homme", "mec", "oncle", "neveu", "garçon", "fils", "gars", "gamin", 
                                  "ami", "pot", "maître", "frère", "amant", "époux", "mari", "marié" 
                                  "père", "papa", "daron", "grand-père", "papie"]
            masculine_relation_plural = ["hommes", "mecs", "oncles", "neveux", "garçons", "fils", "gars", "gamins", 
                                  "amis", "pots", "maîtres", "frères", "amants", "époux", "maris", "mariés" 
                                  "pères", "papas", "darons", "grand-pères", "papies"]
            feminine_titles = ["m", "mlle", "madame", "mademoiselle", "baronesse", "comtesse", "marquise", "duchesse", "princesse", "emperesse", "reine", "dame"]
            masculine_titles = ["mr", "monsieur", "monseigneur", "baron", "compte", "marquis", "duc", "prince", "dauphin" "empereur", "roi"]

            feminine = ["elle", "madame", "sienne"] + feminine_relation + feminine_relation_plural + feminine_titles + feminine_jobs + feminine_jobs_plural
            masculine = ["il", "monsieur", "sien"] + masculine_relation + masculine_relation_plural + masculine_titles + masculine_jobs + masculine_jobs_plural

        elif language == "pl":
            feminine_relation = ["kobieta", "kobietka", "baba", "dziewczynka", "dziewczyna", "laska", "nastolatka",
                                 "ciocia", "ciotka", "siostrzenica", "przyjaciółka", "partnerka", "kochanka", "dziewka",
                                 "siostra", "panna", "panienka", "dziewica", "żona", "matka", "mama", "mamusia", "babcia", "wnuczka"]
            feminine_relation_plural = ["kobiety", "kobiet", "kobiecie", "kobietom", "kobietę", "kobietą", "kobietami", "kobietach", "kobieto",
                                        "kobietki", "kobietek", "kobietce", "kobietkom", "kobietkę", "kobietką", "kobietkami", "kobietkach", "kobietko",
                                        "baby", "bab", "babie", "babom", "babę", "babą", "babami", "babach", "babo",
                                        "dziewczynki", "dziewczynek", "dziewczynce", "dziewczynkom", "dziewczynkę", "dziewczynką", "dziewczynkami", "dziewczynce", "dziewczynkach", "dziewczynko",
                                        "dziewczyny", "dziewczyn", "dziewczynie", "dziewczynom", "dziewczynę", "dziewczyną", "dziewczynami", "dziewczynach", "dziewczyno",
                                        "laski", "lasek", "lasce", "laskom", "laskę", "laską", "laskami", "laskach", "lasko",
                                        "nastolatki", "nastolatek", "nastolatce", "nastolatkom", "nastolatkę", "nastolatką", "nastolatkami", "nastolatkach", "nastolatko",
                                        "ciocie", "cioci", "cioć", "ciociom", "ciocię", "ciocie", "ciocią", "ciociami", "ciociach", "ciociu",
                                        "siostrzenice", "siostrzenicy", "siostrzenic", "siostrzenicom", "siostrzenicę", "siostrzenice", "siostrzenicą", "siostrzenicami", "siostrzenicach", "siostrzenico",	 
                                        "przyjaciółki", "przyjaciółki", "przyjaciółek", "przyjaciółce", "przyjaciółkom", "przyjaciółkę", "przyjaciółki", "przyjaciółką", "przyjaciółkami", "przyjaciółkach", "przyjaciółko",
                                        "partnerki", "partnerek", "partnerce", "partnerkom", "partnerkę", "partnerką", "partnerkami", "partnerkach", "partnerko",
                                        "kochanki", "kochanek", "kochance", "kochankom", "kochankę", "kochanką", "kochankami", "kochankach", "kochanko",
                                        "dziewki", "dziewek", "dziewce", "dziewkom", "dziewkę", "dziewką", "dziewkami", "dziewkach", "dziewko",
                                        "siostry", "sióstr", "siostrze", "siostrom", "siostrę", "siostrą", "siostrami", "siostrach", "siostro", 
                                        "panny", "panien", "pannie", "pannom", "pannę", "panną", "pannami", "pannach", "panno",
                                        "panienki", "panienek", "panience", "panienkom", "panienkę", "panienki", "panienką", "panienkami", "panienkach", "panienko", 
                                        "dziewice", "dziewicy", "dziewic", "dziewicy", "dziewicom", "dziewicę", "dziewicą", "dziewicami", "dziewicach", "dziewico", 
                                        "żony", "żon", "żonie", "żonom", "żonę", "żoną", "żonami", "żonach", "żono", 
                                        "córki", "córek", "córce", "córkom", "córkę", "córką", "córkami", "córce", "córkach", "córko", 
                                        "córeczki", "córeczek", "córeczce", "córeczkom", "córeczkę", "córeczki", "córeczką", "córeczkami", "córeczkach", "córeczko", 
                                        "matki", "matek", "matce", "matkom", "matkę", "matką", "matkami", "matkach", "matko",
                                        "mamy", "mam", "mamie", "mamom", "mamę", "mamą", "mamami", "mamach", "mamo",
                                        "mamusie", "mamusi", "mamuś", "mamusiom", "mamusię", "mamusią", "mamusiami", "mamusiach", "mamusiu",
                                        "babcie", "babci", "babć", "babci", "babciom", "babcię", "babcią", "babciami", "babciach", "babciu",
                                        "wnuczki", "wnuczek", "wnuczce", "wnuczkom", "wnuczkę", "wnuczką", "wnuczkami", "wnuczkach", "wnuczko", "wnuczki"]
            feminine_jobs = ["aktorka", "bohaterka", "amatorka", "reżyserka", "producentka", "operatorka",
                            "tancerka", "piosenkarka", "studentka", "nauczycielka", "innowatorka",
                            "właścicielka", "dyrektorka", "kierowniczka", "programistka", "informatyczka", "szwaczka", 
                            "zakonnica", "gospodyni", "kelnerka", "pielęgniarka", "doktorka", "kupująca", "sprzedawczyni"]
            feminine_jobs_plural = ["aktorki", "aktorek", "aktorce", "aktorkom", "aktorkę", "aktorki", "aktorką", "aktorkami", "aktorkach", "aktorko",
                                "bohaterki", "bohaterek", "bohaterce", "bohaterkom", "bohaterkę", "bohaterki", "bohaterką", "bohaterkami", "bohaterkach", "bohaterko", 
                                "amatorki", "amatorek", "amatorce", "amatorkom", "amatorkę", "amatorki", "amatorką", "amatorkami", "amatorkach", "amatorko",
                                "reżyserki", "reżyserki", "reżyserek", "reżyserce", "reżyserkom", "reżyserkę", "reżyserki", "reżyserką", "reżyserkach", "reżyserko",
                                "producentki", "producentek", "producentce", "producentkom", "producentkę", "producentką", "producentkami", "producentkach", "producentko",
                                "operatorki", "operatorek", "operatorce", "operatorkom", "operatorkę", "operatorki", "operatorką", "operatorkami", "operatorkach", "operatorko",
                                "tancerki", "tancerek", "tancerce", "tancerkom", "tancerkę", "tancerki", "tancerką", "tancerkami", "tancerkach", "tancerko",
                                "piosenkarki", "piosenkarek", "piosenkarce", "piosenkarkom", "piosenkarkę", "piosenkarką", "piosenkarkami", "piosenkarkach", "piosenkarko",
                                "studentki", "studentek", "studentce", "studentkom", "studentkę", "studentką", "studentkami", "studentkach", "studentko",
                                "nauczycielki", "nauczycielek", "nauczycielce", "nauczycielkom", "nauczycielkę", "nauczycielką", "nauczycielkami", "nauczycielkach", "nauczycielko",
                                "właścicielki", "właścicielek", "właścicielce", "właścicielkom", "właścicielkę", "właścicielką", "właścicielkami", "właścicielkach", "właścicielko",
                                "dyrektorki", "dyrektorek", "dyrektorce", "dyrektorkom", "dyrektorkę", "dyrektorką", "dyrektorkami", "dyrektorkach", "dyrektorko",
                                "kierowniczki", "kierowniczek", "kierowniczce", "kierowniczkom", "kierowniczkę", "kierowniczką", "kierowniczkami", "kierowniczkach", "kierowniczko",
                                "programistki", "programistek", "programistce", "programistkom", "programistkę", "programistką", "programistkami", "programistkach", "programistko",
                                "informatyczki", "informatyczek", "informatyczce", "informatyczkom", "informatyczkę", "informatyczką", "informatyczkami", "informatyczkach", "informatyczko", 
                                "szwaczki", "szwaczek", "szwaczce", "szwaczkom", "szwaczkę", "szwaczką", "szwaczkami", "szwaczkach", "szwaczko",
                                "zakonnicy", "zakonnic", "zakonnicy", "zakonnicom", "zakonnicę", "zakonnice", "zakonnicą", "zakonnicami", "zakonnicach", "zakonnico",
                                "gospodynie", "gospodyni", "gospodyń", "gospodyniom", "gospodynię", "gospodynią", "gospodyniami", "gospodyniach", "gospodyni",
                                "kelnerki", "kelnerek", "kelnerce", "kelnerkom", "kelnerkę", "kelnerką", "kelnerkami", "kelnerkach", "kelnerko",
                                "pielęgniarki", "pielęgniarek", "pielęgniarce", "pielęgniarkom", "pielęgniarkę", "pielęgniarką", "pielęgniarkami", "pielęgniarkach", "pielęgniarko",
                                "doktorki", "doktorek", "doktorce", "doktorkom", "doktorkę", "doktorki", "doktorką", "doktorkami", "doktorkach", "doktorko", 
                                "kupujące", "kupującej", "kupujących", "kupującą", "kupującymi",
                                "sprzedawczyni", "sprzedawczyń", "sprzedawczyniom", "sprzedawczynię", "sprzedawczynie", "sprzedawczynią", "sprzedawczyniami", "sprzedawczyniach"]
            masculine_jobs = ["aktor", "komik", "bohater", "amator", "reżyser", "producent", "operator",
                            "tancerz", "piosenkarz", "animator", "student", "nauczyciel", "innowator",
                            "właściciel", "dyrektor", "kierownik", "programista", "informatyk", "szewc",
                            "technik", "mnich", "ksiądz", "kelner", "pielęgniarz", "doktor", "kupujący", "sprzedawca"]
            masculine_jobs_plural = ["aktorzy", "aktory", "aktora", "aktorów", "aktorowi", "aktorom", "aktorem", "aktorami", "aktorze", "aktorach",
                                "komicy", "komiki", "komika", "komików", "komikowi", "komikom", "komikiem", "komikami", "komiku", "komikach", "komiku",
                                "bohaterowie", "bohaterzy", "bohatery", "bohatera", "bohaterów", "bohaterowi", "bohaterom", "bohaterem", "bohaterami", "bohaterze", "bohaterach",
                                "amatorzy", "amatorowie", "amatory", "amatora", "amatorów", "amatorowi", "amatorom", "amatorem", "amatorami", "amatorze", "amatorach", 
                                "reżyserzy", "reżyserowie", "reżysery", "reżysera", "reżyserów", "reżyserowi", "reżyserom", "reżyserem", "reżyserami", "reżyserze", "reżyserach", "reżyserze",
                                "producenci", "producenty", "producenta", "producentów", "producentowi", "producentom", "producentem", "producentami", "producencie", "producentach", "producencie",
                                "operatory", "operatora", "operatorów", "operatorowi", "operatorom", "operatorem", "operatorami", "operatorze", "operatorach",
                                "tancerze", "tancerza", "tancerzy", "tancerzowi", "tancerzom", "tancerzem", "tancerzami", "tancerzu", "tancerzach",
                                "piosenkarze", "piosenkarza", "piosenkarzy", "piosenkarzowi", "piosenkarzom", "piosenkarzem", "piosenkarzami", "piosenkarzu", "piosenkarzach", 
                                "animatorzy", "animatory", "animatora", "animatorów", "animatorowi", "animatorom", "animatorem", "animatorami", "animatorze", "animatorach",
                                "studenci", "studenty", "studenta", "studentów", "studentowi", "studentom", "studentem", "studentami", "studencie", "studentach",
                                "nauczyciele", "nauczyciela", "nauczycieli", "nauczycielowi", "nauczycielom", "nauczycielem", "nauczycielami", "nauczycielu", "nauczycielach", 
                                "właściciele", "właściciela", "właścicieli", "właścicielowi", "właścicielom", "właścicielem", "właścicielami", "właścicielu", "właścicielach",
                                "dyrektorzy", "dyrektorowie", "dyrektory", "dyrektora", "dyrektorów", "dyrektorowi", "dyrektorom", "dyrektorem", "dyrektorami", "dyrektorze", "dyrektorach", 
                                "kierowniki", "kierownika", "kierowników", "kierownikowi", "kierownikom", "kierownikiem", "kierownikami", "kierowniku", "kierownikach",
                                "programiści", "programisty", "programistów", "programiście", "programistom", "programistę", "programistą", "programistami", "programistach", "programisto",
                                "informatycy", "informatyki", "informatyka", "informatyków", "informatykowi", "informatykom", "informatykiem", "informatykami", "informatyku", "informatykach", 
                                "szewcy", "szewce", "szewca", "szewców", "szewcowi", "szewcom", "szewcem", "szewcami", "szewcu", "szewcach", "szewcu", "szewcze",
                                "technicy", "techniki", "technika", "techników", "technikowi", "technikom", "technikiem", "technikami", "techniku", "technikach",
                                "mnichy", "mnicha", "mnichów", "mnichowi", "mnichom", "mnich", "mnichy", "mnichem", "mnichami", "mnichu", "mnichach",
                                "księża", "księdza", "księży", "księdzu", "księżom", "księdza", "księdzem", "księżmi", "księdzu", "księżach", "księże",
                                "kelnerzy", "kelnery", "kelnera", "kelnerów", "kelnerowi", "kelnerom", "kelnerem", "kelnerami", "kelnerze", "kelnerach", "kelnerze",
                                "pielęgniarze", "pielęgniarza", "pielęgniarzy", "pielęgniarzowi", "pielęgniarzom", "pielęgniarzem", "pielęgniarzami", "pielęgniarzu", "pielęgniarzach", "pielęgniarzu",
                                "doktorzy", "doktory", "doktora", "doktorów", "doktorowi", "doktorom", "doktorem", "doktorami", "doktorze", "doktorach", "doktorze",
                                "kupujący", "kupujące", "kupującego", "kupujących", "kupującemu", "kupującym", "kupującego", "kupujących", "kupującym", "kupującymi", "kupujących", "kupujący",
                                "sprzedawcy", "sprzedawce", "sprzedawcy", "sprzedawców", "sprzedawcy", "sprzedawcom", "sprzedawcę", "sprzedawców", "sprzedawcą", "sprzedawcami", "sprzedawcach", "sprzedawco"]
                             
            masculine_relation = ["mężczyzna", "facet", "chłopak", "chłopiec", "nastolatek", 
                                  "wujek", "bratanek", "przyjaciel", "kumpel", "brat", "kochanek", "mąż", 
                                  "ojciec", "tata", "tatuś", "syn", "synek", "dziadek", "wnuk"]
            masculine_relation_plural = ["mężczyźni", "mężczyzny", "mężczyzn", "mężczyźnie", "mężczyznom", "mężczyznę", "mężczyzną", "mężczyznami", "mężczyznach", "mężczyzno",
                                        "faceci", "facety", "faceta", "facetów", "facetowi", "facetom", "facetów", "facetem" "facetami", "facetach", "facecie",
                                        "chłopacy", "chłopaki", "chłopaka", "chłopaków", "chłopakowi", "chłopakom", "chłopaków", "chłopakiem", "chłopakami", "chłopakach", "chłopaku",
                                        "chłopcy", "chłopca", "chłopców", "chłopcu", "chłopcom", "chłopców", "chłopcem", "chłopcami", "chłopcach", "chłopcze",
                                        "nastolatkowie", "nastolatki", "nastolatka", "nastolatków", "nastolatkowi", "nastolatkom", "nastolatków", "nastolatkiem", "nastolatkami", "nastolatkach", "nastolatku"
                                        "wujkowie", "wujki", "wujka", "wujków", "wujkowi", "wujkom", "wujkiem", "wujkami", "wujkach", "wujku",
                                        "bratankowie", "bratanki", "bratanka", "bratanków", "bratankowi", "bratankom", "bratankiem", "bratankami", "bratankach", "bratanku",
                                        "przyjaciele", "przyjaciela", "przyjaciół", "przyjacielowi", "przyjaciołom", "przyjacielem" "przyjaciółmi", "przyjaciołach", "przyjacielu",
                                        "kumple", "kumpla", "kumpli", "kumplów", "kumplowi", "kumplom", "kumplów", "kumplem", "kumplami", "kumplach", "kumplu",
                                        "bracia", "braty", "brata", "braci", "bratu", "braciom", "bratem" "braćmi", "bracie", "braciach", "bracie",
                                        "kochankowie", "kochanki", "kochanka", "kochanków", "kochankowi", "kochankom", "kochankiem", "kochankami", "kochankach", "kochanku",
                                        "mężowie", "męże", "męża", "mężów", "mężowi", "mężów", "mężem" "mężami", "mężach", "mężu",
                                        "ojcowie", "ojca", "ojców", "ojcu", "ojcom", "ojcem" "ojcami", "ojcu", "ojcach", "ojcze",
                                        "tatowie", "taty", "tatów", "tacie", "tatom", "tatę", "tatą", "tatami", "tatach", "tato",
                                        "tatusiowie", "tatusie", "tatusia", "tatusiów", "tatusiowi", "tatusiom", "tatusiem", "tatusiami", "tatusiach", "tatusiu",
                                        "synowie", "syny", "syna", "synów", "synowi", "synom", "syna", "synów", "synem", "synami", "synach", "synu",
                                        "synkowie", "synki", "synka", "synków", "synkowi", "synkom", "synkiem", "synkami", "synkach", "synku",
                                        "dziadki", "dziadka", "dziadków", "dziadkowi", "dziadkom", "dziadki", "dziadkiem", "dziadkami", "dziadkach", "dziadku",
                                        "wnukowie", "wnuki", "wnuka", "wnuków", "wnukowi", "wnukom", "wnukiem" "wnukami", "wnukach", "wnuku"]
            feminine_titles = ["pani", "hrabina", "markiza", "księżna", "księżniczka", "cesarna", "królowa"]
            masculine_titles = ["pan", "hrabia", "markiz", "książę", "cesarz", "król"]

            feminine = ["ona", "jej"] + feminine_relation + feminine_relation_plural + feminine_titles + feminine_jobs + feminine_jobs_plural
            masculine = ["on", "jego"] + masculine_relation + masculine_relation_plural + masculine_titles + masculine_jobs + masculine_jobs_plural

        else:
            raise NameError('The specified language is not supported or misformatted. Try "en" or "fr" as language arguments to the filter() method.')

        assert len(sentences) > 0, "You must provide at least one sentence for the analysis. Check the content of your sentences array you pass to the filter() method."

        for sentence in sentences:

            # Initialize the variables
            feminine_flag = False
            masculine_flag = False
            union_flag = False
            neutral_flag = False
            intersection_feminine = set()
            intersection_masculine = set()
            fem = feminine + feminine_input
            
            # Lowercase and split the words in the sentence to find the intersection with the feminine array of keywords
            intersection_feminine = set(sentence.lower().split()).intersection(
                    set(feminine + feminine_input)
                )
            
            # Lowercase and split the words in the sentence to find the intersection with the masculine array of keywords
            intersection_masculine = set(sentence.lower().split()).intersection(
                    set(masculine + masculine_input))
                       
            # If the intersection occured, the intersection_feminine and intersection_masculine variables will contain at least one common keyword
            # use this intersection information to get the value for the corresponding flags
            feminine_flag = len(intersection_feminine) > 0
            masculine_flag = len(intersection_masculine) > 0

            # In case the sentence contains the keywords from feminine and masculine arrays, set a union_flag value
            union_flag = (
                len(intersection_feminine) > 0
                and len(intersection_masculine) > 0
            )

            # If the sentence didn't contain the keywords neither from feminine, nor from masculine arrays, set a neutral_flag value
            neutral_flag = (
                len(intersection_feminine) == 0
                and len(intersection_masculine) == 0
            )

            # Use the union_flag value to set the neutral_flag value, setting to False the feminine and masculine flags
            if union_flag is True:
                feminine_flag = False
                masculine_flag = False
                neutral_flag = True

            # Create the sentence object with the retrieved flag values
            sentence_object = {
                "sentence": sentence,
                "feminine_flag": feminine_flag,
                "masculine_flag": masculine_flag,
                "neutral_flag": neutral_flag,
            }

            # Append the object to the array we return
            flagged_sentences.append(sentence_object)

        return flagged_sentences

    @staticmethod
    def count_genders(flagged_corpus):
        """
        count the number of sentences in each of groups
        :param flagged_corpus: array of flagged sentences
        :return: 3 integer values, representing feminine, masculine and neutral groups respectively
        """
        feminine_count = len(
            [
                flag
                for flag in flagged_corpus
                if flag.get("feminine_flag") is True
            ]
        )
        masculine_count = len(
            [
                flag
                for flag in flagged_corpus
                if flag.get("masculine_flag") is True
            ]
        )
        neutral_count = len(
            [
                flag
                for flag in flagged_corpus
                if flag.get("neutral_flag") is True
            ]
        )
        return feminine_count, masculine_count, neutral_count

    @staticmethod
    def sort_groups(flagged_corpus):
        """
        sort the sentences in each of 3 groups
        :param flagged_corpus: array of flagged sentences
        :return: 3 arrays of strings, containing feminine, masculine and neutral groups respectively
        """
        feminine_group = [
                flag.get("sentence")
                for flag in flagged_corpus
                if flag.get("feminine_flag") is True
            ]
        masculine_group = [
                flag.get("sentence")
                for flag in flagged_corpus
                if flag.get("masculine_flag") is True
            ]
        neutral_group = [
                flag.get("sentence")
                for flag in flagged_corpus
                if flag.get("neutral_flag") is True
            ]
    
        return feminine_group, masculine_group, neutral_group

    def filter(self, sentences: []) -> bool:
        biased = False

        # Retrieve the flags for each of the sentences
        flagged_corpus = self.flag_sentences(sentences, self.language, self.feminine_input, self.masculine_input)

        # Use the retrieved flags to count the number of sentences in each group
        feminine_count, masculine_count, neutral_count = self.count_genders(
            flagged_corpus
        )

        # If the mumber of sentences in the target group is lower than in the test group, set bias to True
        # Note, that the neutral group is not taken into account in this calculation
        if feminine_count < masculine_count:
            biased = True
        else:
            biased = False

        return biased