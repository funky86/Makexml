To je readme za verzijo makexml_v2. Spremembe glede na prejšnjo verzijo:
----------------------------------
	- V input filu (Excel oziroma CSV) ni veè potrebno polje "Shares Left". Po novem to program izraèuna sam.
	- Prejšnja verzija je imela bug pri interpretaciji tradov z enakim tickerjem, vendar razliènim popisnim 
	  listom (PLVP oziroma PLVPSHORT). Kadar imamo nad istim tickerjem tako long kot short trade, 
	  jih moramo med seboj loèiti tako, da zaènemo z novim Transaction Id (0). 
	  Glej primer ARRY v priloženem input.xlsx.

Komponente programa
-------------------

	- base.xml - header XML fila, ki se samodejno doda na zaèetek tako kot zahteva XML struktura (za leto 2017). 
	  Naèeloma tega fila za sam uvoz tradov sploh ne rabimo (potreben je le za zgeneriranje output.xml), 
	  lahko pa si ga tudi popravimo s svojimi podatki.
	- conversion.txt - teèajnica USD/EUR, ki jo program uporabi za preraèun iz dolarjev v evre. Priložena je za obdobje 2016-2017. 
	- conversion.exe - program, s katerim si lahko zgeneriramo teèajnico za poljubno obdobje. Kako, glej spodaj.
	- input.csv - vnodni file s tradi za program. Kako ga narediti, glej spodaj.
	- output.xml - izhodni XML, ki se ga uvozi v eDavke
	- makexml_v2.exe - program, ki zgenerira output.xml

Uporaba makexml.exe - generiranje output.xml, ki ga lahko izvozimo v eDavke
-------------------
V isti mapi potrebujemo naslednje datoteke: base.xml, input.csv, makexml.exe in opcijsko conversion.txt.

Program lahko poženemo z ali brez valutne pretvorbe.

Primer s pretvorbo: makexml.exe convert
Primer brez pretvorbe: makexml.exe

Program bo zgeneriral output.xml na osnovi base.xml, input.csv ter opcijsko conversion.txt (èe uporabljamo pretvorbo).

Uporaba conversion.exe - generiranje teèajnice conversion.txt za poljubno obdobje
-------------------

Èe želimo zgenerirati drugo teèajnico, si moramo najprej prenesti xml (Prenos èasovnih serij od 2017) s strani:
https://www.bsi.si/statistika/devizni-tecaji-in-plemenite-kovine/dnevna-tecajnica-referencni-tecaji-ecb

Prenešeni xml moramo preimenovati v "conversion.xml". Lahko ga poljubno popravimo (izberemo samo doloèeno obdobje).

Potem enostavno zgeneriramo conversion.txt tako, da poženemo "conversion.exe".

Priprava datoteke input.csv - fila z našimi tradi, ki ga bomo pretvorili v xml
---------------------------
Datoteka input.csv je spisek napih tradov in je osnova za program, iz katerega se zgenerira output.xml.
Struktura input.csv je vnaprej predvidena in mora biti toèno taka, kot zahteva program, sicer
pretvorba ne bo delovala. Kakšna mora biti struktura, je razvidno v priloženem input.csv. Priložen je tudi
excel file input.xlsx, iz katerega sem izvozil CSD datoteko input.csv. Sledi razlaga
posameznih stolpcev in navodila za izvoz XLSX v CSD.

	- Ticker - ticker delnice (na primer "ACFC")
	- Transaction Id - zaporedna številka transakcije z isto delnico (od 0 do N)
	- Transaction Type - tip transakcije (Buy, Sell, SellShort, BuyCover)
	- Date - datum v obliki yyyy-mm-dd (uporabimo Formal Cells/Date na stolpcu, da dobimo pravilen format
	- Shares - število delnic, na 4 decimalke
	- Price - cena, na 4 decimalke 
	- Loss Valid - ali se izguba prizna, glej pravilo navidezne odsvojitve (true/false)

Celoten excel file je potrebno roèno pripraviti za vse transakcije in ga shraniti kot (Save As)
CSV (Comma Delimited file). 

V trenutni implementaciji kot loèilo med elementi uporabljam podpièje (;).

Vse decimalne vrednosti morajo biti oznaèene s piko (.). Èe imamo v excelu za decimalno loèilo vejico (,),
jih lahko s pomoèjo teh navodil zaèasno pretvorimo v piko, da zgeneriramo pravilen csv: 
https://support.office.com/en-us/article/change-the-character-used-to-separate-thousands-or-decimals-c093b545-71cb-4903-b205-aebb9837bd1e

V CSV filu je potem potrebno roèno odstraniti prvo vrstico (imena stolpcev). Lahko tudi
vse zaloge kapitala 0.0000 z uporabo funkcije "Replace" pretvorimo v 0, da dobimo lepši zapis, ni pa 
to nujno.

Primer pravilnega CSV fila je input.csv. 

Primer izhodnega xml, ki sem ga zgeneriral na osnovi priloženih input.csv in conversion.txt, je output.xml.

Sourci
------
Priložena sta sourca makexml_v2.cpp in conversion.cpp. Èe želimo druga imena filov ali delimiterja ali pa mogoèe
vnos poljubnih imen filov, je to potrebno popraviti v .cpp in jih prevesti.

Ostalo
------
Za kakršnekoli napake pri pretvorbi podatkov ne odgovarjam! V vsakem primeru je potreben
rocen pregled vseh tradov v eDavkih. Ce bo prislo do spremembe sheme, bom naredil novo
verzijo base.xml fila takoj, ko bom utegnil. Program sem stestiral na Windows 10 in Linux,
na priloženih testnih filih, ter na filu s svojimi realnimi tradi. 
Na obeh sistemih je zgeneriral enak XML, ki sem ga potem tudi uspešno uvozil v eDavke.
Program bi moral v celoti podpirati Doh_KDVP format z long in short tradi z možnostjo
poljubnega zaporedna izvajanja tradov na istem tickerju, seveda pod pogojem, da so ti
pravilno (v pravilnem èasovnem zaporedju) vnešeni v input Excel file.

Kontakt
-------
Za vse dodatne informacije, predloge ali želje sem na voljo na juretrader@gmail.com.
