To je readme za verzijo makexml_v2. Spremembe glede na prej�njo verzijo:
----------------------------------
	- V input filu (Excel oziroma CSV) ni ve� potrebno polje "Shares Left". Po novem to program izra�una sam.
	- Prej�nja verzija je imela bug pri interpretaciji tradov z enakim tickerjem, vendar razli�nim popisnim 
	  listom (PLVP oziroma PLVPSHORT). Kadar imamo nad istim tickerjem tako long kot short trade, 
	  jih moramo med seboj lo�iti tako, da za�nemo z novim Transaction Id (0). 
	  Glej primer ARRY v prilo�enem input.xlsx.

Komponente programa
-------------------

	- base.xml - header XML fila, ki se samodejno doda na za�etek tako kot zahteva XML struktura (za leto 2017). 
	  Na�eloma tega fila za sam uvoz tradov sploh ne rabimo (potreben je le za zgeneriranje output.xml), 
	  lahko pa si ga tudi popravimo s svojimi podatki.
	- conversion.txt - te�ajnica USD/EUR, ki jo program uporabi za prera�un iz dolarjev v evre. Prilo�ena je za obdobje 2016-2017. 
	- conversion.exe - program, s katerim si lahko zgeneriramo te�ajnico za poljubno obdobje. Kako, glej spodaj.
	- input.csv - vnodni file s tradi za program. Kako ga narediti, glej spodaj.
	- output.xml - izhodni XML, ki se ga uvozi v eDavke
	- makexml_v2.exe - program, ki zgenerira output.xml

Uporaba makexml.exe - generiranje output.xml, ki ga lahko izvozimo v eDavke
-------------------
V isti mapi potrebujemo naslednje datoteke: base.xml, input.csv, makexml.exe in opcijsko conversion.txt.

Program lahko po�enemo z ali brez valutne pretvorbe.

Primer s pretvorbo: makexml.exe convert
Primer brez pretvorbe: makexml.exe

Program bo zgeneriral output.xml na osnovi base.xml, input.csv ter opcijsko conversion.txt (�e uporabljamo pretvorbo).

Uporaba conversion.exe - generiranje te�ajnice conversion.txt za poljubno obdobje
-------------------

�e �elimo zgenerirati drugo te�ajnico, si moramo najprej prenesti xml (Prenos �asovnih serij od 2017) s strani:
https://www.bsi.si/statistika/devizni-tecaji-in-plemenite-kovine/dnevna-tecajnica-referencni-tecaji-ecb

Prene�eni xml moramo preimenovati v "conversion.xml". Lahko ga poljubno popravimo (izberemo samo dolo�eno obdobje).

Potem enostavno zgeneriramo conversion.txt tako, da po�enemo "conversion.exe".

Priprava datoteke input.csv - fila z na�imi tradi, ki ga bomo pretvorili v xml
---------------------------
Datoteka input.csv je spisek napih tradov in je osnova za program, iz katerega se zgenerira output.xml.
Struktura input.csv je vnaprej predvidena in mora biti to�no taka, kot zahteva program, sicer
pretvorba ne bo delovala. Kak�na mora biti struktura, je razvidno v prilo�enem input.csv. Prilo�en je tudi
excel file input.xlsx, iz katerega sem izvozil CSD datoteko input.csv. Sledi razlaga
posameznih stolpcev in navodila za izvoz XLSX v CSD.

	- Ticker - ticker delnice (na primer "ACFC")
	- Transaction Id - zaporedna �tevilka transakcije z isto delnico (od 0 do N)
	- Transaction Type - tip transakcije (Buy, Sell, SellShort, BuyCover)
	- Date - datum v obliki yyyy-mm-dd (uporabimo Formal Cells/Date na stolpcu, da dobimo pravilen format
	- Shares - �tevilo delnic, na 4 decimalke
	- Price - cena, na 4 decimalke 
	- Loss Valid - ali se izguba prizna, glej pravilo navidezne odsvojitve (true/false)

Celoten excel file je potrebno ro�no pripraviti za vse transakcije in ga shraniti kot (Save As)
CSV (Comma Delimited file). 

V trenutni implementaciji kot lo�ilo med elementi uporabljam podpi�je (;).

Vse decimalne vrednosti morajo biti ozna�ene s piko (.). �e imamo v excelu za decimalno lo�ilo vejico (,),
jih lahko s pomo�jo teh navodil za�asno pretvorimo v piko, da zgeneriramo pravilen csv: 
https://support.office.com/en-us/article/change-the-character-used-to-separate-thousands-or-decimals-c093b545-71cb-4903-b205-aebb9837bd1e

V CSV filu je potem potrebno ro�no odstraniti prvo vrstico (imena stolpcev). Lahko tudi
vse zaloge kapitala 0.0000 z uporabo funkcije "Replace" pretvorimo v 0, da dobimo lep�i zapis, ni pa 
to nujno.

Primer pravilnega CSV fila je input.csv. 

Primer izhodnega xml, ki sem ga zgeneriral na osnovi prilo�enih input.csv in conversion.txt, je output.xml.

Sourci
------
Prilo�ena sta sourca makexml_v2.cpp in conversion.cpp. �e �elimo druga imena filov ali delimiterja ali pa mogo�e
vnos poljubnih imen filov, je to potrebno popraviti v .cpp in jih prevesti.

Ostalo
------
Za kakr�nekoli napake pri pretvorbi podatkov ne odgovarjam! V vsakem primeru je potreben
rocen pregled vseh tradov v eDavkih. Ce bo prislo do spremembe sheme, bom naredil novo
verzijo base.xml fila takoj, ko bom utegnil. Program sem stestiral na Windows 10 in Linux,
na prilo�enih testnih filih, ter na filu s svojimi realnimi tradi. 
Na obeh sistemih je zgeneriral enak XML, ki sem ga potem tudi uspe�no uvozil v eDavke.
Program bi moral v celoti podpirati Doh_KDVP format z long in short tradi z mo�nostjo
poljubnega zaporedna izvajanja tradov na istem tickerju, seveda pod pogojem, da so ti
pravilno (v pravilnem �asovnem zaporedju) vne�eni v input Excel file.

Kontakt
-------
Za vse dodatne informacije, predloge ali �elje sem na voljo na juretrader@gmail.com.
