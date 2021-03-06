# e-Linguistics Toolkit: Dictionary
#
# Copyright (C) 2008 ELTK Project
# Author: Scott Farrar <farrar@u.washington.edu>
# URL: <http://e-linguistics.org>
# For license information, see LICENSE.TXT

import codecs
from eltk.utils.CharConverter import *


"""
This module contains classes used to create dictionaries and entries meant for display.
"""

class DictEntry:
    
    """
    A dictionary entry minimally containing a  head word and a translation.
    (Optional elements could include: part of speech, notes) 

    All display containers here should contain string representations of the underlying information (ie ling units). Formating details such as parens or commas and other markup are contained in printXXX methods.
    """
    
    def __init__(self,head,translation,pos=''):
        self.head_word=head
        self.pos=pos
        self.alt_forms={} #keys=string, values=set of strings
        self.translation=translation
                
    def __cmp__(self,de):

        """
        Compare two entries based on their head word
            
        TODO: use an ipa map to decide
        """

        if self.head_word>de.head_word:
            return 1
        elif self.head_word<de.head_word:
            return -1
        else: return 0



    def addAltForm(self,fv,alt):
        
        """
        Method for adding alternate forms to an existing entry
        
        @type  fv: string 
        @param fv: A feature value name
        @type  alt: string 
        @param alt: Alternate form, a set of forms
        
        
        """

        self.alt_forms[fv]=alt
   
    
    def addPOS(self,cat):
        pos=cat


    def printPretty(self):

        """
        Used to display entry to stndout

        """
    

        #unpack head words
        heads=[]
        for h in self.head_word:
            heads.append(h)
        
        if heads=='': heads='[not_transcribed]'
        
        

        #unpack alternate forms
        alts='('
        keys=self.alt_forms.keys()

        for k in keys:
            alts=alts+k+': '
            
            for i in self.alt_forms[k]:
                if i is not None:
                    alts=alts+i+', '

        alts=alts+')'
        alts=alts.replace(', )',')')
        if alts=='()': alts=''
        

        
        #unpack translations
        trans=''
        for t in self.translation:
            if t is not None:
                trans=trans+t+', '
            else: trans=trans
        trans=trans[:len(trans)-2]
            
            

        print printList(heads)+' '+alts+': '+trans
        


       


