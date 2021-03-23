from POCs.poc-reading-grades.readability_indexing.py


def run_comparison(text1, text2):
    print("ARI: {ARI}".format(ARI=ARI(text1)))
    print("ARI (EN): {ARI}".format(ARI=ARI(text2)))
    print("FRE: {FRE}".format(FRE=flesch_reading_ease(text1, True)))
    print("FRE (EN): {FRE}".format(FRE=flesch_reading_ease(text2, False)))
    print("FKG: {FKG}".format(FKG=flesch_kincaid_grade(text1, True)))
    print("FKG (EN): {FKG}".format(FKG=flesch_kincaid_grade(text2, False)))
    print("GFI: {GFI}".format(GFI=gunning_fog_index(text1, True)))
    print("GFI (EN): {GFI}".format(GFI=gunning_fog_index(text2, False)))
    print("------------------------------------------")

test_1 = "Ik ben makelaar in koffi, en woon op de Lauriergracht. Het is mijn gewoonte niet, romans te schrijven, of zulke dingen, en het heeft dan ook lang geduurd, voor ik er toe overging een paar riem papier extra te bestellen, en het werk aan te vangen, dat gij, lieve lezer, in de hand hebt genomen, en dat ge lezen moet als ge makelaar in koffie zijt, of als ge wat anders zijt. Niet alleen dat ik nooit iets schreef wat naar een roman geleek, maar ik houd er zelfs niet van, iets dergelijks te lezen."
translated_1 = "I am a coffee broker and live on the Lauriergracht. It is not my habit to write novels or such things, and it took a long time before I proceeded to order a few extra reams of paper, and begin the work that you, dear reader, have in the hand, and that you should read if you are a broker in coffee, or if you are something else. Not only that I never wrote anything that looked like a novel, but I don't even like to read something like that."

test_2 =  "De volle maan, tragisch dien avond, was reeds vroeg, nog in den laatsten dagschemer opgerezen als een immense, bloedroze bol, vlamde als een zonsondergang laag achter de tamarindeboomen der Lange Laan en steeg, langzaam zich louterende van hare tragische tint, in een vagen hemel op. Een doodsche stilte spande alom als een sluier van zwijgen, of, na de lange middagsiësta, de avondrust zonder overgang van leven begon."
translated_2 = "The full moon, tragic that evening, had risen early in the last twilight as an immense, blood-pink sphere, blazed like a sunset low behind the tamarind trees of Lange Laan and rose, slowly purifying itself of its tragic hue, in a vague heaven. A dead silence stretched all over like a veil of silence, or, after the long afternoon siesta, the evening rest began without a transition of life." 

test_3 = "Onbegrijpelijk veel mensen hebben familiebetrekkingen, vrienden of kennissen te Amsterdam. Het is een verschijnsel dat ik eenvoudig toeschrijf aan de veelheid der inwoners van die hoofdstad. Ik had er voor een paar jaren nog een verre neef. Waar hij nu is, weet ik niet. Ik geloof dat hij naar de West gegaan is. Misschien heeft de een of ander van mijn lezers hem wel brieven meegegeven. In dat geval hebben zij een nauwgezette, maar onvriendelijke bezorger gehad, als uit de inhoud van deze weinige bladzijden waarschijnlijk duidelijk worden zal." 
translated_3 = "Incomprehensibly many people have family relationships, friends or acquaintances in Amsterdam. It is a phenomenon that I simply attribute to the multitude of inhabitants of that capital. I had a distant cousin there for a few years. I don't know where he is now. I believe he went to the West. Maybe some of my readers gave him letters. In that case they have had a conscientious but unfriendly delivery person, as will probably become apparent from the contents of these few pages."

run_comparison(test_1, translated_1)
run_comparison(test_2, translated_2)
run_comparison(test_3, translated_3)