class BilingualDictionary:

    """
    A bilingual dictionary containing two sets of entries.
    
    """



    def __init__(self,langs):

        """
        langs   list of two language names
        """

        self.obj_lang=langs[0]
        self.meta_lang=langs[1]
        self.entries_1={}
        self.entries_2={}
    
    def addEntry_1(self,e):
       
        """
        Adds an entry to entries_1

        e       a dictionary entry
        
        """


        head_words=list(e.head_word)

        for h in head_words:

            
            
            self.entries_1[h]=e
            #e.printPretty()

    def addEntry_2(self,e):

        """
        Add an entry to entries_2

        e       a dictionary entry
        """

        head_words=list(e.head_word)
         
        for h in head_words:
            
            self.entries_2[h]=e
            #e.printPretty()




    def printPretty(self):
        """
        Prints dictionary to stndout.
        """
        

        #print part I
        keys=self.entries_1.keys()

        keys.sort()

        for k in keys:
            self.entries_1[k].printPretty()
        
        #print part II
        keys_2=self.entries_2.keys()

        keys_2.sort()

        for k in keys_2:
            self.entries_2[k].printPretty()
        

    def toLatex(self,out_file):
           
        """ 
        Outputs a tex file, converting from IPA to TIPA for each entry.
        
        out_file        The name of the tex output file
        
        This requires the following tex ackages: tipa, linguex, supertabular
        """
        
        print 'Printing to LeTex file...'

        converter=CharConverter('ipa','tipa')
        
        latex_header=u'%This document was autogenerated using from  a Python script.\n\documentclass[letter,12pt]{article}\n\\usepackage{linguex}\n\n\\usepackage[tone,extra]{tipa}\n\\usepackage{supertabular}\n\n\\begin{document}\n\n'
        
        outfile=codecs.open(out_file,'w','utf-8')
        outfile.write(latex_header)

        ############begin first section of bilingual dictionary###################3

        outfile.write(u'\\section*{'+self.obj_lang+u'--'+self.meta_lang+u' Dictionary}\n\n')

        outfile.write(u'\\begin{supertabular}{lll}\n\n')   


        keys=self.entries_1.keys()
        
        keys.sort()
        

        for k in keys:
            
            #headword      
            head_word=converter.convert(k)
            head_word=tipaClean(head_word)
            
            #alt forms
            keys2=self.entries_1[k].alt_forms.keys()
            alts='('
            for k2 in keys2:
                alts=alts+k2+': '
            
                for i in self.entries_1[k].alt_forms[k2]:
                    if i is not None:
                        #################START HERE with tipa issue
                        #print i+' ',
                        i=converter.convert(i)
                        i=tipaClean(i) 
                        #print i
                        alts=alts+'\\textipa{'+i+'}, '

            alts=alts+')'
            alts=alts.replace(', )',')')
            if alts=='()': alts=''
 
            #translation
            translation=''
            for t in self.entries_1[k].translation:
                translation=translation+t+', '
            translation=translation[:len(translation)-2]
            translation=translation.replace('_','\_')

             
            outfile.write(u'\\textbf{\\textipa{'+head_word+u'}}&'+alts+u'&'+translation+u'\\\\\\\\\n')

        outfile.write(u'\end{supertabular}\n\n')
        
        
        
        ############begin next section of bilingual dictionary###################3

        outfile.write(u'\\section*{'+self.meta_lang+u'--'+self.obj_lang+u' Dictionary}\n\n')

        outfile.write(u'\\begin{supertabular}{lll}\n\n') 
        




        keys_2=self.entries_2.keys()

        keys_2.sort()

        for k in keys_2:
            
            #head word
            head_word=k
            head_word=head_word.replace('_','\_')



            #unpack translations
            trans=''
            for t in self.entries_2[k].translation:
                if t is not None:
                    t=converter.convert(t)
                    t=tipaClean(t)
                    trans=trans+t+', '
                else: trans=trans
            trans=trans[:len(trans)-2]
           
            outfile.write(u'\\textbf{'+head_word+u'}&'+''+u'&\\textipa{'+trans+u'}\\\\\\\\\n')

         
        outfile.write(u'\end{supertabular}\n\n\end{document}')
        outfile.close()

      
    def extractBilingualDictionary(self,univ,entry_contents):

        """
        Populates a BilingualDictionary from a universe and desired contents of an entry
            
        univ                    the ling universe to extract entries from

        entry_contents          a list of feature value labels used to construct entry

        """
        
        print 'Extracting bilingual dictionary...'
       
        #begin extract object language --- metalanguage part
        
        morpheme_lists=univ.getMorphemes(self.obj_lang)
        
        for l in morpheme_lists:
            
            head_words=univ.getForm(l)
            
            for h in head_words:
                 
                if h is not '':
                    #instantiate dict. entry
                    d=DictEntry([h],([l[0].label]))
            
            
            
                    #build alt forms, eg plurals
                    data_list=univ.getData('PL.'+l[0].label,1)
            
                    if data_list is not None and len(data_list)>=1: 
                
                        forms=univ.getForm(data_list)
                
                
                        d.addAltForm('PL',forms)

                    self.addEntry_1(d)
                #d.printPretty()



        #begin extract meta language--object language part 
        morpheme_lists=univ.getMorphemes(self.obj_lang) 
         
        for l in morpheme_lists:
                        
            
            translations=univ.getForm(l) 
             
            
            d=DictEntry(([l[0].label]),translations)
            

            self.addEntry_2(d)
            #d.printPretty()
 
